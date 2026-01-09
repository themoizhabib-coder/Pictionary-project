from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from app.models import db, User, GameSession, Round, Word, UserStats
from app.word_selector import select_word
from app.image_generator import generate_image
from app.guess_processor import process_guess
from app.database import init_db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///bictionary.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db.init_app(app)
CORS(app)

# Initialize database
print("🚀 Starting application...", flush=True)
try:
    with app.app_context():
        print("📁 Initializing database...", flush=True)
        db.create_all()
        print("✅ Database tables created", flush=True)
        
        # Check if already seeded
        from app.models import User
        if User.query.first():
            print("✅ Database already seeded with data", flush=True)
        else:
            print("🌱 Seeding database with test data...", flush=True)
            from app.database import seed_database
            seed_database()
            print("✅ Database seeded successfully", flush=True)
except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

# ==================== GAME ENDPOINTS ====================

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start a new game session"""
    data = request.json
    user_id = data.get('user_id')
    age_group = data.get('age_group', 'adult')
    difficulty = data.get('difficulty', 'medium')
    language = data.get('language', 'en')
    total_rounds = data.get('rounds', 10)
    
    try:
        session = GameSession(
            user_id=user_id,
            age_group=age_group,
            difficulty=difficulty,
            language=language,
            total_rounds=total_rounds,
            started_at=datetime.now()
        )
        db.session.add(session)
        db.session.commit()
        
        # Start first round
        round = start_round(session.id)
        
        return jsonify({
            'success': True,
            'session_id': session.id,
            'round': round,
            'total_rounds': total_rounds
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def start_round(session_id):
    """Start a new round within a game session"""
    session = GameSession.query.get(session_id)
    if not session:
        return None
    
    # Select word based on age group and difficulty
    word_data = select_word(
        age_group=session.age_group,
        difficulty=session.difficulty,
        language=session.language
    )
    
    if not word_data:
        return None
    
    word_obj = Word.query.filter_by(word=word_data['word']).first()
    if not word_obj:
        word_obj = Word(
            word=word_data['word'],
            definition=word_data.get('definition', ''),
            translation=word_data.get('translation', ''),
            difficulty=session.difficulty,
            category=word_data.get('category', 'general'),
            age_group=session.age_group
        )
        db.session.add(word_obj)
        db.session.commit()
    
    # Generate AI image
    image_url = generate_image(word_data['word'], style="sketch")
    
    # Create round record
    round_obj = Round(
        session_id=session_id,
        word_id=word_obj.id,
        image_url=image_url,
        started_at=datetime.now(),
        duration_seconds=60
    )
    db.session.add(round_obj)
    db.session.commit()
    
    return {
        'round_id': round_obj.id,
        'round_number': round_obj.round_number,
        'image_url': image_url,
        'hint': generate_hint(word_data['word']),
        'timer_seconds': 60
    }


@app.route('/api/guess', methods=['POST'])
def handle_guess():
    """Process a player's guess"""
    data = request.json
    session_id = data.get('session_id')
    round_id = data.get('round_id')
    user_guess = data.get('guess', '').strip()
    time_taken = data.get('time_taken', 0)
    
    try:
        round_obj = Round.query.get(round_id)
        if not round_obj:
            return jsonify({'error': 'Round not found'}), 404
        
        word = round_obj.word.word
        
        # Process the guess with fuzzy matching
        result = process_guess(
            user_guess=user_guess,
            correct_word=word,
            time_taken=time_taken,
            max_time=60
        )
        
        # Calculate points
        points = 0
        if result['is_correct']:
            points = calculate_points(time_taken, result['match_type'])
        
        # Update round with result
        round_obj.guesses_count += 1
        if result['is_correct']:
            round_obj.is_guessed = True
            round_obj.guessed_at = datetime.now()
        
        db.session.commit()
        
        # Update user stats
        update_user_stats(round_obj.session.user_id, result['is_correct'], points)
        
        return jsonify({
            'success': True,
            'is_correct': result['is_correct'],
            'match_type': result['match_type'],
            'points': points,
            'correct_answer': word if result['is_correct'] else None,
            'message': result['message']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/next-round', methods=['POST'])
def next_round():
    """Move to the next round"""
    data = request.json
    session_id = data.get('session_id')
    
    try:
        session = GameSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        current_round_count = Round.query.filter_by(session_id=session_id).count()
        
        if current_round_count >= session.total_rounds:
            # Game is over
            session.ended_at = datetime.now()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'game_over': True,
                'final_score': calculate_session_score(session_id)
            }), 200
        
        # Start next round
        round_data = start_round(session_id)
        
        return jsonify({
            'success': True,
            'game_over': False,
            'round': round_data,
            'current_round': current_round_count + 1,
            'total_rounds': session.total_rounds
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/game-summary/<int:session_id>', methods=['GET'])
def game_summary(session_id):
    """Get summary of completed game"""
    try:
        session = GameSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        rounds = Round.query.filter_by(session_id=session_id).all()
        
        summary = {
            'session_id': session_id,
            'total_rounds': session.total_rounds,
            'guessed_correctly': sum(1 for r in rounds if r.is_guessed),
            'total_points': calculate_session_score(session_id),
            'words_learned': [
                {
                    'word': r.word.word,
                    'definition': r.word.definition,
                    'translation': r.word.translation,
                    'category': r.word.category,
                    'guessed': r.is_guessed
                }
                for r in rounds
            ],
            'duration': (session.ended_at - session.started_at).total_seconds() if session.ended_at else None
        }
        
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== USER ENDPOINTS ====================

@app.route('/api/user/create', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    username = data.get('username')
    age = data.get('age', 18)
    language = data.get('language', 'en')
    
    try:
        user = User(
            username=username,
            age=age,
            preferred_language=language,
            created_at=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'username': user.username
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<int:user_id>/stats', methods=['GET'])
def user_stats(user_id):
    """Get user statistics"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        stats = UserStats.query.filter_by(user_id=user_id).first()
        
        if not stats:
            return jsonify({
                'user_id': user_id,
                'username': user.username,
                'total_games': 0,
                'total_correct_guesses': 0,
                'total_points': 0,
                'average_accuracy': 0
            }), 200
        
        return jsonify({
            'user_id': user_id,
            'username': user.username,
            'total_games': stats.total_games_played,
            'total_correct_guesses': stats.total_correct_guesses,
            'total_points': stats.total_points,
            'average_accuracy': stats.accuracy_percentage,
            'words_learned': stats.words_learned,
            'average_time_per_guess': stats.average_time_per_guess,
            'streak': stats.current_streak
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PSYCHOLOGY ANALYTICS ENDPOINTS ====================

@app.route('/api/psychology/learning-curve/<int:user_id>', methods=['GET'])
def learning_curve(user_id):
    """Get user's learning curve data"""
    try:
        sessions = GameSession.query.filter_by(user_id=user_id).order_by(GameSession.started_at).all()
        
        learning_data = []
        cumulative_correct = 0
        
        for session in sessions:
            rounds = Round.query.filter_by(session_id=session.id).all()
            correct_in_session = sum(1 for r in rounds if r.is_guessed)
            cumulative_correct += correct_in_session
            
            learning_data.append({
                'session_number': len(learning_data) + 1,
                'correct_guesses': correct_in_session,
                'cumulative_correct': cumulative_correct,
                'total_in_session': len(rounds),
                'accuracy': (correct_in_session / len(rounds) * 100) if rounds else 0,
                'date': session.started_at.isoformat()
            })
        
        return jsonify({
            'user_id': user_id,
            'learning_data': learning_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/psychology/cognitive-metrics/<int:user_id>', methods=['GET'])
def cognitive_metrics(user_id):
    """Get cognitive performance metrics"""
    try:
        sessions = GameSession.query.filter_by(user_id=user_id).all()
        
        metrics = {
            'reaction_time': calculate_avg_reaction_time(user_id),
            'memory_retention': calculate_retention_rate(user_id),
            'difficulty_progression': calculate_difficulty_progression(user_id),
            'category_performance': calculate_category_performance(user_id),
            'visual_recognition': calculate_visual_recognition_score(user_id)
        }
        
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/psychology/comparative-analysis', methods=['GET'])
def comparative_analysis():
    """Compare performance across all users"""
    try:
        all_users = User.query.all()
        
        analysis = {
            'average_accuracy': 0,
            'average_points': 0,
            'most_popular_category': None,
            'top_performers': []
        }
        
        if all_users:
            total_accuracy = 0
            total_points = 0
            category_counts = {}
            
            user_scores = []
            for user in all_users:
                stats = UserStats.query.filter_by(user_id=user.id).first()
                if stats:
                    total_accuracy += stats.accuracy_percentage
                    total_points += stats.total_points
                    user_scores.append({
                        'username': user.username,
                        'points': stats.total_points,
                        'accuracy': stats.accuracy_percentage
                    })
            
            analysis['average_accuracy'] = total_accuracy / len(all_users) if all_users else 0
            analysis['average_points'] = total_points / len(all_users) if all_users else 0
            analysis['top_performers'] = sorted(user_scores, key=lambda x: x['points'], reverse=True)[:10]
        
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Get comprehensive dashboard data"""
    try:
        # Get all users and their stats
        all_users = User.query.all()
        leaderboard = []
        
        for user in all_users:
            stats = UserStats.query.filter_by(user_id=user.id).first()
            if stats:
                leaderboard.append({
                    'user_id': user.id,
                    'username': user.username,
                    'points': stats.total_points,
                    'accuracy': round(stats.accuracy_percentage, 2),
                    'games_played': stats.total_games_played,
                    'words_learned': stats.words_learned
                })
        
        leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)
        
        # Get statistics
        total_games = GameSession.query.count()
        total_guesses = Round.query.count()
        avg_accuracy = sum(u['accuracy'] for u in leaderboard) / len(leaderboard) if leaderboard else 0
        
        # Get category distribution
        all_words = Word.query.all()
        category_dist = {}
        for word in all_words:
            cat = word.category or 'Unknown'
            category_dist[cat] = category_dist.get(cat, 0) + 1
        
        return jsonify({
            'total_users': len(all_users),
            'total_games': total_games,
            'total_guesses': total_guesses,
            'average_accuracy': round(avg_accuracy, 2),
            'leaderboard': leaderboard[:10],
            'category_distribution': category_dist,
            'age_groups': ['5-7', '8-12', 'Adult'],
            'timestamps': {
                'last_updated': datetime.now().isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users with their stats"""
    try:
        users = User.query.all()
        users_data = []
        
        for user in users:
            stats = UserStats.query.filter_by(user_id=user.id).first()
            users_data.append({
                'user_id': user.id,
                'username': user.username,
                'age': user.age,
                'language': user.preferred_language,
                'stats': {
                    'total_games': stats.total_games_played if stats else 0,
                    'total_points': stats.total_points if stats else 0,
                    'accuracy': round(stats.accuracy_percentage, 2) if stats else 0,
                    'words_learned': stats.words_learned if stats else 0
                }
            })
        
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/words', methods=['GET'])
def get_all_words():
    """Get all available words"""
    try:
        words = Word.query.all()
        words_data = []
        
        for word in words:
            words_data.append({
                'id': word.id,
                'word': word.word,
                'definition': word.definition,
                'translation': word.translation,
                'category': word.category,
                'difficulty': word.difficulty,
                'age_group': word.age_group,
                'image_url': f'/api/image/{word.id}'
            })
        
        return jsonify(words_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== HELPER FUNCTIONS ====================

def generate_hint(word, reveal_percent=0.3):
    """Generate a hint for a word"""
    reveal_count = max(1, int(len(word) * reveal_percent))
    hint = list('_' * len(word))
    import random
    positions = random.sample(range(len(word)), reveal_count)
    for pos in positions:
        hint[pos] = word[pos]
    return ''.join(hint)


def calculate_points(time_taken, match_type):
    """Calculate points based on time and match accuracy"""
    base_points = 100
    
    if match_type == 'exact':
        time_bonus = max(0, 100 - (time_taken // 6))  # -1 point per 6 seconds
        return base_points + time_bonus
    elif match_type == 'fuzzy':
        return int(base_points * 0.75)
    elif match_type == 'synonym':
        return int(base_points * 0.5)
    
    return 0


def update_user_stats(user_id, is_correct, points):
    """Update user statistics"""
    stats = UserStats.query.filter_by(user_id=user_id).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        db.session.add(stats)
    
    stats.total_correct_guesses += 1 if is_correct else 0
    stats.total_points += points
    stats.total_guesses += 1
    stats.accuracy_percentage = (stats.total_correct_guesses / stats.total_guesses * 100) if stats.total_guesses > 0 else 0
    
    if is_correct:
        stats.current_streak += 1
    else:
        stats.current_streak = 0
    
    db.session.commit()


def calculate_session_score(session_id):
    """Calculate total score for a session"""
    rounds = Round.query.filter_by(session_id=session_id).all()
    return sum(r.points_earned for r in rounds if r.points_earned)


def calculate_avg_reaction_time(user_id):
    """Calculate average reaction time for guesses"""
    sessions = GameSession.query.filter_by(user_id=user_id).all()
    total_time = 0
    total_guesses = 0
    
    for session in sessions:
        rounds = Round.query.filter_by(session_id=session.id).all()
        for round_obj in rounds:
            if round_obj.guessed_at:
                time_diff = (round_obj.guessed_at - round_obj.started_at).total_seconds()
                total_time += time_diff
                total_guesses += 1
    
    return total_time / total_guesses if total_guesses > 0 else 0


def calculate_retention_rate(user_id):
    """Calculate how well user retains learned words"""
    # This would track if users get the same word right multiple times
    return 0.0


def calculate_difficulty_progression(user_id):
    """Track if user is progressing through difficulty levels"""
    return {}


def calculate_category_performance(user_id):
    """Performance breakdown by category"""
    return {}


def calculate_visual_recognition_score(user_id):
    """Score based on visual recognition performance"""
    return 0.0


if __name__ == '__main__':
    app.run(debug=True, port=5001)

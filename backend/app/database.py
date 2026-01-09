from app.models import db, User, GameSession, Round, Word, UserStats
from app.word_selector import WORD_DATABASE
from datetime import datetime, timedelta
import random

def init_db():
    """Initialize database with tables and seed data"""
    db.create_all()
    seed_database()


def seed_database():
    """Seed database with test data"""
    
    # Check if data already exists
    if User.query.first():
        return  # Already seeded
    
    # Create test users
    users_data = [
        {'username': 'emma_5yo', 'age': 5, 'language': 'en'},
        {'username': 'alex_10yo', 'age': 10, 'language': 'en'},
        {'username': 'john_adult', 'age': 25, 'language': 'en'},
        {'username': 'maria_bilingual', 'age': 8, 'language': 'es'},
        {'username': 'sophie_learner', 'age': 12, 'language': 'en'},
        {'username': 'carlos_spanish', 'age': 30, 'language': 'es'},
        {'username': 'anna_young', 'age': 6, 'language': 'en'},
        {'username': 'thomas_teen', 'age': 15, 'language': 'en'},
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            age=user_data['age'],
            preferred_language=user_data['language'],
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    
    # Create words in database
    for age_group in WORD_DATABASE:
        for difficulty in WORD_DATABASE[age_group]:
            for word_data in WORD_DATABASE[age_group][difficulty]:
                # Check if word already exists
                if not Word.query.filter_by(word=word_data['word']).first():
                    word = Word(
                        word=word_data['word'],
                        definition=word_data['definition'],
                        translation=word_data['translation'],
                        difficulty=difficulty,
                        category=word_data['category'],
                        age_group=age_group,
                        is_appropriate=True,
                        created_at=datetime.now()
                    )
                    db.session.add(word)
    
    db.session.commit()
    
    # Create sample game sessions and rounds
    for user in users[:3]:  # Create sessions for first 3 users
        # Create 3 completed games for each user
        for game_num in range(3):
            session = GameSession(
                user_id=user.id,
                age_group=get_age_group(user.age),
                difficulty=random.choice(['easy', 'medium', 'hard']),
                language=user.preferred_language,
                total_rounds=10,
                started_at=datetime.now() - timedelta(days=random.randint(1, 20)),
                ended_at=datetime.now() - timedelta(days=random.randint(0, 19))
            )
            db.session.add(session)
            db.session.flush()  # Get session ID
            
            # Create 10 rounds for each session
            words = Word.query.limit(10).all()
            correct_count = 0
            total_points = 0
            
            for i, word in enumerate(words):
                is_guessed = random.random() > 0.3  # 70% success rate
                time_taken = random.uniform(5, 55)
                
                round_obj = Round(
                    session_id=session.id,
                    word_id=word.id,
                    round_number=i + 1,
                    image_url=f'https://via.placeholder.com/512?text={word.word}',
                    started_at=session.started_at + timedelta(minutes=i*1.5),
                    guessed_at=session.started_at + timedelta(minutes=i*1.5) + timedelta(seconds=time_taken) if is_guessed else None,
                    duration_seconds=60,
                    is_guessed=is_guessed,
                    guesses_count=random.randint(1, 3) if is_guessed else random.randint(1, 5),
                    points_earned=100 if is_guessed else 0
                )
                db.session.add(round_obj)
                
                if is_guessed:
                    correct_count += 1
                    total_points += 100
            
            db.session.commit()
            
            # Update user stats
            stats = UserStats.query.filter_by(user_id=user.id).first()
            if not stats:
                stats = UserStats(
                    user_id=user.id,
                    total_games_played=0,
                    total_correct_guesses=0,
                    total_guesses=0,
                    total_points=0,
                    words_learned=0,
                    accuracy_percentage=0.0
                )
                db.session.add(stats)
            
            stats.total_games_played = (stats.total_games_played or 0) + 1
            stats.total_correct_guesses = (stats.total_correct_guesses or 0) + correct_count
            stats.total_guesses = (stats.total_guesses or 0) + 10
            stats.total_points = (stats.total_points or 0) + total_points
            stats.words_learned = (stats.words_learned or 0) + correct_count
            stats.accuracy_percentage = (stats.total_correct_guesses / stats.total_guesses * 100) if stats.total_guesses > 0 else 0
            
            db.session.commit()


def get_age_group(age):
    """Determine age group from age"""
    if age <= 7:
        return '5-7'
    elif age <= 12:
        return '8-12'
    else:
        return 'adult'


def get_dummy_game_stats():
    """Get comprehensive dummy statistics for dashboard"""
    return {
        'total_users': 8,
        'total_games_played': 24,
        'total_words_learned': 156,
        'average_accuracy': 68.5,
        'most_played_category': 'animals',
        'difficulty_distribution': {
            'easy': 45,
            'medium': 35,
            'hard': 20
        },
        'language_distribution': {
            'en': 80,
            'es': 20
        },
        'age_group_distribution': {
            '5-7': 15,
            '8-12': 50,
            'adult': 35
        }
    }


def get_psychology_insights():
    """Get psychology-based insights from gameplay data"""
    
    return {
        'cognitive_load': {
            'title': 'Cognitive Load Analysis',
            'description': 'How difficulty levels affect learning',
            'data': {
                'easy': {'accuracy': 85, 'average_time': 12},
                'medium': {'accuracy': 68, 'average_time': 28},
                'hard': {'accuracy': 45, 'average_time': 42}
            }
        },
        'learning_plateau': {
            'title': 'Learning Plateau Detection',
            'description': 'Users may plateau after 3-4 sessions',
            'threshold_games': 4,
            'recommendation': 'Increase difficulty or introduce new categories'
        },
        'motivation_patterns': {
            'title': 'Motivation Patterns',
            'description': 'Peak engagement times and drop-off points',
            'peak_time': '14:00-16:00',
            'retention_rate': '62%'
        },
        'visual_recognition': {
            'title': 'Visual Recognition Improvement',
            'description': 'How visual cues improve word retention',
            'with_images': 75,
            'without_images': 45
        },
        'multilingual_advantage': {
            'title': 'Bilingual Learning Benefits',
            'description': 'Bilingual players show better retention',
            'monolingual_accuracy': 65,
            'bilingual_accuracy': 78
        }
    }

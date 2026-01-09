from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    preferred_language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    game_sessions = db.relationship('GameSession', backref='user', lazy=True)
    stats = db.relationship('UserStats', backref='user', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class GameSession(db.Model):
    """Game session model"""
    __tablename__ = 'game_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age_group = db.Column(db.String(20))  # '5-7', '8-12', 'adult'
    difficulty = db.Column(db.String(20))  # 'easy', 'medium', 'hard'
    language = db.Column(db.String(10), default='en')
    total_rounds = db.Column(db.Integer, default=10)
    started_at = db.Column(db.DateTime, default=datetime.now)
    ended_at = db.Column(db.DateTime)
    
    # Relationships
    rounds = db.relationship('Round', backref='session', lazy=True)
    
    def __repr__(self):
        return f'<GameSession {self.id} - User {self.user_id}>'


class Round(db.Model):
    """Round model"""
    __tablename__ = 'rounds'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('game_sessions.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    round_number = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    started_at = db.Column(db.DateTime, default=datetime.now)
    guessed_at = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer, default=60)
    is_guessed = db.Column(db.Boolean, default=False)
    guesses_count = db.Column(db.Integer, default=0)
    points_earned = db.Column(db.Integer, default=0)
    
    # Relationships
    word = db.relationship('Word', backref='rounds')
    guesses = db.relationship('Guess', backref='round', lazy=True)
    
    def __repr__(self):
        return f'<Round {self.id}>'


class Word(db.Model):
    """Word model"""
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)
    definition = db.Column(db.Text)
    translation = db.Column(db.String(100))  # Translation in another language
    difficulty = db.Column(db.String(20))  # 'easy', 'medium', 'hard'
    category = db.Column(db.String(50))  # 'animals', 'objects', 'actions', etc.
    age_group = db.Column(db.String(20))  # '5-7', '8-12', 'adult'
    is_appropriate = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Word {self.word}>'


class Guess(db.Model):
    """Guess model"""
    __tablename__ = 'guesses'
    
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'), nullable=False)
    user_guess = db.Column(db.String(100))
    is_correct = db.Column(db.Boolean, default=False)
    match_type = db.Column(db.String(20))  # 'exact', 'fuzzy', 'synonym'
    time_taken = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Guess {self.id}>'


class UserStats(db.Model):
    """User statistics model"""
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    total_games_played = db.Column(db.Integer, default=0)
    total_guesses = db.Column(db.Integer, default=0)
    total_correct_guesses = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    accuracy_percentage = db.Column(db.Float, default=0.0)
    words_learned = db.Column(db.Integer, default=0)
    average_time_per_guess = db.Column(db.Float, default=0.0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<UserStats {self.user_id}>'

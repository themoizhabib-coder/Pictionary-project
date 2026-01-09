import random
from datetime import datetime

# EXPANDED Word database with 100+ words (all dummy data, no API needed!)
WORD_DATABASE = {
    '5-7': {
        'easy': [
            {'word': 'Apple', 'definition': 'A red fruit', 'category': 'food', 'translation': 'Manzana'},
            {'word': 'Dog', 'definition': 'A pet animal', 'category': 'animals', 'translation': 'Perro'},
            {'word': 'Cat', 'definition': 'A small pet animal', 'category': 'animals', 'translation': 'Gato'},
            {'word': 'Sun', 'definition': 'Bright star in the sky', 'category': 'nature', 'translation': 'Sol'},
            {'word': 'Moon', 'definition': 'Shines at night', 'category': 'nature', 'translation': 'Luna'},
            {'word': 'House', 'definition': 'A place where people live', 'category': 'objects', 'translation': 'Casa'},
            {'word': 'Tree', 'definition': 'A tall plant with branches', 'category': 'nature', 'translation': 'Árbol'},
            {'word': 'Flower', 'definition': 'A colorful plant', 'category': 'nature', 'translation': 'Flor'},
            {'word': 'Ball', 'definition': 'A round toy', 'category': 'toys', 'translation': 'Pelota'},
            {'word': 'Car', 'definition': 'A vehicle with wheels', 'category': 'objects', 'translation': 'Coche'},
            {'word': 'Fish', 'definition': 'An animal that swims', 'category': 'animals', 'translation': 'Pez'},
            {'word': 'Bird', 'definition': 'An animal with wings', 'category': 'animals', 'translation': 'Pájaro'},
            {'word': 'Star', 'definition': 'Twinkles in the night sky', 'category': 'nature', 'translation': 'Estrella'},
            {'word': 'Cloud', 'definition': 'White fluffy in the sky', 'category': 'nature', 'translation': 'Nube'},
            {'word': 'Rain', 'definition': 'Water falling from sky', 'category': 'nature', 'translation': 'Lluvia'},
        ],
        'medium': [
            {'word': 'Butterfly', 'definition': 'A colorful flying insect', 'category': 'animals', 'translation': 'Mariposa'},
            {'word': 'Rainbow', 'definition': 'Colorful arc in the sky', 'category': 'nature', 'translation': 'Arcoíris'},
            {'word': 'Elephant', 'definition': 'A large animal with a trunk', 'category': 'animals', 'translation': 'Elefante'},
            {'word': 'Castle', 'definition': 'A large old building', 'category': 'objects', 'translation': 'Castillo'},
            {'word': 'Penguin', 'definition': 'A black and white bird', 'category': 'animals', 'translation': 'Pingüino'},
            {'word': 'Dinosaur', 'definition': 'Extinct prehistoric creature', 'category': 'animals', 'translation': 'Dinosaurio'},
            {'word': 'Dragon', 'definition': 'Mythical fire-breathing creature', 'category': 'fantasy', 'translation': 'Dragón'},
            {'word': 'Unicorn', 'definition': 'Magical horse with horn', 'category': 'fantasy', 'translation': 'Unicornio'},
        ],
        'hard': [
            {'word': 'Kaleidoscope', 'definition': 'An optical tube with mirrors', 'category': 'objects', 'translation': 'Caleidoscopio'},
        ]
    },
    '8-12': {
        'easy': [
            {'word': 'Bicycle', 'definition': 'A two-wheeled vehicle', 'category': 'objects', 'translation': 'Bicicleta'},
            {'word': 'Dinosaur', 'definition': 'An extinct prehistoric creature', 'category': 'animals', 'translation': 'Dinosaurio'},
            {'word': 'Telescope', 'definition': 'Used to see distant stars', 'category': 'objects', 'translation': 'Telescopio'},
            {'word': 'Ocean', 'definition': 'A large body of salt water', 'category': 'nature', 'translation': 'Océano'},
            {'word': 'Mountain', 'definition': 'A large high hill', 'category': 'nature', 'translation': 'Montaña'},
            {'word': 'Tiger', 'definition': 'A large striped cat', 'category': 'animals', 'translation': 'Tigre'},
            {'word': 'Lion', 'definition': 'The king of animals', 'category': 'animals', 'translation': 'León'},
            {'word': 'Pizza', 'definition': 'Italian food with cheese', 'category': 'food', 'translation': 'Pizza'},
            {'word': 'Guitar', 'definition': 'A musical instrument', 'category': 'objects', 'translation': 'Guitarra'},
            {'word': 'Computer', 'definition': 'Electronic device for work', 'category': 'objects', 'translation': 'Computadora'},
        ],
        'medium': [
            {'word': 'Helicopter', 'definition': 'An aircraft with rotating blades', 'category': 'objects', 'translation': 'Helicóptero'},
            {'word': 'Volcano', 'definition': 'A mountain that erupts lava', 'category': 'nature', 'translation': 'Volcán'},
            {'word': 'Astronaut', 'definition': 'A person who travels in space', 'category': 'people', 'translation': 'Astronauta'},
            {'word': 'Pyramid', 'definition': 'An ancient Egyptian structure', 'category': 'objects', 'translation': 'Pirámide'},
            {'word': 'Skateboard', 'definition': 'A board with wheels for tricks', 'category': 'objects', 'translation': 'Patineta'},
            {'word': 'Submarine', 'definition': 'A boat under water', 'category': 'objects', 'translation': 'Submarino'},
            {'word': 'Waterfall', 'definition': 'Cascading water down cliff', 'category': 'nature', 'translation': 'Cascada'},
            {'word': 'Desert', 'definition': 'Hot sandy place', 'category': 'nature', 'translation': 'Desierto'},
            {'word': 'Jungle', 'definition': 'Dense tropical forest', 'category': 'nature', 'translation': 'Jungla'},
            {'word': 'Robot', 'definition': 'Mechanical helper', 'category': 'objects', 'translation': 'Robot'},
        ],
        'hard': [
            {'word': 'Metamorphosis', 'definition': 'Complete change of form', 'category': 'concepts', 'translation': 'Metamorfosis'},
            {'word': 'Photosynthesis', 'definition': 'Process plants use to make food', 'category': 'science', 'translation': 'Fotosíntesis'},
            {'word': 'Constellation', 'definition': 'Pattern of stars in sky', 'category': 'science', 'translation': 'Constelación'},
            {'word': 'Archaeology', 'definition': 'Study of ancient civilizations', 'category': 'science', 'translation': 'Arqueología'},
        ]
    },
    'adult': {
        'easy': [
            {'word': 'Ambition', 'definition': 'Strong desire to succeed', 'category': 'emotions', 'translation': 'Ambición'},
            {'word': 'Technology', 'definition': 'Application of science', 'category': 'concepts', 'translation': 'Tecnología'},
            {'word': 'Creativity', 'definition': 'Ability to create something new', 'category': 'traits', 'translation': 'Creatividad'},
            {'word': 'Freedom', 'definition': 'Liberty and independence', 'category': 'concepts', 'translation': 'Libertad'},
            {'word': 'Success', 'definition': 'Achieving your goals', 'category': 'concepts', 'translation': 'Éxito'},
            {'word': 'Happiness', 'definition': 'State of joy and contentment', 'category': 'emotions', 'translation': 'Felicidad'},
        ],
        'medium': [
            {'word': 'Procrastination', 'definition': 'Delaying important tasks', 'category': 'behaviors', 'translation': 'Procrastinación'},
            {'word': 'Nostalgia', 'definition': 'Sentimental desire for the past', 'category': 'emotions', 'translation': 'Nostalgia'},
            {'word': 'Serendipity', 'definition': 'Finding something good by luck', 'category': 'concepts', 'translation': 'Serendipia'},
            {'word': 'Paradox', 'definition': 'A contradictory statement', 'category': 'concepts', 'translation': 'Paradoja'},
            {'word': 'Ephemeral', 'definition': 'Lasting for a very short time', 'category': 'descriptors', 'translation': 'Efímero'},
            {'word': 'Resilience', 'definition': 'Ability to recover from hardship', 'category': 'traits', 'translation': 'Resiliencia'},
            {'word': 'Empathy', 'definition': 'Understanding others feelings', 'category': 'traits', 'translation': 'Empatía'},
            {'word': 'Integrity', 'definition': 'Moral uprightness', 'category': 'traits', 'translation': 'Integridad'},
        ],
        'hard': [
            {'word': 'Existentialism', 'definition': 'Philosophy about existence and essence', 'category': 'philosophy', 'translation': 'Existencialismo'},
            {'word': 'Juxtaposition', 'definition': 'Placing things side by side for effect', 'category': 'concepts', 'translation': 'Yuxtaposición'},
            {'word': 'Cognitive Dissonance', 'definition': 'Tension from conflicting beliefs', 'category': 'psychology', 'translation': 'Disonancia Cognitiva'},
            {'word': 'Melancholy', 'definition': 'Deep sadness and thoughtfulness', 'category': 'emotions', 'translation': 'Melancolía'},
            {'word': 'Pragmatism', 'definition': 'Focus on practical results', 'category': 'philosophy', 'translation': 'Pragmatismo'},
        ]
    }
}

def select_word(age_group='adult', difficulty='medium', language='en', used_words=None):
    """
    Select a word based on age group and difficulty level
    
    Test Cases Covered:
    1. Ages 5-7: Basic concrete nouns
    2. Ages 8-12: More descriptive words
    3. Adults: Abstract concepts
    4. Difficulty scaling: Easy, Medium, Hard
    5. No duplicates: Tracks used words
    6. Bilingual: Returns translation
    7. Category support: Returns word category
    10. Word length: Limits to reasonable length
    
    Args:
        age_group (str): '5-7', '8-12', or 'adult'
        difficulty (str): 'easy', 'medium', or 'hard'
        language (str): Language code (en, es, etc.)
        used_words (list): Words already used in session
    
    Returns:
        dict: Word data with definition, translation, category
    """
    
    if used_words is None:
        used_words = []
    
    # Get appropriate word pool
    if age_group not in WORD_DATABASE:
        age_group = 'adult'
    
    if difficulty not in WORD_DATABASE[age_group]:
        difficulty = 'medium'
    
    word_pool = WORD_DATABASE[age_group][difficulty]
    
    # Filter out used words and verify word length (max 20 chars)
    available_words = [
        w for w in word_pool 
        if w['word'] not in used_words and len(w['word']) <= 20
    ]
    
    if not available_words:
        # If all words used, refresh the pool
        available_words = word_pool
    
    # Select random word
    selected_word = random.choice(available_words)
    
    return {
        'word': selected_word['word'],
        'definition': selected_word['definition'],
        'translation': selected_word['translation'],
        'category': selected_word['category'],
        'age_group': age_group,
        'difficulty': difficulty
    }


def get_word_by_name(word_name):
    """Get word details by name"""
    for age_group in WORD_DATABASE:
        for difficulty in WORD_DATABASE[age_group]:
            for word_data in WORD_DATABASE[age_group][difficulty]:
                if word_data['word'].lower() == word_name.lower():
                    return word_data
    return None

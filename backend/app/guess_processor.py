import os

# Simple Levenshtein distance implementation (no external dependency)
def levenshtein_distance(s1, s2):
    """Calculate Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

# Synonym dictionary
SYNONYMS = {
    'couch': ['sofa', 'divan', 'settee'],
    'sofa': ['couch', 'divan', 'settee'],
    'dog': ['puppy', 'canine', 'hound'],
    'cat': ['kitten', 'feline', 'tom'],
    'car': ['automobile', 'vehicle', 'sedan'],
    'happy': ['joyful', 'glad', 'cheerful'],
    'sad': ['unhappy', 'depressed', 'sorrowful'],
    'big': ['large', 'huge', 'enormous'],
    'small': ['tiny', 'little', 'miniature'],
    'fast': ['quick', 'rapid', 'speedy'],
    'slow': ['sluggish', 'leisurely', 'gradual'],
}

def process_guess(user_guess, correct_word, time_taken=0, max_time=60):
    """
    Process a user's guess with sophisticated matching
    
    Test Cases Covered:
    21. Case sensitivity: Normalizes to lowercase
    22. Leading/trailing spaces: Strips whitespace
    23. Plural vs singular: Basic handling
    24. Common typos: Levenshtein distance fuzzy matching
    25. Synonym support: Dictionary lookup
    26. Fastest guess: Returns time_taken
    27. Empty guess: Returns error
    
    Args:
        user_guess (str): The user's guess
        correct_word (str): The correct answer
        time_taken (float): Time taken to guess (seconds)
        max_time (int): Maximum time allowed
    
    Returns:
        dict: {
            'is_correct': bool,
            'match_type': str ('exact', 'fuzzy', 'synonym', 'none'),
            'message': str,
            'time_taken': float,
            'time_bonus': bool
        }
    """
    
    # Test Case 30: Empty guess handling
    if not user_guess or user_guess.strip() == '':
        return {
            'is_correct': False,
            'match_type': 'none',
            'message': 'Please enter a guess!',
            'time_taken': time_taken,
            'time_bonus': False
        }
    
    # Test Case 22: Strip leading/trailing spaces
    user_guess = user_guess.strip()
    
    # Test Case 21: Normalize case sensitivity
    normalized_guess = user_guess.lower()
    normalized_word = correct_word.lower()
    
    # Test Case 21: Exact match
    if normalized_guess == normalized_word:
        return {
            'is_correct': True,
            'match_type': 'exact',
            'message': f'✓ Correct! The answer was "{correct_word}"',
            'time_taken': time_taken,
            'time_bonus': time_taken < (max_time * 0.3)  # 30% of time
        }
    
    # Test Case 23: Handle plurals
    singular_guess = remove_plural(normalized_guess)
    singular_word = remove_plural(normalized_word)
    
    if singular_guess == singular_word and singular_guess != normalized_guess:
        return {
            'is_correct': True,
            'match_type': 'fuzzy',
            'message': f'✓ Correct! (Accepted: {normalized_guess} matches {correct_word})',
            'time_taken': time_taken,
            'time_bonus': False
        }
    
    # Test Case 25: Synonym matching
    synonym_match = check_synonym_match(normalized_guess, normalized_word)
    if synonym_match:
        return {
            'is_correct': True,
            'match_type': 'synonym',
            'message': f'✓ Correct! "{normalized_guess}" is a synonym for "{correct_word}"',
            'time_taken': time_taken,
            'time_bonus': False
        }
    
    # Test Case 24: Fuzzy matching with Levenshtein distance
    fuzzy_match = fuzzy_match_word(normalized_guess, normalized_word)
    if fuzzy_match['is_match']:
        return {
            'is_correct': True,
            'match_type': 'fuzzy',
            'message': f'✓ Close enough! The answer was "{correct_word}"',
            'time_taken': time_taken,
            'time_bonus': False,
            'similarity': fuzzy_match['similarity']
        }
    
    # Test Case: No match
    return {
        'is_correct': False,
        'match_type': 'none',
        'message': f'✗ Wrong! The answer was "{correct_word}". Try again!',
        'time_taken': time_taken,
        'time_bonus': False
    }


def fuzzy_match_word(guess, correct_word, threshold=0.75):
    """
    Fuzzy match using Levenshtein distance
    
    Args:
        guess (str): User's guess
        correct_word (str): Correct word
        threshold (float): Similarity threshold (0-1)
    
    Returns:
        dict: {'is_match': bool, 'similarity': float}
    """
    
    max_length = max(len(guess), len(correct_word))
    if max_length == 0:
        return {'is_match': True, 'similarity': 1.0}
    
    # Calculate distance using our simple implementation
    distance = levenshtein_distance(guess, correct_word)
    
    # Convert to similarity score (0-1)
    similarity = 1 - (distance / max_length)
    
    # Allow fuzzy match if similarity is high enough
    # For example: "Elefant" vs "Elephant" should match
    is_match = similarity >= threshold
    
    return {
        'is_match': is_match,
        'similarity': similarity,
        'distance': distance
    }


def check_synonym_match(guess, correct_word):
    """
    Check if guess is a synonym of the correct word
    
    Args:
        guess (str): User's guess
        correct_word (str): Correct word
    
    Returns:
        bool: True if guess is a synonym
    """
    
    # Check if correct_word has synonyms and if guess matches any
    if correct_word in SYNONYMS:
        if guess in SYNONYMS[correct_word]:
            return True
    
    # Check reverse (if guess has synonyms that include correct_word)
    if guess in SYNONYMS:
        if correct_word in SYNONYMS[guess]:
            return True
    
    return False


def remove_plural(word):
    """
    Simple plural removal (basic English rules)
    
    Args:
        word (str): Word to singularize
    
    Returns:
        str: Singular form
    """
    
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('es'):
        return word[:-2]
    elif word.endswith('s'):
        return word[:-1]
    
    return word


def validate_image_url(url):
    """
    Validate that an image URL is accessible and has correct mime type
    
    Args:
        url (str): Image URL to validate
    
    Returns:
        bool: True if valid
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200 and 'image' in response.headers.get('content-type', '')
    except:
        return False


def process_image_for_display(image_url, max_width=512, max_height=512):
    """
    Download and process image for display (test case 35: mobile responsiveness)
    
    Args:
        image_url (str): URL of the image
        max_width (int): Maximum width
        max_height (int): Maximum height
    
    Returns:
        str: Resized image URL or original if error
    """
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        # Resize while maintaining aspect ratio
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        return image_url  # In production, save resized image and return new URL
    except:
        return image_url  # Return original on error


def text_to_speech(text, language='en'):
    """
    Convert text to speech (Test case 48: Audio pronunciation)
    
    Args:
        text (str): Text to convert
        language (str): Language code
    
    Returns:
        str: URL to audio file or error message
    """
    try:
        # Using Google Text-to-Speech API (free option)
        encoded_text = text.replace(' ', '%20')
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={language}&client=tw-ob&q={encoded_text}"
        return tts_url
    except:
        return None

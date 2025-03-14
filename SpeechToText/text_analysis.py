import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from string import punctuation
import re

def analyze_text(text):
    """Analyze text and return various insights."""
    if not text.strip():
        return {
            'error': 'Empty text provided'
        }

    # Basic text statistics
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    word_count = len([word for word in words if word.isalnum()])
    
    # Remove stopwords and punctuation for key phrases
    stop_words = set(stopwords.words('english'))
    words_no_stop = [word for word in words 
                     if word.isalnum() and word not in stop_words]
    
    # Get key phrases (most common words)
    word_freq = Counter(words_no_stop)
    key_phrases = word_freq.most_common(5)
    
    # Calculate average sentence length
    avg_sentence_length = word_count / len(sentences) if sentences else 0
    
    # Sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    
    # Determine overall sentiment
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        sentiment = 'Positive'
    elif compound_score <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    # Calculate readability (Flesch Reading Ease approximation)
    total_syllables = sum(count_syllables(word) for word in words_no_stop)
    if word_count > 0 and len(sentences) > 0:
        flesch_score = 206.835 - 1.015 * (word_count / len(sentences)) - 84.6 * (total_syllables / word_count)
    else:
        flesch_score = 0
        
    # Get reading level
    reading_level = get_reading_level(flesch_score)
    
    # Structure analysis
    structure = analyze_structure(text)
    
    return {
        'statistics': {
            'sentences': len(sentences),
            'words': word_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'readability_score': round(flesch_score, 1),
            'reading_level': reading_level
        },
        'key_phrases': [{'phrase': phrase, 'count': count} for phrase, count in key_phrases],
        'sentiment': {
            'overall': sentiment,
            'scores': {
                'positive': round(sentiment_scores['pos'] * 100, 1),
                'neutral': round(sentiment_scores['neu'] * 100, 1),
                'negative': round(sentiment_scores['neg'] * 100, 1)
            }
        },
        'structure': structure
    }

def count_syllables(word):
    """Approximate syllable count."""
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count += 1
    return count

def get_reading_level(score):
    """Convert Flesch score to reading level."""
    if score >= 90:
        return 'Very Easy'
    elif score >= 80:
        return 'Easy'
    elif score >= 70:
        return 'Fairly Easy'
    elif score >= 60:
        return 'Standard'
    elif score >= 50:
        return 'Fairly Difficult'
    elif score >= 30:
        return 'Difficult'
    else:
        return 'Very Difficult'

def analyze_structure(text):
    """Analyze the structure of the text."""
    # Split into paragraphs
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    # Identify potential sections
    sections = []
    current_section = {'title': 'Main Content', 'content': []}
    
    for para in paragraphs:
        # Check if paragraph might be a header (short, ends without period)
        if len(para) < 50 and not para.endswith('.'):
            if current_section['content']:
                sections.append(current_section)
            current_section = {'title': para, 'content': []}
        else:
            current_section['content'].append(para)
    
    if current_section['content']:
        sections.append(current_section)
    
    return {
        'paragraphs': len(paragraphs),
        'sections': sections if len(sections) > 1 else None
    }

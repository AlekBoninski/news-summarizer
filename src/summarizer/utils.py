import re
from nltk.tokenize import sent_tokenize, word_tokenize

from common import Document, Sentence

QUANTITY_ABBREVIATIONS = re.compile(r'(?<=[\s\d/])(млн|хил|г|год|гр|кг|лв|лв|ст|ч|км)\.')
ABBREVIATIONS = re.compile(r'(?<!\w)(изп|гр|ул|бул|обл|нар|Св|св|бр|чл|ал|нк)\.')

def load_stopwords_bg():
    stopwords_file = open('resources/stopwords/bulgarian')
    stopwords_file_content = stopwords_file.read()
    return set(stopwords_file_content.split('\n'))

def tokenize_sentence(sentence):
    words = word_tokenize(sentence)

    return Sentence(words, sentence)

def tokenize_text(text):
    sentences = sent_tokenize(text)

    return Document([tokenize_sentence(s) for s in sentences], text)

def calculate_word_frequency(
        words,
        exclude_stopwords=False,
        exclude_numbers=True
    ):
    from string import punctuation
    punctuation = punctuation + '\n\'\'``'
    stopwords = set()
    if not exclude_stopwords:
        stopwords = load_stopwords_bg()
    word_histogram = {}
    for word in words:
        word_lower = word.lower()
        if word_lower in punctuation:
            continue
        if not exclude_stopwords and word_lower in stopwords:
            continue
        if exclude_numbers and re.match(r'(?<!\w)\d+(?!\w)', word_lower):
            continue
        if word_lower in word_histogram:
            word_histogram[word_lower] += 1
        else:
            word_histogram[word_lower] = 1

    return word_histogram

def filter_text(text):
    bulgarian_filters = [
        lambda text: QUANTITY_ABBREVIATIONS.sub(r'\1 ', text),
        lambda text: ABBREVIATIONS.sub(r'\1 ', text),
        lambda text: text.replace(' т.е.', 'т-е'),
        lambda text: text.replace('в т.ч.', 'в т-ч')
    ]

    filtered = text
    for f in bulgarian_filters:
        filtered = f(filtered)
    return filtered
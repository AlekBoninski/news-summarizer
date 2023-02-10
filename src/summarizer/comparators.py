from collections import OrderedDict
from nltk.tokenize import word_tokenize
import numpy as np

from summarizer.utils import calculate_word_frequency


class CosineSimilariryComparator:

    def __init__(self, source, target):
        source_words = word_tokenize(source)
        target_words = word_tokenize(target)
        self.source_words_freq = calculate_word_frequency(source_words)
        self.target_words_freq = calculate_word_frequency(target_words)

    def similarity(self):
        source_vector = self.__build_vector_base()
        target_vector = self.__build_vector_base()
        for word, freq in self.source_words_freq.items():
            word_lower = word.lower()
            if word_lower not in source_vector:
                raise 'Unable to build text vector: Word in text not in base vector!'
            source_vector[word_lower] += freq
        for word, freq in self.target_words_freq.items():
            word_lower = word.lower()
            if word_lower not in target_vector:
                raise 'Unable to build text vector: Word in text not in base vector!'
            target_vector[word_lower] += freq

        source_vector = list(source_vector.values())
        target_vector = list(target_vector.values())

        cosine_similarity = np.dot(source_vector, target_vector) / (np.sqrt(np.sum(np.square(source_vector))) * np.sqrt(np.sum(np.square(target_vector))))
        return cosine_similarity

    def __build_vector_base(self):
        vector_base = OrderedDict()
        for word in self.source_words_freq.keys():
            vector_base[word.lower()] = 0
        for word in self.target_words_freq.keys():
            vector_base[word.lower()] = 0
        return vector_base

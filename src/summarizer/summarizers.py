from nltk.tokenize import word_tokenize, sent_tokenize
from common import SummarizedArticle
from summarizer.summary_builder import SummaryBuilder
from summarizer.utils import calculate_word_frequency

class FrequencySummarizer:
    def __init__(self, article):
        self.title = article.title
        self.words = word_tokenize(article.text)
        self.sentences = sent_tokenize(article.text)
        self.word_frequency = {}
        self.sentence_scores = {}

    def summarize(self, ratio=0.3):
        self.word_frequency = calculate_word_frequency(self.words)
        self.__calculate_sentence_scores()
        
        summary_sentence_length = max(1, int(len(self.sentences) * ratio))
        summary_builder = SummaryBuilder(summary_sentence_length)
        for sentence in self.sentences:
            summary_builder.add_sentence(sentence, self.sentence_scores[sentence])

        summary = summary_builder.build()

        return SummarizedArticle(self.title, self.sentences, summary)

    def __calculate_sentence_scores(self):
        for sentence in self.sentences:
            sentence_lower = sentence.lower()
            if sentence not in self.sentence_scores:
                self.sentence_scores[sentence] = 0
            for word, freq in self.word_frequency.items():
                if word in sentence_lower:
                    self.sentence_scores[sentence] += freq

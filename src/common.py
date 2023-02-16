class NewsArticle:

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __str__(self):
        return 'NewsArticle(title={title})'.format(title=self.title)

    def __repr__(self):
        return 'NewsArticle(title={title})'.format(title=self.title)

class Document:

    def __init__(self, sentences, original=None):
        self.sentences = sentences
        self.original = original
        self.__words = None

    @property
    def words(self):
        if self.__words is not None:
            return self.__words
        self.__words = [word for sentence in self.sentences for word in sentence.words]
        return self.__words

class Sentence:

    def __init__(self, words, original=None):
        self.words = words
        self.original = original

class SummarizedArticle:

    def __init__(self, title, original_sentences, summarized_text):
        self.title = title
        self.original_sentences = original_sentences
        self.summarized_text = summarized_text
        self.__original_text = None

    @property
    def original_text(self):
        if self.__original_text is not None:
            return self.__original_text
        return ' '.join(self.original_sentences)

    def evaluate_summary(self, comparator):
        source = self.__get_evaluation_metric()
        return comparator(source, self.summarized_text).similarity()

    def __get_evaluation_metric(self):
        return ' '.join([self.original_sentences[0], self.original_sentences[-1], self.title])

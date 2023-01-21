class NewsArticle:

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __str__(self):
        return 'NewsArticle(title={title})'.format(title=self.title)

    def __repr__(self):
        return 'NewsArticle(title={title})'.format(title=self.title)

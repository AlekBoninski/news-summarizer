import bs4, requests, re
from common import NewsArticle
from summarizer.utils import filter_text


class DnevnikCrawler:
    base_url = 'https://dnevnik.bg'
    latest_news_url = '{base_url}/novini/dnes'.format(base_url=base_url)
    article_link_selector = '.content > .site-block > .grid-container > div > article > div:not(:has(p.gallery-gridcount)) > h2 > a'
    article_title_selector = '.main-content > .content > h1'
    article_content_selector = '.article-content > p:not(:has(em))'

    def __init__(self, filter_text=True):
        self.filter_text = filter_text

    def __fetch_latest_article_links_and_titles(self, articles_to_fetch):
        latest_news_html = requests.get(self.latest_news_url).text
        soup = bs4.BeautifulSoup(latest_news_html)
        article_links = [('{base_url}{path}'.format(base_url=self.base_url, path=element.get('href')), element.text) for element in soup.select(self.article_link_selector)]
        return article_links[0:articles_to_fetch]

    def __fetch_article(self, link, fallback_title=''):
        try:
            article_html = requests.get(link).text
            soup = bs4.BeautifulSoup(article_html)
            title_element = soup.select(self.article_title_selector)
            article_content_elements = list(filter(lambda element: bool(element.text.strip()) and element.next.name != 'figure', soup.select(self.article_content_selector)))
            title = title_element[0].text if len(title_element) > 0 else fallback_title
            # Add a dot to the end of text blocks that have no punctuation marks for sentence end since this website has articles that have intermittent headings.
            text = ' '.join('{text}{dot}'.format(text=element.text, dot='' if re.match('\.|\?|!', element.text.strip()[-1]) else '. ') for element in article_content_elements)

            if self.filter_text:
                text = filter_text(text)

            return NewsArticle(title, text)
        except:
            pass

    def fetch_latest_articles(self, articles_to_fetch=10):
        article_links_and_titles = self.__fetch_latest_article_links_and_titles(articles_to_fetch)
        articles = [self.__fetch_article(link, title) for (link, title) in article_links_and_titles]
        return list(filter(lambda article: article.text.strip() != '' and article.title.strip() != '', articles))

    def fetch_article(self, article_url):
        return self.__fetch_article(article_url)

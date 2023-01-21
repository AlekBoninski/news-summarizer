import bs4, requests, re
from news_providers.common import NewsArticle


class DnevnikCrawler:
    base_url = 'https://dnevnik.bg'
    latest_news_url = '{base_url}/novini/dnes'.format(base_url=base_url)
    article_link_selector = '.content > .site-block > .grid-container > div > article > div:not(:has(p.gallery-gridcount)) > h2 > a'
    article_title_selector = '.main-content > .content > h1'
    article_content_selector = '.article-content > p'

    def __init__(self, articles_to_fetch):
        self.articles_to_fetch = articles_to_fetch

    def __fetch_latest_article_links_and_titles(self):
        latest_news_html = requests.get(self.latest_news_url).text
        soup = bs4.BeautifulSoup(latest_news_html)
        article_links = [('{base_url}{path}'.format(base_url=self.base_url, path=element.get('href')), element.text) for element in soup.select(self.article_link_selector)]
        return article_links[0:self.articles_to_fetch]

    def __fetch_article(self, link, fallback_title=''):
        # article_link = 'https://www.dnevnik.bg/bulgaria/2023/01/21/4440961_rumen_radev_oshte_sum_na_poziciiata_che_bulgariia_ne/'
        # article_link = 'https://www.dnevnik.bg/bulgaria/2023/01/21/4440940_geshev_razsledvaniiata_za_kushtata_v_barselona_i/'
        article_link = 'https://www.dnevnik.bg/evropa/2023/01/21/4435082_samo_v_edna_strana_v_evropa_horata_sa_nedovolni_ot/'
        try:
            # article_html = requests.get(link).text
            article_html = requests.get(article_link).text
            soup = bs4.BeautifulSoup(article_html)
            title_element = soup.select(self.article_title_selector)
            article_content_elements = list(filter(lambda element: bool(element.text.strip()) and element.next.name != 'figure', soup.select(self.article_content_selector)))
            first = article_content_elements[0]
            next = []
            for e in first.next_elements:
                next.append(e)
            title = title_element[0].text if len(title_element) > 0 else fallback_title
            # Add a dot to the end of text blocks that have no punctuation marks for sentence end since this website has articles that have intermittent headings.
            text = ''.join('{text}{dot}'.format(text=element.text, dot='' if re.match('\.|\?|!', element.text.strip()[-1]) else '.') for element in article_content_elements)
            return NewsArticle(title, text)
        except:
            pass


    def fetch_articles(self):
        article_links_and_titles = self.__fetch_latest_article_links_and_titles()
        articles = [self.__fetch_article(link, title) for (link, title) in article_links_and_titles]
        return articles
        

    def test(self):
        article = self.__fetch_article('')
        print(article)

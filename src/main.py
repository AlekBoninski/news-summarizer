from news_providers.dnevnik import DnevnikCrawler


crawler = DnevnikCrawler(10)
# print(crawler.fetch_articles())
crawler.test()


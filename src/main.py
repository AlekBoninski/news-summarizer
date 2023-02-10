import datetime
import json
from news_providers.dnevnik import DnevnikCrawler
from summarizer.comparators import CosineSimilariryComparator
from summarizer.summarizers import FrequencySummarizer

now = datetime.datetime.now()
print('Starting run: {}'.format(now))

crawler = DnevnikCrawler()
articles = crawler.fetch_latest_articles(5)

summaries = [FrequencySummarizer(article).summarize() for article in articles]

result = [
    { 
        'title': sa.title, 
        'original': sa.original_text, 
        'summary': sa.summarized_text,
        'score': sa.evaluate_summary(CosineSimilariryComparator)
    } for sa in summaries
]


with open('out/{}.json'.format(now), 'w') as f:
    json.dump(result, f, ensure_ascii=False)

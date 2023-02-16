import datetime
from news_providers.dnevnik import DnevnikCrawler
from summarizer.comparators import CosineSimilariryComparator
from summarizer.summarizers import FrequencySummarizer, LexRankSummarizer, LuhnSummarizer
import matplotlib.pyplot as plt

now = datetime.datetime.now()
print('Starting run: {}'.format(now))

crawler = DnevnikCrawler()
articles = crawler.fetch_latest_articles(15)

ratios = [i / 10 for i in range(1, 8)]

results = {
    'Frequency': [],
    'LexRank': [],
    'Luhn': []
}

for ratio in ratios:
    frequency_summaries = [FrequencySummarizer(article).summarize(ratio) for article in articles]
    lexrank_summaries = [LexRankSummarizer(article).summarize(ratio) for article in articles]
    luhn_summaries = [LuhnSummarizer(article).summarize(ratio) for article in articles]

    frequency_score = sum([summary.evaluate_summary(CosineSimilariryComparator) for summary in frequency_summaries]) / len(frequency_summaries)
    lexrank_score = sum([summary.evaluate_summary(CosineSimilariryComparator) for summary in lexrank_summaries]) / len(lexrank_summaries)
    luhn_score = sum([summary.evaluate_summary(CosineSimilariryComparator) for summary in luhn_summaries]) / len(luhn_summaries)

    results['Frequency'].append((ratio, frequency_score))
    results['LexRank'].append((ratio, lexrank_score))
    results['Luhn'].append((ratio, luhn_score))

print('Num of articles: {}'.format(len(articles)))

colors = ['red', 'green', 'blue']
for label, scores in results.items():
    plt.plot([score[0] for score in scores], [score[1] for score in scores], label=label, color=colors.pop())
plt.xlabel('Ratio')
plt.ylabel('Score')
plt.legend()
plt.savefig('out/results{}.png'.format(len(articles)))

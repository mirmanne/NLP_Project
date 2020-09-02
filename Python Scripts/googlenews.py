from newsapi import NewsApiClient
import os
#import gdelt
#import query_gdelt as gd

def google_news():
	api = NewsApiClient(api_key = 'key')

	google_news_articles = []

	sources = ['the-wall-street-journal',  'abc-news', 'associated-press', 'business-insider',  'bbc-news', 'bloomberg',
	 'cbs-news', 'cnbc', 'cnn', 'daily-mail',  'fox-news', 'wired', 'time', 'the-washington-times', 'usa-today',
	  'the-washington-post', 'the-telegraph',  'the-new-york-times', 'nbc-news', 'abc-news-au', 'ansa',
	  'ary-news', 'austrailian-financial-review', 'axios', 'blasting-news-br',  'bleacher-report',  'business-insider-uk',
	  'buzzfeed', 'cbc-news', 'entertainment-weekly', 'fortune', 'four-four-two',  'google-news', 'ign', 'msnbc', 'mtv-news',
	  'national-geographic', 'national-review',  'news24', 'newsweek', 'politico', 'reuters', 'reddit-r-all', 'techcrunch', 
	  'the hill', 'the-huffington-post', 'vice-news']

	for source in sources:
		for i in range(5):
			google_news_articles.append(api.get_everything(sources = source, from_param='2019-06-13',language='en',sort_by='relevancy', page = i+1))

	k = 0
	for i in range(len(google_news_articles)):
		for article in google_news_articles[i]['articles']:
			print(article['title'])
			k += 1

	print(k)

	f = open('google_news_articles.txt', 'w')
	f.write(google_news_articles)

#google_news()



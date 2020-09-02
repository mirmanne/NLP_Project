from __future__ import print_function
from time import time
from sklearn.decomposition import NMF
from sklearn.datasets import fetch_20newsgroups


import json
import os
import gdelt
import query_gdelt
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import mysql.connector

#nltk.download('stopwords')

data = json.load(open('articles_raw.json', 'r'))

finalclean = []
for i in article_final:
    finalclean.append(clean_string(i))
def clean_string(content):
      clean1 = re.sub('[^a-zA-z]',' ', content)
      clean = clean1.lower()
      clean = clean.split()
      stem = PorterStemmer()
      clean = [stem.stem(word) for word in clean if not word in set(stopwords.words('english'))]
      clean = ' '.join(clean)
      #finalclean.append(clean)
      return clean
 
def make_matrix(words):
    maker = TfidfVectorizer(min_df = 15)
    matrixtf = maker.fit_transform(words).toarray()
    finalmatrix = pd.DataFrame(np.array(matrixtf),columns = maker.get_feature_names()) 
    return finalmatrix    

def convert_txt_to_json():

	#articles = 
	art2 = []
	art3 = []
	art4 = []
	art5 = []

	for x in articles:
		art2.append(x['articles'])

	for x in art2:
		for y in x:
			art3.append(y)


	for article in art3:
		temp = article['source']['name']
		article['source'] = article['source']['id']
		article.update({'source_name':temp})
		art4.append(article)

	with open('articles2.json', 'w') as file:
		json.dump(art4, file)

def do_sql():

	data = json.load(open('articles_raw.json', 'r'))

	db = mysql.connector.connect(host = 'localhost', user = 'root',
						 passwd = 'password', database = 'group_project', auth_plugin='mysql_native_password')

	print(db)

	cursor = db.cursor()

	k = 0
	for article in data:
		if article['content'] is not 'null': 
			print(str(k))
			s = 'INSERT INTO general_info_raw (source_id, source_name, author, title, description, url, url_to_image, published_at, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
			s1 = (article['source'],  article['source_name'], article['author'], article['title'], article['description'], article['url'], article['urlToImage'], article['publishedAt'], article['content'])
			cursor.execute(s, s1)
			k += 1

	db.commit()

	print(cursor.execute('SELECT * FROM general_info_raw'))
    
    cursor.close()
    db.close()

def clean_json():
	for i in range(len(data)):
		if(data[i]['content']) == None or 'null':
			data.pop(i)

		with open('articles.json', 'w') as file:
			json.dump(data, file)

def remove_null_content_and_description():
	new_json = []
	i = 0
	for article in data:
		if article['content'] == None or article['description'] == None:
			print('no content and/or description. popped ' + str(i))
		else:
			new_json.append(article)

		i += 1

	print(len(new_json))

	with open('articles_cleaned.json', 'w') as file:
		json.dump(new_json, file)

def remove_escape_chars():
	k = []

	i = 0

	for article in data:
		article['description'] = article['description'].replace('\\n', '').replace('\\r', '').replace('\\u', '')
		article['content'] = article['content'].replace('\\n', '').replace('\\r', '').replace('\\u', '')
		k.append(article)
		print(i)
		i+=1

	with open('articles_final.json', 'w') as file:
		json.dump(k, file)

def make_cleaned_text_json():
	a = []

	for article in data:
		a.append(article['description'] + ' ' + article['content'])

	k = []
	i = 0
	for s in a:
		print(str(i))
		k.append(clean_string(s))
		i +=1

	with open('cleaned.json', 'w') as file:
		json.dump(k, file)

def make_matrix_and_write_to_json():

	clean = json.load(open('cleaned.json', 'r'))

	matrix = make_matrix(clean)

	print(matrix)

	with open('matrix.json', 'w') as file:
		json.dump(matrix.to_json(orient = 'index'), file)
		''

def do_sql_on_string_json():
	clean = json.load(open('cleaned.json', 'r'))

	db = mysql.connector.connect(host = 'localhost', user = 'root',
						 passwd = 'password', database = 'group_project', auth_plugin='mysql_native_password')

	cursor = db.cursor()

	for s in clean:
		a = "INSERT INTO nlp_strings (string_text) VALUES ('" + s + "')"
		cursor.execute(a)

	db.commit()

import topics_extraction_with_nmf
clean = json.load(open('cleaned.json', 'r'))
topics_extraction_with_nmf.nmf(clean, 10)

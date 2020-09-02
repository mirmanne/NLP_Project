import math
import pandas as pd
import scrape_gdelt
import toolbox
import json

dataset = pd.read_csv("20150218230000.csv",  error_bad_lines=False, header = None)
dataset1 = pd.read_csv("20150218231500.export.csv",  error_bad_lines=False, header = None)
dataset2 = pd.read_csv("20150218233000.export.csv",  error_bad_lines=False, header = None)
dataset3 = pd.read_csv("20150218234500.export.csv",  error_bad_lines=False, header = None)
dataset4 = pd.read_csv("20150219000000.export.csv",  error_bad_lines=False, header = None)

url = []
def extract_url(data):
    for i in data:
        NewData = dataset[4]
        FinalData = []
        for k in NewData:
            if isinstance(k, str):
                x = k.split("\t")
                FinalData.append(x)
    for z in FinalData:
        url.append(z[8])

extract_url(dataset)

big_data = dataset.append(dataset1)
def add_to_main(data):
    big_data.append(data)

def write_urls(url):
    with open('GDELT_urls.txt', 'w') as f:
        for item in url:
            f.write("%s\n" % item)


article_texts = []
i = 0
for w in url:
    i = i + 1
    article = scrape_gdelt.GdeltArticle(w)
    text = article.results['text']
    article_texts.append(text)
    print(i)
    

article_texts_description = []
i=0;
for w in url:
    i = i + 1
    article = scrape_gdelt.GdeltArticle(w)
    text = article.results['description']
    article_texts_description.append(text)
    print(i)

article_final = []
for i in article_texts:
    if i != "":
        #x = clean_string(i)
        article_final.append(i)
        
with open('GEDLT_articles.json', 'w') as file:
	json.dump(article_final, file)


saveURL = []
count = 1
formatDigits = '0' + str(4) + 'd'
 
for url in range(0, numLinks):
 
    try:
 
        # proceed to extract the text if the url is new only
 
        if url not in saveURL:
 
            # this is a new url, so proceed
 
 
            # save the url to ensure there is no duplicate
 
            saveURL.append(url)
 
 
            # extract the text
 
            article = scrape.GdeltArticle(url)
 
            text = article.results['text']
 
 
            # save the text
 
            if text != '':
 
            # save the text
 
            savePath = 'document_' + format(count, formatDigits) + '.txt'
 
            f2 = open(savePath, 'wb')
 
            f2.write(text.encode('utf-8'))
 
            f2.close()
 
            print(count)
 
            count += 1
 
    except:
 
        continue
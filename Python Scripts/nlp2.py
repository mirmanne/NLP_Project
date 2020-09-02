import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
'''
#NLP for Group Project

datasetnlp = pd.read_csv("file_name.tsv", delimiter = '\t', quoting = 3)

for f in oslistdir():
    
'''

def load_data():
    files = os.listdir("locationoffiles")
    data = []
    for file in files:
        file1 = "locationoffiles" + file
        f1 = open(file1, 'r')
        text1 = f1.read()
        f1.close()
        
        #Append text to data
        data.append(text1)
    return data


files = os.listdir("locationoffiles")
data = []
for file in files:
    file1 = "locationoffiles" + file
    f1 = open(file1, 'r')
    text1 = f1.read()
    f1.close()
        
    #Append text to data
    data.append(text1)


#def clean_data(texts):
    #Making data useful for processing
    import re
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    
    #Take out punctuation, lowercase text, take out stop words, and apply stemming
    finalclean = []
    for i in range(len(data)):
        clean1 = re.sub('[^a-zA-z]',' ', data[i])
        clean = clean1.lower()
        clean = clean.split()
        stem = PorterStemmer()
        clean = [stem.stem(word) for word in clean if not word in set(stopwords.words('english'))]
        clean = ' '.join(clean)
        finalclean.append(clean)
        print(i)
    #return finalclean



from sklearn.feature_extraction.text import TfidfVectorizer
maker = TfidfVectorizer()
matrixtf = maker.fit_transform(finalclean).toarray()

finalmatrix = pd.DataFrame(np.array(matrixtf),columns = maker.get_feature_names())

from __future__ import print_function
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.datasets import fetch_20newsgroups


def nmf(dataset):
	n_samples = 4976
	n_features = 10568
	n_topics = 5
	n_top_words = 10

	

	t0 = time()
	print("Loading dataset and extracting TF-IDF features...")
	#dataset = fetch_20newsgroups(shuffle=True, random_state=1,
	#                             remove=('headers', 'footers', 'quotes'))

	vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,
	                             stop_words='english')
	tfidf = vectorizer.fit_transform(dataset)
	print("done in %0.3fs." % (time() - t0))

	# Fit the NMF model
	print("Fitting the NMF model with n_samples=%d and n_features=%d..."
	      % (n_samples, n_features))
	nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
	print("done in %0.3fs." % (time() - t0))

	feature_names = vectorizer.get_feature_names()

	for topic_idx, topic in enumerate(nmf.components_):
	    print("Topic #%d:" % topic_idx)
	    print(" ".join([feature_names[i]
	                    for i in topic.argsort()[:-n_top_words - 1:-1]]))
	    print()

nmf(finalclean)
#Creating .csv file. 
cleandata = open("clean_data.csv","w")
cleandata.close()

#Writing to file. 
for entries in finalclean :
    cleandata = open("clean_data.csv","a")
    cleandata.write(entries)
    cleandata.write("\n")
    cleandata.close()

'''
Topic #0:
said mean member apparatu end support second portion shaft includ

Topic #1:
case stuf tube shir tubular food sausag film horn cellulos

Topic #2:
carcass cut devic blade conveyor poultri accord meat mean bone

Topic #3:
fish cut fillet mean belli head blade bodi apparatu guid

Topic #4:
mold plate food caviti product patti meat chamber pressur open
'''





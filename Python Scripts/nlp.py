import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
def clean_string(content):
      clean1 = re.sub('[^a-zA-z]',' ', content)
      clean = clean1.lower()
      clean = clean.split()
      stem = PorterStemmer()
      clean = [stem.stem(word) for word in clean if not word in set(stopwords.words('english'))]
      clean = ' '.join(clean)
      return clean
      
 
def make_matrix(words):
    from sklearn.feature_extraction.text import TfidfVectorizer
    maker = TfidfVectorizer()
    matrixtf = maker.fit_transform(words).toarray()
    finalmatrix = pd.DataFrame(np.array(matrixtf),columns = maker.get_feature_names()) 
    return finalmatrix    
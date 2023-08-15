import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pickle
import numpy as np

vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def process_text(row):
    nltk.download('punkt')
    nltk.download('stopwords')
    ps = PorterStemmer()
    tag_pattern = re.compile(r'<.*?>')
    
    text = row.lower()
    text = tag_pattern.sub('', text)
    tokens = word_tokenize(text)
    
    filtered_tokens = [ps.stem(token) for token in tokens if token.isalpha() and token not in stopwords.words('english')]
    text = " ".join(filtered_tokens)
    vectors = vectorizer.transform([text]).toarray()
    vectors = vectors.ravel()
    #vectors_lss = vectors[0:8000]

    return vectors

from __future__ import division
import string
import math
import bs4
import requests
import pandas as pd
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
import six
import csv
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv('Book1.csv')
X = data['link1'].values
Y = data['link2'].values
l1=[]
l1.append(X)
l1.append(Y)
print(X)
print(Y)
s1=[]
u=[]
str=''
stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()
def fun1(para):
    res=requests.get(para)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    hi=soup.select('p')
    s=[]
    u=[]
    b=[]
    ac=[]
    for k in range(len(hi)):
        s.append(hi[k].getText())
    for l in range(len(s)):
        text = s[l]
        x=re.split('; |\, |\.|\n',text)
        for n in range(len(x)):
            if len(x[n])>2:
                c=stemmer.stem(x[n])

                d=lemmatiser.lemmatize(c, pos="v")
                u.append(d)
        str1 = ''.join(u)        
    return str1                
    
tokenize = lambda doc: doc.lower().split(" ")

document_0 = fun1(X[0])
document_1 =fun1(Y[0])

all_documents = [document_0, document_1]

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents
avg=[]
m={}
tf=tfidf(all_documents)
with open('SVM.csv','w') as newFile1:
    newFileWriter = csv.writer(newFile1)
    newFileWriter.writerow(['tf1','tf2'])
    newFileWriter.writerow([tf[0],tf[1]])
    
print("---------------------------------------------------------------------")
for i in range(len(tf)):
    avg.append(sum(tf[i])/len(tf))
    m[i]=avg[i]
print(avg)
key_min = max(m.keys(), key=(lambda k: m[k]))


m1=m[key_min]
l2=l1[key_min]

with open('Book2.csv','w') as newFile:
    newFileWriter = csv.writer(newFile)
    newFileWriter.writerow(['link','key'])
    newFileWriter.writerow([m1,l2[0]])
    

sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
sklearn_representation = sklearn_tfidf.fit_transform(all_documents)
def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

tfidf_representation = tfidf(all_documents)
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
    for count_1, doc_1 in enumerate(tfidf_representation):
        our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))

skl_tfidf_comparisons = []
for count_0, doc_0 in enumerate(sklearn_representation.toarray()):
    for count_1, doc_1 in enumerate(sklearn_representation.toarray()):
        skl_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))

for x in zip(sorted(our_tfidf_comparisons, reverse = True), sorted(skl_tfidf_comparisons, reverse = True)):
    print(x)




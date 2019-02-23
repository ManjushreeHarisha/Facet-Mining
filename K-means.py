from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import bs4
import requests
import pandas as pd
data = pd.read_csv('Book2.csv')
X = data['key'].values

print(X)

def fun2(para):
    res=requests.get(para)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    hi=soup.select('p')
    s=[]
    u=[]
    b=[]
    ac=[]
    for k in range(len(hi)):
        s.append(hi[k].getText())
    return s


def clu(documents):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)
    model = KMeans(n_clusters=len(documents), init='k-means++', max_iter=len(documents), n_init=1)
    model.fit(X)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]

    terms2=[]
    string=""
    term_dict={}
    terms = vectorizer.get_feature_names()
    string=' '.join(terms)
    f = open('helloworld.txt','w')
    f.write(string)
    f.close()

    for i in range(len(documents)):
        print("Cluster %d:" % i),
        terms1=[]
        for ind in order_centroids[i, :3]:
            print(terms[ind])
    #print("--------------------------------------------------------------------------------------------------------------------")   

print("1##############################################################11111111")
documents=fun2(X[0])
clu(documents)








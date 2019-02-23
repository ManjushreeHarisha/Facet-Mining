import bs4
import requests
import nltk
from textblob import TextBlob
import re
import six
import math
import csv
from collections import Counter
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tkinter import *


def callback():
    
    try:
        from googlesearch import search
    except ImportError: 
        print("No module named 'google' found")
    count=0
    # to search
    query=e.get()
    a=[]
    for j in search(query, tld="co.in", num=2, stop=1, pause=2):
        a.append(j)
        print(j)
        count=count+1

    res2_len=[]
      


        
    #https://stackoverflow.com/questions/24153519/how-to-read-html-from-a-url-in-python-3
    def fun1(para):
        stemmer = PorterStemmer()
        lemmatiser = WordNetLemmatizer()
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
                c=stemmer.stem(x[n])
                d=lemmatiser.lemmatize(c, pos="v")
                a=TextBlob(d)
                b=a.tags
                
                for i in b:
                    if i[1]=='NN':
                        u.append(i[0])
        result=[]
        res2=[]
        dict1={}
        for i in range(len(u)):
            result.append(u[i].isalpha())
            dict1[u[i]]=result[i]
        for k, v in six.iteritems(dict1):
            if v==True:
                if len(k)>2:
                    res2.append(k)
        res2_len.append(len(res2))
        return res2






    all_list=[]
    for k in range(count):
        all_list.append(fun1(a[k]))


    best={}


    similarity=[]
    def counter_cosine_similarity(c1,c2):
            terms = set(c1).union(c2)
            dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
            magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
            magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
            similarity.append(dotprod / (magA * magB))
            return similarity
    sim1=[]
    dict2={}
    k=0

    for i in range(len(all_list)):
        for j in range(i + 1, len(all_list)):
            res2_len.append(len(all_list[i])+len(all_list[j]))
            
            counterA = Counter(all_list[i])
            counterB = Counter(all_list[j])
            sim1=counter_cosine_similarity(counterA,counterB)
            best[sim1[i]]=i,j
            k=k+1
        
            


    key_min = max(best.keys(), key=(lambda k: best[k]))


    i,j=best[key_min]
    link1=a[i]
    link2=a[j]
    print("BEST LINK: WITH LEAST SIMILARITY")
    print(link1)
    print(link2)


    with open('Book1.csv','w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['link1','link2'])
        newFileWriter.writerow([link1,link2])
        
        
    with open('webmine.csv','w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['Combination','Similarity in %','word_count'])
        for i in range(len(sim1)):
            h="C"+str(i)
            newFileWriter.writerow([h,sim1[i],res2_len[i]])
        

   
        

      

    

master = Tk()

e = Entry(master)
e.pack()

e.focus_set()



b = Button(master, text="get", width=10, command=callback)
b.pack()
e = Entry(master, width=50)
e.pack()

text = e.get()
mainloop()

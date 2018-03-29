# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 22:37:26 2018

@author: jiyuxin
"""
import json

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def delete_punctuation():
    chardigit='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' 
    with open('D:/项目/newjson/test.json','r') as f:
       lines = json.loads(f.read())
       list = []

    for line in lines: 
        for ch in line: 

            if ch in chardigit: 

                list.append(ch) 
    print("starting..")
    with open('D:/项目/newjson/test.json','w') as write:
        json.dump(list,write)
    print("successed")
    
def delete_stopping_word():
    with open('D:/项目/资料/MEDICAL/topapp_review.json','r') as f:
       lines = json.loads(f.read())
    list = []
    stop_words = stopwords.words('english')
    for line in lines:
       clean = [word for word in line.split() if word not in stop_words]
       list.append(clean)
    print("starting..")
    with open('D:/项目/newjson/test.json','w') as write:
        json.dump(list,write)
    print("successed")
    
def stemming():
    with open('D:/项目/newjson/test.json','r') as f:
       lines = json.loads(f.read())
    ps = PorterStemmer()
    list = []
    for line in lines:
        list.append(ps.stem(line))
    print("starting..")    
    with open('D:/项目/newjson/test.json','w') as write:
        json.dump(list,write)
    print("successed")
def main():
    
    delete_stopping_word()
    delete_punctuation()

if __name__ == "__main__":
    main()
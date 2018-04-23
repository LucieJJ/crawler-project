# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 05:08:57 2018

@author: jiyuxin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 22:37:26 2018

@author: jiyuxin
"""
import json
import string
import re
from time import sleep
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def delete_punctuation(address):
    with open(address,'r') as f:
       List = json.loads(f.read())
    punc = string.punctuation
    #print(List)
    new_list = []

    for line in List: 
        if line not in punc:
            new_list.append(line) 

                
    print("starting..")
    with open(address,'w') as write:
        json.dump(new_list,write)
    print("successed")
    
def delete_stopping_word(address):
    with open(address,'r') as f:
       List = json.loads(f.read())
    newlist = []
    stop_words = stopwords.words('english')
    for line in List:
       #clean = [word for word in line.split() if word not in stop_words]
       if line not in stop_words:
           newlist.append(line)
    print("starting..")
    with open(address,'w') as write:
        json.dump(newlist,write)
    print("successed")
    
def stemming(address,list):
    
    ps = PorterStemmer()
    newlist = []
    for line in list:
        words = word_tokenize(line)
        for w in words:
                newlist.append(ps.stem(w))
    print("starting..")    
    with open(address,'w') as write:
        json.dump(newlist,write)
    print("successed")
def main():
    addressID = 'D:/项目/资料/MEDICAL/topapp_appid.json'
    addressR = 'D:/项目/资料/MEDICAL/topapp_review.json'
    addressTrans = 'D:/项目/newjson/test.json'
    with open(addressID,'r') as f:
       ids = json.loads(f.read())
    with open(addressR,'r') as f:
       values = json.loads(f.read()) 
    val = values.get(ids[0])#list 里又分dictionary
    list = []
    for v in val:
        list.append(v.get('comment'))
    #print(list)
       
    stemming(addressTrans,list)
    
    delete_stopping_word(addressTrans)
    
    delete_punctuation(addressTrans)
   
    print('done')

if __name__ == "__main__":
    main()
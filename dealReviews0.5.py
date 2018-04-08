# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 10:57:12 2018

@author: jiyuxin
"""

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
import os
from os.path import join as pjoin
import json
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


def delete_punctuation(address,r2):
    
    List = r2
    punc = string.punctuation
    
    new_list = []

    for line in List: 
        if line not in punc:
            new_list.append(line) 
    return new_list    

    
def delete_stopping_word(address,r1):
    
    
    newlist = []
    stop_words = stopwords.words('english')
    for line in r1:
        
       
       if line not in stop_words:
           newlist.append(line)
    return newlist      
           
    
    
def stemming(out,comment):
    
    ps = PorterStemmer()
    newlist = []
    
    words = word_tokenize(comment)
    
    for w in words:
        newlist.append(ps.stem(w))
    
    return newlist
     
def related_reviews(out,address,r3):
    
    outputdir = out
    listdir = os.listdir(outputdir)
    Reviews = r3
    sec_words = ["security","slow","termination","account","hijacking","authentication","back", "door","Business", "Email","Compromise","Card","skimmers","Data","Driven", "Attack","Flooding","leak","memory","Identification","Information","Mobile", "Code","password","Pharming","Replicator","Sensitive" ,"Information","Smurfing","spoofing","Virus","Vulnerability"]
    ps = PorterStemmer()
    newW = []
    newRe = []
    for aw in sec_words:
        words = word_tokenize(aw)
        for w in words:
                newW.append(ps.stem(w))##sec_words stemming
    for line in Reviews:
        
       if line in newW:
           newRe.append(line)
    
    if 'keywords.json' in listdir:  
        fr = open(pjoin(outputdir, 'keywords.json'), 'a')   
        model=json.dumps(newRe)  
        fr.write(model)    
        fr.close()
    return newRe
    
def main():
    addressID = 'D:/项目/资料/MEDICAL/topapp_appid.json'
    addressR = 'D:/项目/资料/MEDICAL/topapp_review.json'
    addressTrans = 'D:/项目/newjson/test.json'
    outputdir = 'D:/项目/newjson'
    listdir = os.listdir(outputdir)
    with open(addressID,'r') as f:
       ids = json.loads(f.read())
    with open(addressR,'r') as f:
       values = json.loads(f.read())
    
    for id in ids:
        val = values.get(id)#list 里又分dictionary
        if 'relatedReviews.json' in listdir:  
                    fr = open(pjoin(outputdir, 'relatedReviews.json'), 'a')   
                    blank1 = json.dumps('    ')
                    model=json.dumps(id)  
                    blank2 = json.dumps(':     ')
                    fr.write(blank1)
                    fr.write(model) 
                    fr.write(blank2)
                    fr.close()
    
        for v in val:
    
            oneComment = v.get('comment')
        
            r1 = stemming(outputdir,oneComment)
            r2 = delete_stopping_word(addressTrans,r1)
            r3 = delete_punctuation(addressTrans,r2)
            related_reviews(outputdir,addressTrans,r3)
            v['processedwords'] = oneComment
            issecurity = related_reviews(outputdir,addressTrans,r3)
            if issecurity:
            #
                if 'relatedReviews.json' in listdir:  
                    fr = open(pjoin(outputdir, 'relatedReviews.json'), 'a')   
                    model=json.dumps(oneComment)  
                    fr.write(model)    
                    fr.close()
                    
        print('current app in dealing:')
        print(id)
        
    print('done')

if __name__ == "__main__":
    main()
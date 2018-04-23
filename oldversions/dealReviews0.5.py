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


def delete_punctuation(r2):
    
    
    punc = string.punctuation
    
    new_list = []

    for line in r2: 
        if line not in punc:
            new_list.append(line) 
    return new_list    

    
def delete_stopping_word(r1):
    
    
    newlist = []
    stop_words = stopwords.words('english')
    for line in r1:
        if line not in stop_words:
           newlist.append(line)
    return newlist      
           
    
    
def stemming(comment):
    
    ps = PorterStemmer()
    newlist = []
    
    words = word_tokenize(comment)
    
    for w in words:
        newlist.append(ps.stem(w))
    
    return newlist
     
def related_reviews(out,r3):
    
    outputdir = out
    listdir = os.listdir(outputdir)
    Reviews = r3
    sec_words = ["security","slow","termination","account","hijacking","authentication","back", "door","Business", "Email","Compromise","Card","skimmers","Data","Driven", "Attack","Flooding","leak","memory","Identification","Information","Mobile", "Code","password","Pharming","Replicator","Sensitive" ,"Information","Smurfing","spoofing","Virus","Vulnerability"]
    ps = PorterStemmer()
    newW = []
    newRe = []
    for a_word in sec_words:
        words = word_tokenize(a_word)
        for w in words:
                newW.append(ps.stem(w))##sec_words stemming
    for line in Reviews:
        
       if line in newW:
           newRe.append(line)
    
    if 'keywords.json' in listdir:  
        fr = open(pjoin(outputdir, 'keywords.json'), 'a')   
        model4=json.dumps(newRe)  
        fr.write(model4)    
        fr.close()
    return newRe
    
def main():
    categories = [
         'ART_AND_DESIGN',
         'AUTO_AND_VEHICLES',
         'BEAUTY',
         'BOOKS_AND_REFERENCE',
         'BUSINESS',
         'COMICS',
         'COMMUNICATION',
         'DATING',
         'EDUCATION',
         'ENTERTAINMENT',
         'EVENTS',
         'FAMILY'
         
         ]
    base_url = 'D:/项目/资料'
    outputdir = 'D:/项目/newjson'
    listdir = os.listdir(outputdir)
    for cat in categories:
        print('\nFetching data in category %s\n' % cat)
        cat_url = os.path.join(base_url, cat)
        if 'relatedReviews.json' in listdir:  
                    fr = open(pjoin(outputdir, 'relatedReviews.json'), 'a')   
                    blank1 = json.dumps('    ')
                    model1=json.dumps(cat)  
                    blank2 = json.dumps(':     ')
                    fr.write(blank1)
                    fr.write(model1) 
                    fr.write(blank2)
                    fr.close()
    
        with open(os.path.join(cat_url, 'topapp_appid.json'),'r') as f:
            ids = json.loads(f.read())
        with open(os.path.join(cat_url, 'topapp_review.json'),'r') as f:
            values = json.loads(f.read())
    
        for id in ids:
            val = values.get(id)
            if 'relatedReviews.json' in listdir:  
                    fr = open(pjoin(outputdir, 'relatedReviews.json'), 'a')   
                    blank1 = json.dumps('    ')
                    model2=json.dumps(id)  
                    blank2 = json.dumps(':     ')
                    fr.write(blank1)
                    fr.write(model2) 
                    fr.write(blank2)
                    fr.close()
    
            for v in val:
    
                oneComment = v.get('comment')
        
                after_stemming = stemming(oneComment)
                remove_stopping = delete_stopping_word(after_stemming)
                punc_deleted = delete_punctuation(remove_stopping)
                related_reviews(outputdir,punc_deleted)
                v['processedwords'] = oneComment
                issecurity = related_reviews(outputdir,punc_deleted)
                if issecurity:
            
                    if 'relatedReviews.json' in listdir:  
                        fr = open(pjoin(outputdir, 'relatedReviews.json'), 'a')   
                        model3=json.dumps(oneComment)  
                        fr.write(model3)    
                        fr.close()
                    
            print('current app in dealing:')
            print(id)
        
    print('done')

if __name__ == "__main__":
    main()
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
     
def dump_to_json(file_name,listdir,outputdir,input):
    
    if file_name in listdir:  
            fr = open(pjoin(outputdir, file_name), 'a')   
            model3=json.dumps(input)  
            fr.write(model3)    
            fr.close()

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
    
    #dump_to_json('keywords.json',listdir,outputdir,newRe)
    
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
         'FAMILY',
         'FINANCE',
         'FOOD_AND_DRINK',
         'GAME',
         'HEALTH_AND_FITNESS',
         'HOUSE_AND_HOME',
         'LIBRARIES_AND_DEMO',
         'LIFESTYLE',
         'MAPS_AND_NAVIGATION',
         'MEDICAL',
         'MUSIC_AND_AUDIO',
         'NEWS_AND_MAGAZINES',
         'PARENTING',
         'PERSONALIZATION',
         'PHOTOGRAPHY',
         'PRODUCTIVITY',
         'SHOPPING',
         'SOCIAL',
         'SPORTS',
         'TOOLS',
         'TRAVEL_AND_LOCAL',
         'VIDEO_PLAYERS',
         'WEATHER'
         
         
         ]
    base_url = 'D:/项目/资料'
    outputdir = 'D:/项目/newjson'
    listdir = os.listdir(outputdir)
    comments = []
    rank_cat = []
    rank_id = {}
    review_cat = {}
    review_id = {}
    rank_top50 = {}
    size_rank = 0
    for cat in categories:
        print('\nFetching data in category %s\n' % cat)
        cat_url = os.path.join(base_url, cat)
        
    
        with open(os.path.join(cat_url, 'topapp_appid.json'),'r') as f:
            ids = json.loads(f.read())
        with open(os.path.join(cat_url, 'topapp_review.json'),'r') as f:
            values = json.loads(f.read())
        #ids = ['com.hypetypetext.animated.text.editor','com.snt.colorshapetounlockdoll','com.sonymobile.sketch','com.lightapp.wolves',"wall.team10.wallpapers", "com.yusuf.ronaldowallpapersnew", "com.andromo.dev648448.app719015", "com.meltinglogic.pixly", "com.cadTouch.androidTrial", "de.test.project1", "idealtheory.tiles.app", "com.metajunky.glittercoloring", "com.zamastudio.nifty.diy.crafts", "com.infokombinat.howtodrawkawaii", "com.drawcoloring.sonichedhog", "com.dbs.dragonbal", "text3d.logo.designArt", "howto.draw.book.coloring.beyblade.gamesart", "com.nsoft.calligraphy.nameart", "com.onetap.bit8painter", "com.rollins.seth.hd.wallpapers", "com.vegapunk.raphiphopwallpapers", "com.lightapp.wolves", "com.SpaceSavingFurniture.usefulcraft", "com.andromo.dev660614.app735712", "com.brakefield.idfree", "com.bifjamed.bangtanWallpapers", "learn.to.draw.glow.animal", "com.hakehakewp.annieleblancwallpapershd4k", "com.diewithme", "lilpump.yusuf99.wallpaperhd", "com.yusuf.messiwallpapersnew", "com.ai.viewer.illustrator", "com.appdreams.write.name.add.photo.birthday.cake.photo.frames.editor.live.wallpaper", "com.color.dream.number.book.pixly", "com.chardon.yugiwallpap", "com.eyewind.colorfit.garden"]
        for id in ids:
            print('current app in dealing:')
            print(id)
            comments = []#reset
            rank_cat = []#reset
            size_rank = 0#reset
            val = values.get(id)
            for v in val:
    
                oneComment = v.get('comment')
        
                after_stemming = stemming(oneComment)
                remove_stopping = delete_stopping_word(after_stemming)
                punc_deleted = delete_punctuation(remove_stopping)
                related_reviews(outputdir,punc_deleted)
                
                issecurity = related_reviews(outputdir,punc_deleted)
                if issecurity:
                    comments.append(oneComment)
                    size_rank = size_rank+len(issecurity)#get the score
            
            rank_cat.append(size_rank)
            rank_cat.append(cat)
            rank_id[id] = rank_cat
            review_id[id] = comments
        
        review_cat[cat] = review_id
    rank_id = sorted(rank_id.items(), key=lambda item:item[1], reverse=True)  
    
    count = 0
    required_count = 50
    for key,value in rank_id:
        count += 1
        if count >  required_count:
            break
        rank_top50[key] = value
        
       
       
    dump_to_json('relatedReviews.json',listdir,outputdir,review_cat)
    dump_to_json('rank.json',listdir,outputdir,rank_top50)   
    
     
    print('done')

if __name__ == "__main__":
    main()
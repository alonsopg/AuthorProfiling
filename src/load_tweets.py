#!/usr/bin/env python
# -*- coding: utf-8

# Importar librerías requeridas
import os
import json
import codecs
import xml.etree.ElementTree as ET



# Carga los tweets de un XML (formato 2015)
def load_tweets_xml(filename):
    tweets,ids=[],[]
    with open(filename,'r') as filename:
        """lee el xml y agrega el tweet leido en nuestro arreglo de tweets"""
        count = 0
        tree = ET.parse(filename)
        root = tree.getroot()
        for document in root.iter('document'):
            txt=document.text
            txt=txt.replace("![CDATA[",'')
            txt=txt.replace("]]",'')
            txt=txt.strip()
            tweets.append(document.text)
            ids.append(count)
            count+=1
    return tweets,ids


# Busca en un directiorio archivos xml (pan15) o xml y json (pan14)
def load_tweets(DIR,format='pan15',mix=True):
    tweets, ids=[],[]
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            if format.startswith('pan14'):
                if filename.endswith('.json'):
                    with open(os.path.join(DIR,filename)) as json_file:
                        data = json.load(json_file)
                        id_usuario=os.path.basename(filename[:-5])
                        for tweet in data:
                            try:
                                tweets.append(tweet['data'])
                                ids.append((tweet['index'],id_usuario))
                            except KeyError:
                                pass

            else:
                if filename.endswith('.xml'):
                    tweets_,ids_=load_tweets_xml(os.path.join(DIR,filename))
                    id_usuario=os.path.basename(filename[:-4])
                    tweets.append(tweets_)
                    ids.append([(i,id_usuario) for i in ids_])

    # Mezclar tweets de usarios 
    if mix:
        tweets_={}
        order_=[]
        for i,id_user in enumerate(ids):
            try:
                tweets_[id_user[0][1]].append(" ".join(tweets[i]).strip())
            except KeyError:
                tweets_[id_user[0][1]]=[" ".join(tweets[i]).strip()]
                order_.append(id_user[0][1])
        tweets=[" ".join(tweets_[id_user]) for id_user in order_ ]
        ids=order_
    return tweets,ids

                        



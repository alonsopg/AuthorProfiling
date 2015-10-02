#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

# Importar librerías requeridas
import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import argparse, os, codecs, re, itertools

# Local imports
from load_tweets import load_tweets

# Variables de configuaración
NAME='ef_distance'
prefix='distance'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus with json")
    p.add_argument("-d", "--dir",
            action="store", dest="dir",default="feats",
        help="Default directory for features [feats]")
    p.add_argument("-p", "--pref",
            action="store", dest="pref",default=prefix,
        help="Prefix to save the file of features %s"%prefix)
    p.add_argument("--mix",
            action="store_true", dest="mix",default=True,
        help="Mix tweets into pefiles")
    p.add_argument("--format",
            action="store_true", dest="format",default="pan15",
        help="Change to pan14 to use format from 2015 [feats]")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    p.add_argument("--stopwords", default=None,
        action="store", dest="stopwords",
        help="List of stop words [data/stopwords.txt]")
    p.add_argument("--min",
        action="store", dest="min",default=10,type=int,
        help="Define el valor minimo de cuentas ")
    opts = p.parse_args()

    def DistJaccard(str1, str2):
        str1 = set(str1.split())
        str2 = set(str2.split())
        try:
            return float(len(str1 & str2)) / len(str1 | str2)
        except ZeroDivisionError:
            return 0
    

    # prepara función de verbose
    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:   
        verbose = lambda *a: None 

    # Colecta los tweets y sus identificadores (idtweet y idusuario)
    users,ids=load_tweets(opts.DIR,opts.format,False)
    #print (users)
    #lo limpiamos de links
    clean_users = [[re.sub(r'\bhttps?:\/\/.*[\r\n]*', u'', i) for i in x] for x in users]    
    #Lo mostramos 
    histogram_list = []

    for tweets in clean_users:
        #print(tweets)
        
        tweets_1 = list(tweets)
        tweets_2 = list(tweets)
        
        #tweets_1 = list(clean_tweets_2)
        #tweets_2 = list(clean_tweets_2)
        #print(tweets_1)
    
        listaVector=[]
        contador=0
        for i,cadena in enumerate(tweets_1):
            for cadena2 in tweets_2[i+1:]:
                
                distanciaJaccard=DistJaccard(cadena,cadena2)
                listaVector.append(distanciaJaccard)


    
        import numpy as np
        import matplotlib.pyplot as plt
        hist=np.histogram(listaVector,range=(0,1))
        histogram_list.append(hist[0])
        
        
    # Imprime alguna información sobre los tweets
    if opts.verbose:
        for i,tweet in enumerate(tweets[:10]):
            verbose('Tweet example',i+1,tweet[:100])
        verbose("Total tweets   : ",len(tweets))
        try:
            verbose("Total usuarios : ",len(set([id for x,id in ids])))
        except ValueError:
            verbose("Total usuarios : ",len(ids))
            
    

    # Calculamos los features
    #metemos las stop words en una lista
    #if not opts.stopwords:
    #    my_stop_words=[]
    #else:
    #    with codecs.open(opts.stopwords, encoding='utf-8') as f:
    #        spanish_stop_words = [line.strip() for line in f]
            #print (spanish_stop_words)

    #    from sklearn.feature_extraction import text
    #    my_stop_words = text.ENGLISH_STOP_WORDS.union(spanish_stop_words)


    # - Creamos contador
    #from sklearn.feature_extraction.text import TfidfVectorizer
    #tfidf_vect = TfidfVectorizer(norm=u'l1', use_idf=True, 
    #smooth_idf=True, sublinear_tf=False,
    #min_df=2,stop_words=set(my_stop_words), ngram_range=(4, 4))
    
    # - Contamos las palabras en los tweets
    feats = np.asarray(histogram_list)

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,prefix+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    #verbose("First feats names :",tfidf_vect.get_feature_names()[:10])
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,prefix+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)
 

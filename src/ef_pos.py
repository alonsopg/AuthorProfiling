#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

# Importar librerías requeridas
import cPickle as pickle
import numpy as np
import argparse
import os
import codecs

# Local imports
from load_tweets import load_tweets

# Variables de configuaración
NAME='ef_pos'
prefix='pos'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus with json")
    p.add_argument("-d", "--dir",
            action="store", dest="dir",default="feats",
        help="Default directory for features [feats]")
    p.add_argument("-p", "--pref",
            action="store_true", dest="pref",default=prefix,
        help="Prefix to save the file of features %s"%prefix)
    p.add_argument( "--vect",
            action="store", dest="vect",default=None,
        help="Training vector file")
    p.add_argument("--mix",
            action="store_true", dest="mix",default=True,
        help="Mix tweets into pefiles")
    p.add_argument("--format",
            action="store_true", dest="format",default="pan15",
        help="Change to pan14 to use format from 2015 [feats]")
    p.add_argument("--stopwords", default=None,
        action="store", dest="stopwords",
        help="List of stop words [data/stopwords.txt]")
    p.add_argument("--tag",
        action="store", dest="tag",default=1,type=int,
        help="Position of pos tag ")
    p.add_argument("--ngram",
        action="store", dest="ngrammax",default=3,type=int,
        help="El valor máximo de ngramas ")
    p.add_argument("--min",
        action="store", dest="min",default=10,type=int,
        help="Define el valor minimo de cuentas ")
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Verbose mode [Off]")
    opts = p.parse_args()
    

    # prepara función de verbose
    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:   
        verbose = lambda *a: None 

    # Colecta los tweets y sus identificadores (idtweet y idusuario)
    tweets,ids=load_tweets(opts.DIR,opts.format,mix=opts.mix)

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
    if not opts.stopwords:
        my_stop_words=[]
    else:
        with codecs.open(opts.stopwords, encoding='utf-8') as f:
            spanish_stop_words = [line.strip() for line in f]
            #print (spanish_stop_words)

        from sklearn.feature_extraction import text
        my_stop_words = text.ENGLISH_STOP_WORDS.union(spanish_stop_words)

    # Reading tagged files

    tagged=[]
    for idd in ids:
        tagged.append([])
        for line in\
            codecs.open(os.path.join(opts.DIR,idd+".txt_tag"),'r','utf-8'):
                tagged[-1].append(line.strip().split()[-opts.tag])
        tagged[-1]=" ".join(tagged[-1])

    # - Creamos contador
    if not opts.vect:
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf_vect = TfidfVectorizer(min_df=opts.min,
                stop_words=set(my_stop_words),
                ngram_range=(1,opts.ngrammax))
        # - Contamos las palabras en los tweets
        feats = tfidf_vect.fit_transform(np.asarray(tagged))
        print(tfidf_vect.get_feature_names())
    else:
        with open(opts.vect,"r") as model:
            s=model.read()
            tfidf_vect = pickle.loads(s)
            # - Contamos las palabras en los tweets
            feats = tfidf_vect.transform(np.asarray(tweets))

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,prefix+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    with open(os.path.join(opts.dir,prefix+'.vec'),'wb') as idxf:
        pickle.dump(tfidf_vect, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("First feats names :",tfidf_vect.get_feature_names()[:100])
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,prefix+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)
 
   
    





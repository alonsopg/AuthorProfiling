#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import codecs
import cPickle as pickle
import numpy as np
import os

from load_tweets import load_tweets
from collections import Counter

NAME='ef_polarity'
prefix='polarity'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
    p.add_argument("LIST1",default=None,
        action="store", help="File with list of words")
    p.add_argument("-d", "--dir",
            action="store", dest="dir",default="feats",
        help="Default directory for features [feats]")
    p.add_argument("--deli",
            action="store", dest="deli",default=None,
        help="Delimeter [None]")
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

    opts = p.parse_args()

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
            verbose(u'Tweet example',i+1,tweet[:100])
        verbose(u"Total tweets   : ",len(tweets))
        try:
            verbose(u"Total usuarios : ",len(set([id for x,id in ids])))
        except ValueError:
            verbose(u"Total usuarios : ",len(ids))

    # Calculamos los features
    # - Cargar lista de palabras uno

    words=[]
    for line in codecs.open(opts.LIST1,encoding='utf-8'):
        line=line.strip()
        if not opts.deli:
            bits=line.split()
            words.append((" ".join(bits[:-1]),float(bits[-1])))
        else:
            bits=line.split(opts.deli)
            words.append((bits[0],float(bits[-1])))

    tweet_counts=[]
    for tweet in tweets:
        tweet_words=tweet.split()
        counts=Counter(tweet_words)
        vec=[counts[word]*val for word,val in words]
        vec.append(sum(vec))
        vec.append(sum(vec)/len(tweet_words))
        tweet_counts.append(vec)

    # - Contamos las palabras en los tweets
    feats = np.asarray(tweet_counts)

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,opts.pref+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,opts.pref+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)





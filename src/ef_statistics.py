#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import cPickle as pickle
import numpy as np
import os

from load_tweets import load_tweets

NAME='ef_statistics'
prefix='statistics'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
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

    opts = p.parse_args()

    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:   
        verbose = lambda *a: None 


    # Colecta los tweets y sus identificadores (idtweet y idusuario)
    users,ids=load_tweets(opts.DIR,opts.format,False)

    # Imprime alguna información sobre los tweets
    if opts.verbose:
        for tweets in users[:2]:
            verbose("User")
            for i,tweet in enumerate(tweets[:2]):
                verbose(u'Tweet example',i+1,tweet)
            verbose(u"Total tweets   : ",len(tweets))
            try:
                verbose(u"Total usuarios : ",len(set([id for x,id in ids])))
            except ValueError:
                verbose(u"Total usuarios : ",len(ids))

    # Calculamos los features
    # - Cargar lista de palabras uno

    tweet_stats=[]
    for tweets in users:
        # lens
        stats=[]
        # chars
        feat=[len(t) for t in  tweets]
        chars=sum(feat)
        stats.append(sum(feat))
        stats.append(sum(feat)/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # words
        feat=[len(t.split()) for t  in  tweets]
        stats.append(chars*1.0/sum(feat))
        stats.append(sum(feat))
        stats.append(sum(feat)*1.0/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # Mayusculas 
        feat=[sum([1 for l in t if l.isupper()]) for t in  tweets]
        stats.append(sum(feat))
        stats.append(sum(feat)/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # Palabras con Mayuscula inicial
        feat=[sum([1 for l in t.split() if l.istitle()]) for t in  tweets]
        stats.append(sum(feat))
        stats.append(sum(feat)/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # Arrobas (amigos)
        feat=[sum([1 for l in t if l=="@"]) for t in  tweets]
        stats.append(sum(feat))
        stats.append(sum(feat)*1.0/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # Arrobas inicial (reply??) 
        feat=[1 for t in  tweets if t[0] == "@"]
        stats.append(sum(feat))
        stats.append(sum(feat)*1.0/len(tweets))
	# HashTags (amigos)
        feat_hash=[sum([1 for l in t if l=="#"]) for t in  tweets]
        stats.append(sum(feat_hash))
        stats.append(sum(feat_hash)*1.0/len(tweets))
        stats.append(max(feat_hash))
        stats.append(min(feat_hash))

        # Arrobas minusculas
        feat=[sum([1 for l in t if l.islower()]) for t in  tweets]
        stats.append(sum(feat))
        stats.append(sum(feat)*1.0/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # Números 
        feat=[sum([1 for l in t if l.isdigit()]) for t in  tweets]
        stats.append(sum(feat))
        stats.append(sum(feat)*1.0/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
        # Oraciones
        feat=[len(t.split('.')) for t  in  tweets]
        stats.append(sum(feat))
        stats.append(sum(feat)*1.0/len(tweets))
        stats.append(max(feat))
        stats.append(min(feat))
    
        tweet_stats.append(stats)

    # - Contamos las palabras en los tweets
    feats = np.asarray(tweet_stats)

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,opts.pref+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,opts.pref+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)





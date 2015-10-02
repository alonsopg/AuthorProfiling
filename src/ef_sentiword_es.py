#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import codecs
import cPickle as pickle
import numpy as np
import csv
import os
import pandas as pd
import re
from collections import Counter

from load_tweets import load_tweets

NAME='ef_sentiword'
prefix='sentiword'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)

    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")

    p.add_argument("LIST",default=None,
        action="store", help="File with list of words")

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
            verbose('Tweet example',i+1,tweet[:100])
        verbose("Total tweets   : ",len(tweets))
        try:
            verbose("Total usuarios : ",len(set([id for x,id in ids])))
        except ValueError:
            verbose("Total usuarios : ",len(ids))
    
    # Calculamos los features
    # - Cargar lista de palabras uno


#    df = pd.read_csv(opts.LIST, sep = '\t')
    with open(opts.LIST) as text1:
        words_pos = [a for a, b, c in list(csv.reader(text1))[1:] if float(b) > 0]
    
    with open(opts.LIST) as text2:
        words_neg = [a for a, b, c in list(csv.reader(text2))[1:] if float(c) > 0]    
        
    #words_pos_final = set(term.split("#", 1)[0].replace("_", " ") for term in words_pos)
    _regex_1 = re.compile(r"(\b{}\b)".format(r"\b|\b".join(words_pos)))
    #words_pos_final = set(term.split("#", 1)[0].replace("_", " ") for term in pos_score)
    
    
    #words_neg_final = set(term.split("#", 1)[0].replace("_", " ") for term in words_neg)
    _regex_2 = re.compile(r"(\b{}\b)".format(r"\b|\b".join(words_neg)))
    #words_neg_final = set(term.split("#", 1)[0].replace("_", " ") for term in neg_score)


    #print(tweets)

    count_words_pos = [
        
             _regex_1.findall(sublista)
         for sublista in tweets
    ]

    #print('pos count')
    pos_count = [
        sum(1 for ocurrencia in _regex_1.findall(sublista))
        for sublista in tweets
    ]


    #print('.......')
    count_words_neg = [
         _regex_2.findall(sublista_2)
        for sublista_2 in tweets
    ]


    #print('neg count')
    neg_count = [
        
        sum(1 for ocurrencia_2 in _regex_2.findall(sublista_2))
         for sublista_2 in tweets
    ]




    #print ('\nEste es el count: ',pos_count)
    #print ('Se reconocieron las palabras: ', count_words_pos)

#        print '\n********************************************************\n'

    #print ('Este es el count negativo',neg_count)
    #print ('Se reconocieron las palabras en el negativo:', count_words_neg)

    feats = np.vstack((np.asarray([neg_count]),np.asarray([pos_count])))
    feats = feats.T
    print(feats)
    
    # Guarda la matrix de features
    with open(os.path.join(opts.dir,opts.pref+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,opts.pref+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)

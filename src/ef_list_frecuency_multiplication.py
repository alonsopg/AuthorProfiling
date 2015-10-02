#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import cPickle as pickle
import numpy as np
import csv
import os

from load_tweets import load_tweets
from collections import Counter

NAME='ef_list_frequency_multiplication'
prefix='list_frequency_multiplication'

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
            verbose('Tweet example',i+1,tweet[:100])
        verbose("Total tweets   : ",len(tweets))
        try:
            verbose("Total usuarios : ",len(set([id for x,id in ids])))
        except ValueError:
            verbose("Total usuarios : ",len(ids))

    # Calculamos los features
    # - Cargar lista de palabras uno
    lista_dict = []
    lista_wights1 = []
    lista_wights2 =  []
    lista_wights3= []
    with open(opts.LIST) as f:
      for row in csv.reader(f):
        lista_dict.append(row[0])
        lista_wights1.append(float(row[1]))
        lista_wights2.append(float(row[2]))
        lista_wights3.append(float(row[3]))

    counts=[]
    for usuario in tweets:
        usuario=usuario.split()
        cc=Counter(usuario)
        vec1=[cc[item] for item in lista_dict]

        vec=vec1
        counts.append(vec1)


    feats = np.asarray(counts)


    counts2=[]
    for vector in feats:
        results1 = [a*b for a,b in zip(vector,lista_wights1)]+[a*b for a,b in zip(vector,lista_wights2)]+[a*b for a,b in zip(vector,lista_wights3)]

        counts2.append(results1)


    # - Contamos las palabras en los tweets
    feats = np.asarray(counts2)

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,opts.pref+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,opts.pref+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)




















































#tweets = [['this is a task a a a a this abandon abandoned abandoned  abated'],['task non this yu']]






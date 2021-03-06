#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import cPickle as pickle
import numpy as np
import os
import re
import csv

from load_tweets import load_tweets

NAME='ef_whissell_t'
prefix='whissell_t'

class Sum(object):
    def __init__(self, *arguments):
        self.lista = arguments

    def __repr__(self):
        return str(tuple(self.lista))

    def __iadd__(self, otr):
        nuev_elem = [self.lista[i] + otr.lista[i] for i in range(3)]
        return Sum(*nuev_elem)


if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)

    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
   
    p.add_argument("LISTA",default=None,
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
    
    acarreos_final = {}
    with open(opts.LISTA) as f:
        read = csv.reader(f)
        for elem in read:
            acarreos_final[elem[0].lower()] = Sum(*map(float, elem[1:]))
    
    sum_per_line = []
    for x in tweets:
        acarreo_sum = Sum(0,0,0)
        for word in re.split(r'[^\w]+', x[0]):
        #for word in re.split(r'[^\w]+', elem):
            try:
                sum = acarreos_final[word.lower()]
                #print("  encontro en wissel con el sig peso: %s %s" % (word.lower(), sum))
                acarreo_sum += sum
            except KeyError:
                pass
        sum_per_line.append(acarreo_sum)

    
    # - Contamos las palabras en los tweets
    feats = np.asarray([l.lista for l in sum_per_line])

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,opts.pref+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,opts.pref+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)





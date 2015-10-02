#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import codecs
import os

from load_tweets import load_tweets

NAME='extract_text'

if __name__ == "__main__":
    # Las opciones de línea de comando
    p = argparse.ArgumentParser(NAME)
    p.add_argument("DIR",default=None,
        action="store", help="Directory with corpus")
    p.add_argument("-d", "--dir",
            action="store", dest="dir",default="feats",
        help="Default directory for features [feats]")
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

    for idd,user in zip(ids,users):
        with codecs.open(os.path.join(opts.DIR,idd[0][1]+".txt"),'w','utf-8') as f:
            for tweet in user:
                print(tweet,file=f)



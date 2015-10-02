#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function
import argparse
import codecs
#from sklearn.feature_extraction.text import TfidfVectorizer
import cPickle as pickle
#from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os


from load_tweets import load_tweets

NAME='ef_links'
prefix='links'


links = dict()
user_list = list()
final_list = list()

#Funcion para contar los links
def buscar(tweet):
	#fname = raw_input("Enter file name: ")
	#fh = open(fname)
	fh = tweet
	count = 0
	links_user = dict()
	for line in [fh]:
		#print line
		words = line.split()

		for word in words:
			if not word.startswith('http://www') : continue
			link2_name = word.split('www.')
			link2_name2 = link2_name[1].split('.')
			count += 1
			links[link2_name2[0]] = links.get(link2_name2[0],0)+1
			links_user[link2_name2[0]] = links_user.get(link2_name2[0],0)+1

		for word in words:
			if not word.startswith('http://') : continue
			link2_name = word.split('//')
			link2_name2 = link2_name[1].split('.')
			if(link2_name2[0] != 'www'):
				links[link2_name2[0]] = links.get(link2_name2[0],0)+1
				links_user[link2_name2[0]] = links_user.get(link2_name2[0],0)+1
				count += 1

		for word in words:
			if not word.startswith('www.') : continue
			link_name = word.split('.')
			count = count + 1
			links[link_name[1]] = links.get(link_name[1],0)+1
			links_user[link_name[1]] = links_user.get(link_name[1],0)+1

	user_list.append(links_user)
	return links_user

#Funcion para crear la lista de listas de los usuarios y los links
def matriz():
	for user in user_list:
		temp = list()
		for link in link_list:
			temp.append(user.get(link,0))
		final_list.append(temp)


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
    
    p.add_argument("-l", "--links",
            action="store", dest="links",default=None,
        help="Links list to read from")
    

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
    # - Creamos contador
    
    for user in tweets:
	buscar(user)

    if not opts.links:
        link_list = links.keys()
    else:
        with open(opts.links,"r") as model:
            s=model.read()
            link_list = pickle.loads(s)
    matriz()

    # - Contamos las palabras en los tweets
    feats = np.asarray(final_list)

    # Guarda la matrix de features
    with open(os.path.join(opts.dir,prefix+'.dat'),'wb') as idxf:
        pickle.dump(feats, idxf, pickle.HIGHEST_PROTOCOL)

    # Imprimimos información de la matrix
    verbose("links             :",link_list)
    verbose("Total de features :",feats.shape[1])
    verbose("Total de renglones:",feats.shape[0])

    # Guarda los indices por renglones de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,prefix+'.idx'),'wb') as idxf:
        pickle.dump(ids, idxf, pickle.HIGHEST_PROTOCOL)

    # Guarda los links  de la matrix (usuario o tweet, usuario)
    with open(os.path.join(opts.dir,prefix+'.vec'),'wb') as idxf:
        pickle.dump(link_list, idxf, pickle.HIGHEST_PROTOCOL)


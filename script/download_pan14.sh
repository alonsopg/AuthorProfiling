#!/bin/bash

if [ ! -f data/pan14-author-profiling-training-corpus-spanish-twitter-2014-04-16.zip ]; then
	echo "Original spanish zip file not found"
	read -p "Do you want to download spanish pan14 corpus? [yes/NO]" -n 1 -r
	echo   
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		wget http://turing.iimas.unam.mx/~ivanvladimir/pan14-author-profiling-training-corpus-spanish-twitter-2014-04-16.zip 
		mv pan14-author-profiling-training-corpus-spanish-twitter-2014-04-16.zip data
	fi
fi

if [ ! -f data/pan14-author-profiling-training-corpus-english-twitter-2014-04-16.zip ]; then
	echo "Original english zip file not found, please download it"
	read -p "Do you want to download english pan14 corpus? [yes/NO]" -n 1 -r
	echo   
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		wget http://turing.iimas.unam.mx/~ivanvladimir/pan14-author-profiling-training-corpus-english-twitter-2014-04-16.zip 
		mv pan14-author-profiling-training-corpus-english-twitter-2014-04-16.zip data
	fi
fi


unzip data/pan14-author-profiling-training-corpus-spanish-twitter-2014-04-16.zip 
unzip data/pan14-author-profiling-training-corpus-english-twitter-2014-04-16.zip 

mv mnt/nfs/tira/data/pan14-training-corpora-truth/pan14-author-profiling-training-corpus-english-twitter-2014-04-16 data/pan14_english
mv mnt/nfs/tira/data/pan14-training-corpora-truth/pan14-author-profiling-training-corpus-spanish-twitter-2014-04-16 data/pan14_spanish

if [ ! -f data/tweets_en.zip ]; then
	echo "Extracted  english tweets file not found"
	echo "Please download from private copy to make a functional copy"
else
	unzip data/tweets_en.zip
	mv data/tweets_en/*.json data/pan14_english
	rm -rf data/tweets_en
fi

if [ ! -f data/tweets_es.zip ]; then
	echo "Extracted  spanish tweets file not found"
	echo "Please download from private copy to make a functional copy"
else
	unzip data/tweets_es.zip
	mv tweets/*.json data/pan14_spanish
	rm -rf tweets
fi


rm -rf mnt/nfs/tira/data/pan14-training-corpora-truth


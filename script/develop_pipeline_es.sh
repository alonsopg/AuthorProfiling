#!/bin/bash

mode="gender"
echo "Running training authorid"
while getopts m: opt; do
	case $opt in
	m)
	mode=$OPTARG
	;;
	esac
	done


rm feats/*.idx
rm feats/*.dat

#python src/ef_1grams.py --stopwords data/stop_words/stop_words_es.txt data/pan15/spanish
python src/ef_tfidf.py --stopwords data/stop_words/stop_words_es.txt  data/pan15/spanish
python src/ef_links.py data/pan15/spanish


python src/ef_wissell_t.py data/pan15/spanish/ data/SentimentAnalysisDict/es/Whissell/whissell_es.txt

python src/develop.py  -m ${mode} -v data/pan15/spanish

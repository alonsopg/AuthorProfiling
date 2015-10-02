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

rm feats/*

#python src/ef_1grams.py data/pan15/italian
python src/ef_tfidf.py --stopwords data/stop_words/stop_words_it.txt data/pan15/italian
python src/ef_list_baseline.py -p lb_reyes data/pan15/italian data/SentimentAnalysisDict/it/Reyes/counterFactuality-ita.txt data/SentimentAnalysisDict/it/Reyes/temporalCompression-ita.txt
python src/ef_list_frequency.py -p lf_reyes data/pan15/italian data/SentimentAnalysisDict/it/Reyes/counterFactuality-ita.txt data/SentimentAnalysisDict/it/Reyes/temporalCompression-ita.txt
#python src/ef_links.py data/pan15/italian

# Emoticons y puntuación
python src/ef_list_emoticons.py data/pan15/italian data/emoticons.txt
python src/ef_list_punctuation.py data/pan15/italian data/punctuation.txt

python src/ef_list_baseline.py -p lb_hu data/pan15/italian data/SentimentAnalysisDict/it/Hu-Liu/positives.txt data/SentimentAnalysisDict/it/Hu-Liu/negatives.txt
python src/ef_list_frequency.py -p lf_hu data/pan15/italian data/SentimentAnalysisDict/it/Hu-Liu/positives.txt data/SentimentAnalysisDict/it/Hu-Liu/negatives.txt

python src/ef_wissell_t.py data/pan15/italian/ data/SentimentAnalysisDict/it/Whissell/whissell-v1.txt

python src/develop.py -v -m ${mode} data/pan15/italian

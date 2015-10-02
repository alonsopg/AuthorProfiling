#!/bin/bash

mode="gender"
echo "Running training authorprof"
while getopts m: opt; do
	case $opt in
	m)
	mode=$OPTARG
	;;
	esac
	done

rm feats/*.idx
rm feats/*.dat

#python src/ef_1grams.py  --stopwords data/stop_words/stop_words_en.txt  data/pan15/english
python src/ef_tfidf.py --stopwords data/stop_words/stop_words_en.txt data/pan15/english
python src/ef_links.py data/pan15/english
python src/ef_list_baseline.py -p lb_reyes data/pan15/english data/SentimentAnalysisDict/en/Reyes/counterFactuality-english.txt data/SentimentAnalysisDict/en/Reyes/temporalCompression-english.txt
python src/ef_list_frequency.py -p lf_reyes data/pan15/english data/SentimentAnalysisDict/en/Reyes/counterFactuality-english.txt data/SentimentAnalysisDict/en/Reyes/temporalCompression-english.txt

# Emoticons y puntuación
python src/ef_list_emoticons.py data/pan15/english data/emoticons.txt
python src/ef_list_punctuation.py data/pan15/english data/punctuation.txt

# Sentiword
python src/ef_sentiword.py data/pan15/english data/SentimentAnalysisDict/en/SWN/sentiword-net_en.tsv

#python src/ef_list_baseline.py -p lb_hu data/pan15/english data/SentimentAnalysisDict/en/Hu-Liu/positives.txt data/SentimentAnalysisDict/en/Hu-Liu/negatives.txt
python src/ef_list_frequency.py -p lf_hu data/pan15/english data/SentimentAnalysisDict/en/Hu-Liu/positives.txt data/SentimentAnalysisDict/en/Hu-Liu/negatives.txt

python src/ef_wissell_t.py data/pan15/english/ data/SentimentAnalysisDict/en/Whissell/whissell_en.txt

python src/develop.py --estimators 400 -m ${mode} -v data/pan15/english

#!/bin/bash

mode=0
while getopts t opt; do
	case $opt in
	t)
	mode=1
    ;;
	esac
	done
shift $(($OPTIND - 1))

# ------------  Based on vocabulary
# tfidf
if [ $mode -eq 0 ]; 
then
	python src/ef_tfidf.py -d $2 --stopwords data/stop_words/stop_words_en.txt $1
else
	python src/ef_tfidf.py -d $2 --vect $2/tfidf.vec --stopwords data/stop_words/stop_words_en.txt $1
fi

# Extrae links
if [ $mode -eq 0 ]; 
then
	python src/ef_links.py -d $2 $1
else
	python src/ef_links.py -d $2 -l $2/links.vec $1
fi

# ------------ Bades on lists
# Usando listas de positivos y negativos
python src/ef_list_baseline.py -d $2 -p lb_reyes $1 data/SentimentAnalysisDict/en/Reyes/counterFactuality-english.txt data/SentimentAnalysisDict/en/Reyes/temporalCompression-english.txt
python src/ef_list_frequency.py -d $2 -p lf_reyes $1 data/SentimentAnalysisDict/en/Reyes/counterFactuality-english.txt data/SentimentAnalysisDict/en/Reyes/temporalCompression-english.txt

#python src/ef_distance.py -d $2 $1

# Usando listas de polarity
python src/ef_polarity.py -d $2 $1 data/SentimentAnalysisDict/en/polarity-AFINN.txt

# Emoticons y puntuación
python src/ef_list_emoticons.py -d $2 $1 data/emoticons.txt
python src/ef_list_punctuation.py -d $2 $1 data/punctuation.txt

# Sentiword
python src/ef_sentiword.py -d $2 $1 data/SentimentAnalysisDict/en/SWN/sentiword-net_en.tsv

# Lista de Whissell
python src/ef_wissell_t.py -d $2 $1/ data/SentimentAnalysisDict/en/Whissell/whissell_en.txt

# Stadistica de corpus
python src/ef_statistics.py -d $2  $1

cp -r $1 $2
FILE=`basename $1`
python src/extract_text.py $2/$FILE
bash script/tag_english.sh $2/$FILE
if [ $mode -eq 0 ]; 
then
	python src/ef_pos.py --ngram 1 --tag 2 -d $2 $2/$FILE
else
	python src/ef_pos.py --vect $2/pos.vec --ngram 1 --tag 2 -d $2 $2/$FILE
fi

rm -rf $2/$FILE

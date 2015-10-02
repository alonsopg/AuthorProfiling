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
	python src/ef_tfidf.py -d $2 --stopwords data/stop_words/stop_words_it.txt $1
else
	python src/ef_tfidf.py -d $2 --vect $2/tfidf.vec --stopwords data/stop_words/stop_words_it.txt $1
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
python src/ef_list_baseline.py -d $2 -p lb_reyes $1 data/SentimentAnalysisDict/it/Reyes/counterFactuality-ita.txt data/SentimentAnalysisDict/it/Reyes/temporalCompression-ita.txt
python src/ef_list_frequency.py -d $2 -p lf_reyes $1 data/SentimentAnalysisDict/it/Reyes/counterFactuality-ita.txt data/SentimentAnalysisDict/it/Reyes/temporalCompression-ita.txt

# Usando listas de polarity
python src/ef_polarity.py -d $2 --deli '#' $1 data/SentimentAnalysisDict/it/afinn-v1.txt


#python src/ef_distance.py -d $2 $1

# Emoticons y puntuación
python src/ef_list_emoticons.py -d $2 $1 data/emoticons.txt
python src/ef_list_emoticons.py -d $2 $1  data/SentimentAnalysisDict/it/taboowords_it.txt
python src/ef_list_punctuation.py -d $2 $1 data/punctuation.txt

# Sentiword
python src/ef_sentiword_it.py -d $2 $1 data/SentimentAnalysisDict/it/SWN/SentiWN_it.tsv

# Lista de Whissell
python src/ef_wissell_t.py -d $2 $1/ data/SentimentAnalysisDict/it/Whissell/whissell-v1.txt

# Stadistica de corpus
python src/ef_statistics.py  -d $2 $1

# POS
cp -r $1 $2
FILE=`basename $1`
python src/extract_text.py $2/$FILE
bash script/tag_italian.sh $2/$FILE
if [ $mode -eq 0 ]; 
then
	python src/ef_pos.py -d $2 --tag 1 $2/$FILE
else
	python src/ef_pos.py --vect $2/pos.vec --tag 1 -d $2 $2/$FILE
fi
rm -rf $2/$FILE



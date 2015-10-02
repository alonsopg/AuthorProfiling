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
	python src/ef_tfidf.py -d $2 --stopwords data/stop_words/stop_words_du.txt $1
else
	python src/ef_tfidf.py -d $2 --vect $2/tfidf.vec --stopwords data/stop_words/stop_words_du.txt $1
fi

# Extrae links
if [ $mode -eq 0 ]; 
then
	python src/ef_links.py -d $2 $1
else
	python src/ef_links.py -d $2 -l $2/links.vec $1
fi

# Usando listas de polarity
python src/ef_polarity.py -d $2  $1 data/SentimentAnalysisDict/du/polarity-AFINN.txt

#python src/ef_distance.py -d $2 $1

# Emoticons y puntuación
python src/ef_list_emoticons.py -d $2 $1 data/emoticons.txt
python src/ef_list_punctuation.py -d $2 $1 data/punctuation.txt

# Stadistica de corpus
python src/ef_statistics.py -d $2  $1

# POS
cp -r $1 $2
FILE=`basename $1`
python src/extract_text.py $2/$FILE
bash script/tag_dutch.sh $2/$FILE
if [ $mode -eq 0 ]; 
then
	python src/ef_pos.py -d $2 --tag 1 $2/$FILE
else
	python src/ef_pos.py --vect $2/pos.vec --tag 1 -d $2 $2/$FILE
fi
rm -rf $2/$FILE



#!/bin/bash
DIR=xmlToJson_es/
if [ ! -d "$DIR" ]
then
mkdir $DIR
fi
DIR2=xmlToJson_en/
if [ ! -d "$DIR2" ]
then
mkdir $DIR2
fi
DIR3=../data/tweets_es/
if [ ! -d "$DIR3" ]
then
mkdir $DIR3
fi
DIR4=../data/tweets_en/
if [ ! -d "$DIR4" ]
then
mkdir $DIR4
fi
echo "instalando dependencias"
npm install
echo "dependencias instaladas"
if [ -d "../data/pan14_english" ]
then
echo "Conviertiendo xml_en..."
node xmlReader.js ../data/pan14_english/ xmlToJson_en/
fi
if [ -d "../data/pan14_spanish " ]
then
echo "Conviertiendo xml_es..."
node xmlReader.js ../data/pan14_spanish/ xmlToJson_es/
fi
echo "Descargando y Escribiendo tweets en ingles..."
FILES_EN=xmlToJson_en/*
for f in $FILES_EN
do 
node readTweets.js $f ../data/tweets_en/
done
#FILES_ES=xmlToJson_es/*
#for f1 in $FILES_ES
#do
#node readTweets.js $f1 --/data/tweets_es/
#done
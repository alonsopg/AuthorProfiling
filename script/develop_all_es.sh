#!/bin/bash

mode="gender"
est=1000
echo "Running training authorprof"
while getopts m: opt; do
	case $opt in
	m)
	mode=$OPTARG
    ;;
	e)
	est=$OPTARG
	;;
	
	esac
	done

bash script/extract_es.sh $@

# gender
python src/develop.py -v --estimators ${est} -v data/pan15/spanish
python src/develop.py -v --estimators ${est}  -m age -w weights/es_gender.txt -v data/pan15/spanish
python src/develop.py -v --estimators ${est}  -m ex -v data/pan15/spanish
python src/develop.py -v --estimators ${est}  -m st -v data/pan15/spanish
python src/develop.py -v --estimators ${est}  -m op -v data/pan15/spanish
python src/develop.py -v --estimators ${est}  -m co -v data/pan15/spanish
python src/develop.py -v --estimators ${est}  -m agre -v data/pan15/spanish



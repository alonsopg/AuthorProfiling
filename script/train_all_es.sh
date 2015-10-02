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

rm $2/*
bash script/extract_es.sh $@

# gender
python src/train.py --model model_ge.model -d $2 --estimators ${est} -v $1
python src/train.py --model model_age.model -d $2 --estimators ${est}  -m age -w weights/es_gender.txt -v $1
python src/train.py --model model_ex.model -d $2 --estimators ${est}  -m ex -v $1
python src/train.py --model model_st.model -d $2 --estimators ${est}  -m st -v $1
python src/train.py --model model_op.model -d $2 --estimators ${est}  -m op -v $1
python src/train.py --model model_co.model -d $2 --estimators ${est}  -m co -v $1
python src/train.py --model model_agr.model -d $2 --estimators ${est}  -m agre -v $1



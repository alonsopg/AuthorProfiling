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

bash script/extract_du.sh $@

# gender
python src/develop.py --estimators ${est} -v data/pan15/dutch
python src/develop.py --estimators ${est}  -m ex -v data/pan15/dutch
python src/develop.py --estimators ${est}  -m st -v data/pan15/dutch
python src/develop.py --estimators ${est}  -m op -v data/pan15/dutch
python src/develop.py --estimators ${est}  -m co -v data/pan15/dutch
python src/develop.py --estimators ${est}  -m agre -v data/pan15/dutch



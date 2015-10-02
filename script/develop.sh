#!/bin/bash

testdir=
model='feats'

echo "Running testing authorid"
while getopts i:o:m: opt; do
	case $opt in
	i)
		testdir=$OPTARG
		;;
	m)
		modeldir=$OPTARG
		;;
	o)
		outdir=$OPTARG
		;;
	esac
done

LANG=`ls ${testdir}/*.xml | head -1 | xargs grep lang`

if [[ $LANG == *"lang=\"en\""* ]]
then
	bash script/develop_all_en.sh ${testdir} ${model}
fi
if [[ $LANG == *"lang=\"es\""* ]]
then
	bash script/develop_all_es.sh ${testdir} ${model}
fi
if [[ $LANG == *"lang=\"it\""* ]]
then
	bash script/develop_all_it.sh ${testdir} ${model}
fi
if [[ $LANG == *"lang=\"nl\""* ]]
then
	bash script/develop_all_du.sh ${testdir} ${model}
fi



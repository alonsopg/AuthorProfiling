#!/bin/bash

testdir=

echo "Running training authorprof"
while getopts c:o:m: opt; do
	case $opt in
	c)
		testdir=$OPTARG
		;;
	o)
		outdir=$OPTARG
		;;
	esac
done

LANG=`ls ${testdir}/*.xml | head -1 | xargs grep lang`

if [[ $LANG == *"lang=\"en\""* ]]
then
	bash script/train_all_en.sh ${testdir} ${outdir}
	# Compreses model
	pushd ${outdir}
	tar -czvf /tmp/model_en.tgz .
	cp /tmp/model_en.tgz .
	popd
fi
if [[ $LANG == *"lang=\"es\""* ]]
then
	bash script/train_all_es.sh ${testdir} ${outdir}
	# Compreses model
	pushd ${outdir}
	tar -czvf /tmp/model_es.tgz .
	cp /tmp/model_es.tgz .
	popd
fi
if [[ $LANG == *"lang=\"it\""* ]]
then
	bash script/train_all_it.sh ${testdir} ${outdir}
	# Compreses model
	pushd ${outdir}
	tar -czvf /tmp/model_it.tgz .
	cp /tmp/model_it.tgz .
	popd

fi
if [[ $LANG == *"lang=\"nl\""* ]]
then
	bash script/train_all_du.sh ${testdir} ${outdir}
	# Compreses model
	pushd ${outdir}
	tar -czvf /tmp/model_du.tgz .
	cp /tmp/model_du.tgz .
	popd
fi



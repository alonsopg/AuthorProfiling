#!/bin/bash

mode="gender"
echo "Running training authorid"
while getopts m: opt; do
	case $opt in
	m)
	mode=$OPTARG
	;;
	esac
	done


rm feats/*.idx
rm feats/*.dat



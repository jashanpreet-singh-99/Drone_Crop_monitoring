#!/bin/bash

for file in ../rez_dataset/*
do
	echo "Processing: $file"
	((count = 0))
	for img in $file/*
	do
		img_n=$(basename $img)
		label=$(echo $img_n| cut -d "_" -f 1)
		ext=$(echo $img_n| cut -d "." -f 2)
		n_name=$(echo $label\_$count.$ext)
		echo $count $img $n_name
		mv $img $(echo ../rez_dataset/$file/$n_name)
		((count += 1))
	done
done

#!/bin/bash

echo 'Working On $1'
for file in ../$1/*
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
		mv $img $(echo ../$1/$file/$n_name)
		((count += 1))
	done
done

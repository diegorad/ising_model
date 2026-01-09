#! /bin/bash

calc(){ awk "BEGIN { print "$*" }"; }

nc=8 	#Parallel threads
min=0
max=1
nSteps=96

range="$(calc $max-$min)"
batch=$(($nSteps/$nc))

numStep="$(calc $range/$(($nSteps-1)))"

mkdir plot_serie

>output_D.txt

for i in $(seq 0 $(($batch-1)))
do
echo -ne $i"/"$batch"\r"
	for j in $(seq 0 $(($nc-1)))
	do
	 	step=$(($nc*$i+$j))
		val="$(calc $min+$step*$numStep)"
		echo $val "$(./findZero_ratio.sh $step $val)" >> output_D.txt&
	done
	wait
done

sort -n output_D.txt > output_D.txt.tmp
mv output_D.txt.tmp output_D.txt

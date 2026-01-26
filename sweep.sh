#! /bin/bash

calc() {
    echo "$*" | bc -l
}

nc=8 	#Parallel threads
min=-2
max=0
nSteps=48	#Must be divisible by nc

range="$(calc $max - $min)"
batch=$(($nSteps/$nc))

numStep="$(calc $range/$(($nSteps-1)))"

rm -r plot_serie 2> /dev/null
rm -r data_* 2> /dev/null
mkdir plot_serie 2> /dev/null

for i in $(seq 0 $(($batch-1)))
do
echo -ne $i"/"$batch"\r"
	for j in $(seq 0 $(($nc-1)))
	do
	 	step=$(($nc*$i+$j))
		val="$(calc $min+$step*$numStep)"
		./sweep_rutine.sh $step $val&
	done
	wait
done

sort -n output_D.txt > output_D.txt.tmp
mv output_D.txt.tmp output_D.txt

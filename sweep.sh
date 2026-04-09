#! /bin/bash

calc() {
    echo "$*" | bc -l
}

nc=8 	#Parallel threads
min=4
max=8
nSteps=96 	#Must be divisible by nc

range="$(calc $max - $min)"
batch=$(($nSteps/$nc))

numStep="$(calc $range/$(($nSteps-1)))"

#external_val=$1

rm -r plot_serie 2> /dev/null
rm -r output_serie 2> /dev/null
rm -r data_* 2> /dev/null
rm -f susceptibility.txt
rm -f avg_mag.txt
mkdir plot_serie 2> /dev/null
mkdir output_serie 2> /dev/null

#for i in $(seq 0 $(($batch-1)))
#do
#echo -ne $i"/"$batch"\r"
#	for j in $(seq 0 $(($nc-1)))
#	do
#	 	step=$(($nc*$i+$j))
#		val="$(calc $min+$step*$numStep)"
#		./sweep_rutine.sh $step $val&
#	done
#	wait
#done
#

MAX_WORKERS=4
running_pids=""
counter=0

function spawn_process() {
    "$@" &
    
#    echo $(jobs -rp | wc -l)
    while [[ $(jobs -rp | wc -l) -ge $MAX_WORKERS ]]; do
        wait -n
    done
}

#spawn_process ./sweep_rutine.sh 0 6
#spawn_process ./sweep_rutine.sh 1 5
#spawn_process ./sweep_rutine.sh 2 4
#spawn_process ./sweep_rutine.sh 3 3
#spawn_process ./sweep_rutine.sh 4 6
#spawn_process ./sweep_rutine.sh 5 5
#spawn_process ./sweep_rutine.sh 6 4
#spawn_process ./sweep_rutine.sh 7 3

while read F  ; do
        echo $F
        counter=$(($counter+1))
        spawn_process ./sweep_rutine.sh $counter $F
done <./batch_values.dat

wait

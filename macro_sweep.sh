#! /bin/bash

rm -rf run
mkdir run

counter=0

while read val  ; do
		printf "\r"
        echo "Macro $counter: $val"
        time srun --partition=hour --cpus-per-task=11 ./sweep.sh $counter $val < /dev/null
        counter=$(($counter+1))
        wait
done <./macro_values.dat

#Spinner for last one
#spinner



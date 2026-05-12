#! /bin/bash

rm -rf run
mkdir run

counter=0

while read val  ; do
		printf "\r"
        echo "Macro $counter: $val"
        #Field
	    ./fieldgen.py --mode half_loop --range 2 --rate $val > /dev/null
	    
#        time srun --partition=hour --cpus-per-task=11 ./sweep.sh $counter $val < /dev/null
		./sweep.sh $counter $val
#		./optimize.py --column 1 --ext_val $val --index $counter < /dev/null

		#Process
		./average.py --files --dir ./run/run_$counter/output_bin_serie/ > /dev/null
		echo "$val $(./findZero.py --file ./run/run_$counter/averaged_output.txt  --column 1) $(./findZero.py --file ./run/run_$counter/averaged_output.txt --column 2)" >> zeros.txt
		
        counter=$(($counter+1))
        wait
done <./macro_values.dat

#Spinner for last one
#spinner



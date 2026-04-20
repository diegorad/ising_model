#! /bin/bash

calc() {
    echo "$*" | bc -l
}

int() {
	echo $(printf "%.0f" $val)
}

#external_val=$3
#external_val=$( printf "%.0f" $3 )

mkdir -p ./run/data_serie/data_$1

cp *.py ./run/data_serie/data_$1
cp tools.* ./run/data_serie/data_$1
cp ising_model ./run/data_serie/data_$1
cp *.dat ./run/data_serie/data_$1

cd ./run/data_serie/data_$1

printf -v val "%0.5f" $2

val1="$(calc 0.5 + 0*$2)"
val2="$(calc $2*0.5 - 1.2)"
int_val="$(int $val)"
	
#	./fieldgen.py --mode const --range $val --steps 5000 >/dev/null
#	./netgen.py --S_0 7 --ratio 0 --size $int_val >/dev/null
#	./netgen.py --S_0 1 --S_1 4 --size 23 --type 'shell' --replacement 0.24 --layers 6 | grep 'Ratio =' | cut -d'=' -f2 | xargs >> ../out.txt
#	python3 growNet.py --size 500 --S_0 1 --S_1 4 --ratio 0.34 --replacement 0.2 >/dev/null
    
	./ising_model --J_ij="{0, 6, 0}" --D_i="{0, 0}" --out=output --T $val --init=sat --seed=$1 > output.txt
	cp output.txt ../../output_serie/out_$1.txt
	
	#Bin points
	./average.py --mode bin --bin_size 0.01 > output.tmp
	mv output.tmp output.txt
	
	#Susceptibility
#	echo "$val $(./average.py -s --T $val --size 50 --trim)" >> ../../susceptibility.txt
	
#	echo "$val $(./average.py -s --T 6 --size 50 --trim)" >> ../../magcurve.txt
		
	#Plot
	python3 plot.py --savefig --label "T=$val"
	cp plot.png ../../plot_serie/plot_$1.png
	
	#Zero
	echo "$2 $(./findZero.py)" >> ../../zeros.txt
	
#	cp output.txt ../../output_bin_serie/out_$1.txt
#	echo "$2 $(python3 average.py -s --trim --T 6 --size 50)" >> ../../susceptibility.txt


cd ../
#rm -r data_$1

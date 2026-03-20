#! /bin/bash

calc() {
    echo "$*" | bc -l
}

#external_val=$3
#external_val=$( printf "%.0f" $3 )

mkdir data_$1

cp *.py ./data_$1
cp tools.* ./data_$1
cp ising_model ./data_$1
cp *.dat ./data_$1

cd data_$1

printf -v val "%0.5f" $2

	val1="$(calc 0.5 + 0*$2)"
	val2="$(calc $2*0.5 - 1.2)"
	
#	./fieldgen.py --rate 0.01 --range 2.5 >/dev/null
	./netgen.py --S_0 1 --S_1 4 --size 25 --type 'shell' --replacement 0.25 --layers 6 >/dev/null
#	./netgen.py --S_0 1 --S_1 4 --size 23 --type 'shell' --replacement 0.24 --layers 6 | grep 'Ratio =' | cut -d'=' -f2 | xargs >> ../out.txt
#	python3 growNet.py --size 500 --S_0 1 --S_1 4 --ratio 0.34 --replacement 0.2 >/dev/null
    
	./ising_model --J_ij="{3.5, 0.2, -1.5}" --D_i="{0, -0.58}" --out=output --seed=$1 > output.txt
#	echo "$val $(python3 average.py --susceptibility --T $val)" >> ../susceptibility.txt
#	python3 plot.py --total --savefig --label "Ratio=$val"
#	cp plot.png ../plot_serie/plot_$1.png
	cp output.txt ../output_serie/out_$1.txt

cd ../
rm -r data_$1

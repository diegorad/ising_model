#! /bin/bash

calc() {
    echo "$*" | bc -l
}

mkdir data_$1

cp *.py ./data_$1
cp tools.* ./data_$1
cp ising_model ./data_$1
cp *.dat ./data_$1

cd data_$1

printf -v val "%0.5f" $2

	val1="$(calc 0.5 + 0*$2)"
	val2="$(calc $2*0.5 - 1.2)"
	
	./fieldgen.py --rate 0.01 --range 2.5 >/dev/null
	python3 netgen.py --ratio 0.2 --S_0 1 --S_1 2 --size 50 >/dev/null
#	python3 growNet.py --size 250 --S_0 1 --S_1 3 >/dev/null

	./ising_model --J_ij="{3.4, 0.37, -2.75}" --D_i="{0, -1.77}" --out=output --seed=$1 > output.txt
#	echo "$val $(python3 average.py --susceptibility --T $val)" >> ../susceptibility.txt
#	python3 plot.py --total --savefig --label "Ratio=$val"
#	cp plot.png ../plot_serie/plot_$1.png
	cp output.txt ../output_serie/out_$1.txt

cd ../
rm -r data_$1

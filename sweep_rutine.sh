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

#	python3 netgen.py --ratio $val --size 50 --S_0 1 --S_1 4 --periodic >/dev/null
	python3 growNet.py --size 600 --S_0 1 --S_1 3 --replacement 0 >/dev/null

	./ising_model --J_ij="{2.7, -1, 1}" --D_i="{0, 0}" --out=output --seed=$1 > output.txt
#	echo "$val $(python3 average.py --susceptibility --T $val)" >> ../susceptibility.txt
#	python3 plot.py --total --savefig --label "Ratio=$val"
#	cp plot.png ../plot_serie/plot_$1.png
	cp output.txt ../output_serie/out_$1.txt

cd ../
rm -r data_$1

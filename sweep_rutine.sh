#! /bin/bash

calc() {
    echo "$*" | bc -l
}

mkdir data_$1

cp netgen.py ./data_$1
cp tools.* ./data_$1
cp ising_model ./data_$1
cp findZero.py ./data_$1
cp plot.py ./data_$1
cp *.dat ./data_$1
cp fieldgen.py ./data_$1

cd data_$1

printf -v val "%0.5f" $2

	python3 netgen.py --S_0 7 --ratio 0.05 >/dev/null
	val1="$(calc 0.5 + 0*$2)"
	val2="$(calc 0 - 1*$2)"

	./ising_model --J_ij="{0.145, 2.3, $2}" --D_i="{-0.376, 0}" --out=output --seed=$1 > output.txt
#	echo $(python3 findZero.py $1)
	python3 plot.py --savefig --label "$val"
	cp plot.png ../plot_serie/plot_$1.png

cd ../
rm -r data_$1

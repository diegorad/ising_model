#! /bin/bash

mkdir data_$1

cp netgen.py ./data_$1
cp tools.* ./data_$1
cp ising_model ./data_$1
cp findZero.py ./data_$1
cp plot.py ./data_$1
cp *.dat ./data_$1

cd data_$1

printf -v val "%0.2f" $2

	python3 netgen.py 0.55 >/dev/null
	./ising_model --out=output --D_i="{-0.2, 0}" --J_ij="{0.05, 0.85, $2}" --seed=$1 > output.txt
#	echo $(python3 findZero.py $1)
	python3 plot.py --savefig --label "J_12=$val"
	cp plot.png ../plot_serie/plot_$1.png

cd ../
rm -r data_$1

#! /bin/bash

mkdir data_$1

cp netgen.py ./data_$1
cp tools.* ./data_$1
cp ising_model ./data_$1
cp findZero.py ./data_$1
cp plot.py ./data_$1

cd data_$1

	python3 netgen.py $2 >/dev/null
	./ising_model --out=output --D="{0,0}" --seed=$1 > output.txt
	echo $(python3 findZero.py $1)
#	python3 plot.py
#	cp plot.png ../plot_serie/plot_$1.png

cd ../
rm -r data_$1

#! /bin/bash

./ising_model --out=output --D="{$2,0}" --seed=$1 > out_$1.txt
echo $(python3 findZero.py $1)
rm out_$1.txt

#! /bin/bash

./ising_model -o $1 $2 > out_$1.txt
echo $(python3 findZero.py $1)
rm out_$1.txt

#! /bin/bash

gcc -o ising_model ising_model.c tools.c utils.c -lm
./ising_model $1
python3 plot.py

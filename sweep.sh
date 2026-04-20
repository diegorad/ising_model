#! /bin/bash

MAX_WORKERS=2
running_pids=""
counter=0

calc() {
    echo "$*" | bc -l
}

#external_val=$1

spin='-\|/'

gcc -o ising_model ising_model.c tools.c utils.c cli.c -lm

rm -rf plot_serie
rm -rf output_serie
rm -rf data_serie
rm -rf run
rm -f susceptibility.txt
rm -f avg_mag.txt
mkdir -p ./run/plot_serie
mkdir ./run/output_serie
mkdir ./run/output_bin_serie

function spinner() {
    i=0
    while :; do
        any_running=false

        for p in "${pids[@]}"; do
            if kill -0 "$p" 2>/dev/null; then
                any_running=true
                break
            fi
        done

        $any_running || break

        i=$(( (i+1) % 4 ))
        printf "\r${spin:$i:1}"
        sleep 0.1
    done
    printf "\r"
}

function spawn_process() {
    "$@" &
    pid=$!
    pids+=($pid)
    
    while [[ $(jobs -rp | wc -l) -ge $MAX_WORKERS ]]; do
        spinner
        wait -n
    done
}

while read F  ; do
		printf "\r"
        echo "$counter: $F"
        counter=$(($counter+1))
        spawn_process ./sweep_rutine.sh $counter $F
done <./batch_values.dat

#Spinner for last one
spinner

wait

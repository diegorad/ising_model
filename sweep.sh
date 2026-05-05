#! /bin/bash

MAX_WORKERS=8
running_pids=""
counter=0

calc() {
    echo "$*" | bc -l
}

macro_index=$1
printf -v macro_value "%0.5f" $2

run_dir="./run/run_$macro_index"
spin='-\|/'

gcc -o ising_model ising_model.c tools.c utils.c cli.c -lm

#rm -rf plot_serie
#rm -rf output_serie
#rm -rf data_serie
rm -rf $run_dir
#rm -f susceptibility.txt
#rm -f avg_mag.txt
mkdir -p $run_dir/plot_serie
mkdir $run_dir/output_serie
mkdir $run_dir/output_bin_serie

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

while read val  ; do
		printf -v val "%0.5f" $val
		printf "\r"
        echo "$counter: $val"
        counter=$(($counter+1))
        spawn_process ./sweep_rutine.sh $macro_index $counter $val $macro_value
done <./batch_values.dat

#Spinner for last one
spinner

wait

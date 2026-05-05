#! /bin/bash

calc() {
    echo "$*" | bc -l
}

int() {
	echo $(printf "%.0f" $val)
}

#external_val=$3
#external_val=$( printf "%.0f" $3 )

macro_index=$1
macro_value=$4
run_dir="./run/run_$macro_index"

mkdir -p $run_dir/data_serie/data_$2

cp *.py $run_dir/data_serie/data_$2
cp tools.* $run_dir/data_serie/data_$2
cp ising_model $run_dir/data_serie/data_$2
cp *.dat $run_dir/data_serie/data_$2
cp -r ./data_* $run_dir/data_serie/data_$2

cd $run_dir/data_serie/data_$2

printf -v val "%0.5f" $3
printf -v macro_val "%0.5f" $macro_value

aux_val="$(calc -0.177599 - 2.15532*$val)"
val2="$(calc $3*0.5 - 1.2)"
int_val="$(int $val)"
	
	#Optimize
	./optimize.py --column 1 --ext_val $val > ../../opt_result_$2.txt
	#Plot Error
	./error.py --dir data_Fe --mode half_loop --norm range --scale 0.181 --savefig --label "$val"
	cp plot.png ../../plot_serie/error_$val.png
	
#	./fieldgen.py --mode const --range $val --steps 5000 >/dev/null
#	./netgen.py --S_0 7 --ratio 0 --size $int_val >/dev/null
#	./netgen.py --S_0 1 --S_1 4 --size 23 --type 'shell' --replacement 0.24 --layers 6 | grep 'Ratio =' | cut -d'=' -f2 | xargs >> ../out.txt
#	python3 growNet.py --size 500 --S_0 1 --S_1 4 --ratio 0.34 --replacement 0.2 >/dev/null

	#Generate network
	#./netgen.py --S_0 4 --ratio 0 --size $int_val >/dev/null
	
#	#Run sim
#	echo "Val:$val Macro_val:$macro_val Aux_val:$aux_val" > values.txt    
#	./ising_model --J_ij="{$val, 4.6, 0}" --D_i="{$aux_val, 0}" --out=output --init=sat --seed=$2 > output.txt
#	cp output.txt ../../output_serie/out_$2.txt
	
#	#Bin points
#	./average.py --mode bin --bin_size 0.01 > output.tmp
#	mv output.tmp output.txt
#	cp output.txt ../../output_bin_serie/out_$2.txt
	
	#Plot
	python3 plot.py --savefig --label "$val"
	cp plot.png ../../plot_serie/plot_$2.png
	
	#Zero
#	echo "$3 $(./findZero.py --column 1) $(./findZero.py --column 2)" >> ../../zeros.txt
	
#	#Saturation value
#	echo "$val $(tail -n 1 output.txt)" >> ../../saturation.txt
	
	#Susceptibility
#	echo "$val $(./average.py -s --T $val --size 25 --trim)" >> ../../susceptibility.txt
	
#	echo "$val $(./average.py -s --T 6 --size 50 --trim)" >> ../../magcurve.txt
		
	
#	cp output.txt ../../output_bin_serie/out_$2.txt
#	echo "$3 $(python3 average.py -s --trim --T 6 --size 50)" >> ../../susceptibility.txt


cd ../
#rm -r data_$2

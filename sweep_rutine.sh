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
#macro_value_2=$5
#macro_value_3=$6
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
#printf -v macro_val_2 "%0.5f" $macro_value_2
#printf -v macro_val_3 "%0.5f" $macro_value_3

aux_val="$(calc -0.195313 - 3.15885*$val + 1.07552*$val*$val)"
int_val="$(int $val)"
	
#	#Plot Error
#	./error.py --dir data_Fe --mode half_loop --show --norm_sim False --scale_sim 0.0016 --norm_data False --scale_data 5.86 --savefig --label "$val"
#	cp plot.png ../../plot_serie/error_$val.png

	#Field
#	./fieldgen.py --mode const --range $val --steps 1e5 >/dev/null

#	#Generate network
	./netgen.py --S_0 2 --ratio 0 --size 50 >/dev/null

#	#Optimize
#	./optimize.py --column 1 --ext_val $val > ../../opt_result_$2.txt
	
#	#Run sim
#	echo "Val:$val Macro_val:$macro_val Macro_val_2:$macro_val_2 Macro_val_3:$macro_val_3 Aux_val:$aux_val" > values.txt
#	echo "$val, 4.4, -4.8, $aux_val, 0" > ../../parameters.txt    
	./ising_model --J_ij="{0, 4.6, 0}" --D_i="{0, 0}" --out=output --init=sat --seed=$2 > output.txt
#	cp output.txt ../../output_serie/out_$2.txt
	
#	#Bin points
	./average.py --mode bin --bin_size 0.01 > output.tmp
	mv output.tmp output.txt
	cp output.txt ../../output_bin_serie/out_$2.txt
	
	#Plot
#	fig_plot.py --save plot
	python3 plot.py --savefig --label "$val"
	cp plot.png ../../plot_serie/plot_$2.png
	
#	#Zero
	echo "$val $(./findZero.py --column 1) $(./findZero.py --column 2)" >> ../../zeros.txt
	
#	#Saturation value
#	echo "$val $(tail -n 1 output.txt)" >> ../../saturation.txt
	
	#Susceptibility
#	echo "$val $(./average.py -s --T $val --size 25 --trim)" >> ../../susceptibility.txt
	
	#Average on time	
#	echo "$val $(./average.py --mode time --trim 9e4)" >> ../../magcurve.txt
		
#	cp output.txt ../../output_bin_serie/out_$2.txt
#	echo "$3 $(python3 average.py -s --trim --T 6 --size 50)" >> ../../susceptibility.txt

	rm field.dat
cd ../
#rm -r data_$2

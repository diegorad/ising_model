#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>

#include "tools.h"
#include "utils.h"
#include "cli.h"

#define CLEAR_SCREEN "\033[2J"
#define CURSOR_HOME  "\033[H"
#define HIDE_CURSOR  "\033[?25l"
#define SHOW_CURSOR  "\033[?25h"

#define lattice_size 50
    
int main(int argc, char *argv[])
{	
	//Default parameter values
	Config cfg = {
		    .out_mode = OUT_PLOT,
		    .D_i = {0.0, 0.0},
		    .J_ij = {0.1, 1.0, -0.75},
		    .seed = 0
	};
    
	int rc = parse_args(argc, argv, &cfg);
    if (rc != 0) {
        if (rc > 0) return 0;
        return 1;
    }
    
	int **neighbors;
	Node *nodes;
	int L = 2*lattice_size*(lattice_size-1);
	int N = lattice_size*lattice_size;
	int numberOfIterations = 1e3;
	double fieldRange = 5;
	double h=0;
	double k_B = 1.0, T = 1.0;
	double rampRate = fieldRange/(numberOfIterations/5);
	int i,j,iter;
	double energy, energy_flip, delta_energy, P;
	bool event, latch = false;
	FILE *f;

	srand(time(NULL)+cfg.seed);
	
	//Output file
	f = fopen("output.txt", "w");
	
	//Load nodes
	nodes = loadNodes("nodes.dat", N);
	
	//Load neighbors
	neighbors = loadIntegerList("neighbors.dat", N, 4);

	//Initialize spins
	for(i=0;i<N;i++){
		int random_index = rand() % (nodes[i].spin_value + 1);
		nodes[i].spin = nodes[i].spin_z[random_index];
	}
	
	//PLOT BEGIN
	if(cfg.out_mode == 2){
		printf(CLEAR_SCREEN);
		fflush(stdout);	
	}
	
	for(iter = 0;iter<numberOfIterations;iter++){
		//PLOT
		if(cfg.out_mode == 2){
			if (iter % 5 == 0){
				printf(CURSOR_HOME);
				print_lattice(nodes, lattice_size);
			}
		}
		
		//OUTPUT
		if(cfg.out_mode == 1)
			printf("%lf %d %d\n", h, sumSpins(N, nodes, 0), sumSpins(N, nodes, 1));
		else
			fprintf(f, "%lf %d %d\n", h, sumSpins(N, nodes, 0), sumSpins(N, nodes, 1));
		
		for(i=0;i<N;i++){
			int newSpin = -999;
			j = rand()%N;
			energy = E(j, false, &newSpin, neighbors, nodes, h, cfg.D_i, cfg.J_ij);
			energy_flip = E(j, true, &newSpin, neighbors, nodes, h, cfg.D_i, cfg.J_ij);
			delta_energy = energy_flip - energy;
			
			event = randDouble(0, 1) <= boltzmann(delta_energy, k_B, T);
			
			if(delta_energy <= 0 || event){
				if(newSpin == -999){
					printf("Error while spin flipping. \n");
					exit(1);
				}
				nodes[j].spin = newSpin;
			}
		}		
				
		if(h < fieldRange && latch == false)
			h += rampRate;
		else{
			h -= rampRate;
			latch = true;
		}
		
		if(h < -fieldRange)
			latch = false;
		
		//MONITOR
		if(cfg.out_mode == 0 || cfg.out_mode == 2)
			if (iter % 5 == 0){
				printf("Step: %d  H: %.3f\r", iter, h);
				if(cfg.out_mode == 2){
					fflush(stdout);
					usleep(100000);
				}
			}	
	}
	
	//Clear
	if(cfg.out_mode == 0)
		printf("\r");
	
	//Close output file
	fclose(f); 
	
	//PLOT END
	if(cfg.out_mode == 2){
		printf(CLEAR_SCREEN CURSOR_HOME SHOW_CURSOR);
	}
}

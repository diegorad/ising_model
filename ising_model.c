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
 
int main(int argc, char *argv[])
{	
	//Default parameter values
	Config cfg = {
		    .out_mode = OUT_PLOT,
		    .D_i = {0.0, 0.0},	//57.88 μeV
		    .J_ij = {1.0, 3.0, -2.0},	//57.88 μeV
		    .seed = 0,
		    .T = 6.0	//T=1 ~ 0.672 K
	};
    
	int rc = parse_args(argc, argv, &cfg);
    if (rc != 0) {
        if (rc > 0) return 0;
        return 1;
    }
    
	int **neighbors;
	Node *nodes;
	int N;
	int numberOfIterations;
	double *fieldRoutine;
	double B=0;	// [B]=[57.88 μeV] so that B=1 ~ 1 T (57.88 μeV/mu_B)
	double k_B = 1.0; // [T]=[57.88 μeV]
	int i,j;
	double energy, energy_flip, delta_energy;
	bool event;
	FILE *f;

	srand(time(NULL)+cfg.seed);
	
	//Output file
	f = fopen("output.txt", "w");
	
	//Load nodes
	nodes = loadNodes("nodes.dat", &N);
	
	//Load neighbors
	neighbors = loadIntegerList("neighbors.dat", N, 4);
	
	//Initialize spins
	for(i=0;i<N;i++){
		int random_index = rand() % (nodes[i].spin_value + 1);
		nodes[i].spin = nodes[i].spin_z[random_index];
	}
	
	//Load field routine
	fieldRoutine = loadFloatList("field.dat", &numberOfIterations);
	
	//PLOT BEGIN
	if(cfg.out_mode == 2){
		printf(CLEAR_SCREEN);
		fflush(stdout);	
	}
	
	for(int iter = 0;iter<numberOfIterations;iter++){
		//Field routine
		B = fieldRoutine[iter];
	
		//PLOT
		if(cfg.out_mode == 2){
			if (iter % 5 == 0){
				printf(CURSOR_HOME);
				print_lattice(nodes, sqrt(N));
			}
		}
		
		//OUTPUT
		if(cfg.out_mode == 1)
			printf("%lf %d %d\n", B, sumSpins(N, nodes, 0), sumSpins(N, nodes, 1));
		else
			fprintf(f, "%lf %d %d\n", B, sumSpins(N, nodes, 0), sumSpins(N, nodes, 1));
		
		for(i=0;i<N;i++){
			int newSpin = -999;
			j = rand()%N;
			energy = E(j, false, &newSpin, neighbors, nodes, B, cfg.D_i, cfg.J_ij);
			energy_flip = E(j, true, &newSpin, neighbors, nodes, B, cfg.D_i, cfg.J_ij);
			delta_energy = energy_flip - energy;
			
			event = randDouble(0, 1) <= boltzmann(delta_energy, k_B, cfg.T);
			
			if(delta_energy <= 0 || event){
				if(newSpin == -999){
					printf("Error while spin flipping. \n");
					exit(1);
				}
				nodes[j].spin = newSpin;
			}
		}		
		
		//MONITOR
		if(cfg.out_mode == 0 || cfg.out_mode == 2)
			if (iter % 5 == 0){
				printf("Step: %d  B: %.3f\r", iter, B);
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

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
		    .out_mode = OUT_MONITOR,
		    .init_mode = RAND, //Spin initialization
		    .D_i = {-0.5, 0.0},	//57.88 μeV
		    .J_ij = {0.2, 2.7, -1.5},	//57.88 μeV
		    .seed = 0,
		    .T = -1,	//T=-1 flags no T overwriting from --T argument
		    .xrate = 0
	};
    
	int rc = parse_args(argc, argv, &cfg);
    if (rc != 0) {
        if (rc > 0) return 0;
        return 1;
    }
    
	int **neighbors;
	Node *nodes;
	int N;
	int neighbors_lenght;
	int numberOfIterations;
	double **routine;
	double B = 0;	// [B]=[57.88 μeV] so that B=1 ~ 1 Tesla (57.88 μeV/mu_B)
	double k_B = 1.0; // [T]=[57.88 μeV]
	double T = 0; //T=1 ~ 0.672 K, T_real = T*(57.88 μeV/k_B_real)
	int i,j;
	double energy, energy_flip, delta_energy, total_energy;
	bool event, event_x;
	FILE *f;

	srand(time(NULL)+cfg.seed);
	
	//Output file
	f = fopen("output.txt", "w");
	
	//Load nodes
	nodes = loadNodes("nodes.dat", &N);
	
	//Load neighbors
	neighbors = loadIntegerList("neighbors.dat", &N, &neighbors_lenght);
	
	//Initialize spins
	for(i=0;i<N;i++){
		int random_index = rand() % (nodes[i].spin_value + 1);
		if(cfg.init_mode == 0)
			nodes[i].spin = nodes[i].spin_z[random_index]; //Random 
		else if(cfg.init_mode == 1)
			nodes[i].spin = nodes[i].spin_value; //All up
		else if(cfg.init_mode == 2)
			nodes[i].spin = -nodes[i].spin_value; //All down
	}
	
	//Load field routine
	routine = loadFloatList("field.dat", &numberOfIterations);
	
	//PLOT BEGIN
	if(cfg.out_mode == 2){
		printf(CLEAR_SCREEN);
		fflush(stdout);	
	}
	
	for(int iter = 0;iter<numberOfIterations;iter++){
		B = routine[iter][0];	//Field routine
		
		if(cfg.T == -1)
			T = routine[iter][1];	//Temperature routine
		else
			T = cfg.T;
	
		//PLOT
		if(cfg.out_mode == 2){
			if (iter % 5 == 0){
				printf(CURSOR_HOME);
				print_lattice(nodes, sqrt(N));
			}
		}
		
		//Total energy
		total_energy = total_E(N, neighbors, neighbors_lenght, nodes, B, cfg.D_i, cfg.J_ij);
		
		//OUTPUT
		if(cfg.out_mode == 1)
			printf("%lf %d %d\n", B, sumSpins(N, nodes, 0), sumSpins(N, nodes, 1));
		else
			fprintf(f, "%lf %d %d\n", B, sumSpins(N, nodes, 0), sumSpins(N, nodes, 1));
		
		for(i=0;i<N;i++){
			int newSpin = -999;
			j = rand()%N;
			energy = E(j, false, &newSpin, neighbors, neighbors_lenght, nodes, B, cfg.D_i, cfg.J_ij);
			energy_flip = E(j, true, &newSpin, neighbors, neighbors_lenght, nodes, B, cfg.D_i, cfg.J_ij);
			delta_energy = energy_flip - energy;
			
			event = randDouble(0, 1) <= boltzmann(delta_energy, k_B, T);
//			event_x = randDouble(0, 1) <= cfg.xrate;
			
			if(delta_energy <= 0 || event){
				if(newSpin == -999){
					printf("Error while spin flipping. \n");
					exit(1);
				}
				nodes[j].spin = newSpin;
			}
			
//			if(event_x){
//				if(newSpin == -999){
//					printf("Error while spin flipping. \n");
//					exit(1);
//				}
//				nodes[j].spin = newSpin;
//			}
		}		
		
		//MONITOR
		if(cfg.out_mode == 0 || cfg.out_mode == 2)
			if (iter % 5 == 0){
				printf("Step: %d  B: %.3f  T: %.3f\r", iter, B, T);
				if(cfg.out_mode == 2){
					fflush(stdout);
					usleep(100000);
				}
			}	
	}
	
	//Clear
	if(cfg.out_mode == 0){
		printf("\r");
		printf("J_ij: {%.3f, %.3f, %.3f}, D_i: {%.3f, %.3f}\n", cfg.J_ij[0], cfg.J_ij[1], cfg.J_ij[2], cfg.D_i[0], cfg.D_i[1]);	
	}
	
	//Close output file
	fclose(f); 
	
	//PLOT END
	if(cfg.out_mode == 2){
		printf(CLEAR_SCREEN CURSOR_HOME SHOW_CURSOR);
	}
}

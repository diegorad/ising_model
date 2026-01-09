#include "utils.h"

double  E(int i, bool flip, int *newSpin, int **neighbors, Node *nodes, double h, double D_0){
	int j, spin;
	int len = nodes[i].spin_value + 1;
	double sum = 0;
	double energy = 0;
	double J, D;
	double J_ij[] = {0.1, 1, -0.75}; //J: AA, BB, AB||BA
	double D_i[] = {D_0, 0};
	
	//Spin flipping
	spin = nodes[i].spin;
	if(flip){
		do{
			int random_index = rand() % len;
			*newSpin = nodes[i].spin_z[random_index];
		} while(*newSpin == spin);
		
		spin = *newSpin;
	}
	
	D = D_i[nodes[i].type];
		
	//Sum of neighboring spins
	for(j=0;j<4;j++){
		//Rules for anti-/-parallel coupling
		if(nodes[i].type == nodes[neighbors[i][j]].type)
			J = J_ij[nodes[i].type];
		else
			J = J_ij[2];
			
		if(neighbors[i][j] != -1)
			sum += J * nodes[neighbors[i][j]].spin;
	}
	
	energy = - spin * sum - h * spin - D * spin * spin;
	
	return energy;
}

double boltzmann(double delta_E, double k_B, double T){
	return exp(-delta_E / (k_B * T));
}

int sumSpins(int N, Node *nodes, int type)
{
	int i,sum = 0;

	for(i=0;i<N;i++){
		if(nodes[i].type == type)
			sum += nodes[i].spin;
	}
	
	return sum;
}

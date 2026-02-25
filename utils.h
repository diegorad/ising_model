#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "tools.h" 

double  E(int i, bool flip, int *newSpin, int **neighbors, Node *nodes, double h, double *D_i, double *J_ij);
double boltzmann(double delta_E, double k_B, double T);
int sumSpins(int N, Node *nodes, int type);
double total_E(int N, int **neighbors, Node *nodes, double B, double *D_i, double *J_ij);

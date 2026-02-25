#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#ifndef TOOLS_H
#define TOOLS_H

typedef struct {
    int index;
    int type;
    int spin_value;
    int *spin_z;
    int spin;
} Node;

#endif

int *createIntVector(int dim);
double *createVector(int dim);
int **createIntVectorList(int n, int m);
double **createVectorList(int n, int m);
Node* loadNodes(const char* filename, int *N);
double **loadFloatList(char *fileName, int *sizeOfArray);
int **loadIntegerList(char *fileName, int sizeOfArray, int dim);
double randDouble(double min, double max);
void exportList(int sizeOfArray, int dim, double **array, char *fileName);
void print_node(const Node* n);
void print_lattice(const Node* nodes, int L);
int parse_double_array(const char *s, double *arr, int n);

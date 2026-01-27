#include "tools.h"

// ANSI Escape prefixes
#define ESC     "\033["

#define RESET   "\033[0m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define BLUE    "\033[34m"
#define WHITE   "\033[37m"
#define YELLOW  "\033[33m"
#define MAG "\e[0;35m"

#define LOW0	"\033[38;5;74m"
#define MID0	"\033[38;5;242m"
#define HIGH0	"\033[38;5;113m"

#define LOW1	"\033[38;5;133m"
#define MID1	"\033[38;5;242m"
#define HIGH1	"\033[38;5;172m"


int *createIntVector(int dim)
{
	int *pf;
	if((pf=(int *)malloc(dim*sizeof(int)))==NULL){
		printf("Error allocating memory \n");
		exit(1);
	}

	return pf;
}

double *createVector(int dim)
{
double *pf;
	if((pf=(double *)malloc(dim*sizeof(double)))==NULL)
	{printf("Error allocating memory \n");
	exit(1);
	}

	return pf;
}

int **createIntVectorList(int n, int m){
	int **array;
	int i;
	
	if((array=(int **)malloc(n*sizeof(int*)))==NULL){
		printf("Error allocating memory \n");
		exit(1);
	}
	
	for(i=0;i<n;i++)
		array[i]=createIntVector(m);
	
	return array;
}

Node* loadNodes(const char* filename, int *N) {
    FILE* f = fopen(filename, "r");
    if (!f) return NULL;
	
	fscanf(f, "%d", N);
	
    Node* nodes = malloc(sizeof(Node) * *N);
    
    for (int i = 0; i < *N; i++) {
        fscanf(f, "%d %d %d",
               &nodes[i].index,
               &nodes[i].type,
               &nodes[i].spin_value);
        
        int len = nodes[i].spin_value + 1;       
        nodes[i].spin_z = malloc(sizeof(int) * len);

        for (int j = 0; j < len; j++) {
            nodes[i].spin_z[j] = -nodes[i].spin_value + 2*j;
    	}
	}
	
    fclose(f);
    return nodes;
}

double *loadFloatList(char *fileName, int *sizeOfArray)
{
	int i;
	double *list;
	FILE *input;
	
	if((input=fopen(fileName,"r"))==NULL)
	{
		printf("Cannot open file %s.\n", fileName);
		exit(1);
	}
	
	if(fscanf(input,"%d",&*sizeOfArray) != 1)
		printf("Error in %s file on line 1: Number of entries on file cannot be retrived.\n", fileName);
		
	list=createVector(*sizeOfArray);
	
	for(i=0;i<*sizeOfArray;i++)
	if(fscanf(input,"%le",&list[i])<=0)
		{printf("loadFloatList::Error allocating memory.\n");
		exit(1);
		}
		
	return list;
}

int **loadIntegerList(char *fileName, int sizeOfArray, int dim)
{
	int i,j;
	int **edgelist;
	FILE *input;

	if((input=fopen(fileName,"r"))==NULL)
	{
		printf("Cannot open file %s.\n", fileName);
		exit(1);
	}
	
/*	if(fscanf(input,"%d",&*sizeOfArray) != 1)*/
/*		printf("Error in %s, line 1: Number of entries on file is not specified.\n", fileName);*/
		
	edgelist=createIntVectorList(sizeOfArray, dim);

	for(i=0;i<sizeOfArray;i++)
		for(j=0;j<dim;j++)
			if(fscanf(input,"%d",&edgelist[i][j]) !=1)
				printf("Error in loadIntegerList function.\n");

	fclose(input);

	return edgelist;
}

double randDouble(double min, double max)
{
    return min + (rand() / (double)RAND_MAX) * (max - min);
}

void exportList(int sizeOfArray, int dim, double **array, char *fileName)
{
	int i,j;
	FILE *f=fopen(fileName, "w");
	if(f==NULL){
		printf("Error writing file!\n");
		exit(1);
	}

	for(i=0;i<sizeOfArray;i++){
		for(j=0;j<dim;j++)
			fprintf(f,"%le\t",array[i][j]);
		fprintf(f,"\n");
	}
	
}

void print_node(const Node* n)
{
    if (n->type == 0) {
        // Type 1: 3-state spin, symbol = ■
        if (n->spin == - (n->spin_value))
            printf(LOW0   "● " RESET);
        else if (n->spin == n->spin_value)
            printf(HIGH0  "● " RESET);
        else
            printf(MID0    "● " RESET);

    } else if (n->type == 1) {
        // Type 2: 2-state spin, symbol = ▲
        if (n->spin == - (n->spin_value))
            printf(LOW1  "● " RESET);
        else if (n->spin == n->spin_value)
        	printf(HIGH1  "● " RESET);
        else
            printf(MID1 "● " RESET);
    }
}

void print_lattice(const Node* nodes, int L)
{
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            print_node(&nodes[i * L + j]);
        }
        printf("\n");
    }
}

int parse_double_array(const char *s, double *arr, int n)
{
    // Expect format: {x,y,...}
    if (s[0] != '{')
        return -1;

    const char *p = s + 1;

    for (int i = 0; i < n; i++) {
        if (sscanf(p, "%lf", &arr[i]) != 1)
            return -1;

        p = strchr(p, ',');
        if (!p) {
            if (i == n - 1)
                break;
            return -1;
        }
        p++;
    }

    return 0;
}

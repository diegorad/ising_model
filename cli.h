#ifndef CLI_H
#define CLI_H

#include "tools.h" 

typedef enum {
    OUT_MONITOR,
    OUT_OUTPUT,
    OUT_PLOT,
    OUT_NONE
} OutputMode;

typedef enum {
    RAND,
    SAT,
    SAT_NEG
} InitMode;

typedef struct {
    OutputMode out_mode;
    InitMode init_mode;
    double D_i[2];
    double J_ij[3];
    int seed;
    double T;
    double xrate;
} Config;

int parse_args(int argc, char **argv, Config *cfg);

#endif


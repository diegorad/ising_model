#ifndef CLI_H
#define CLI_H

#include "tools.h" 

typedef enum {
    OUT_MONITOR,
    OUT_OUTPUT,
    OUT_PLOT
} OutputMode;

typedef struct {
    OutputMode out_mode;
    double D_i[2];
    int seed;
} Config;

int parse_args(int argc, char **argv, Config *cfg);

#endif


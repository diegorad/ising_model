#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

#include "cli.h"

static struct option long_options[] = {
    {"out", required_argument, 0, 'o'},
    {"D_i",   required_argument, 0, 'D'},
    {"J_ij",   required_argument, 0, 'J'},
    {"seed", required_argument, 0, 's'},
    {"T", required_argument, 0, 'T'},
    {"help", no_argument, 0, 'h'},
    {0, 0, 0, 0}
};

int parse_args(int argc, char **argv, Config *cfg)
{
    int opt;
    int option_index = 0;

    while ((opt = getopt_long(argc, argv, "o:D:J:s:T:h",
                              long_options, &option_index)) != -1)
    {
        switch (opt) {

        case 'o':
            if (strcmp(optarg, "monitor") == 0)
                cfg->out_mode = OUT_MONITOR;
            else if (strcmp(optarg, "output") == 0)
                cfg->out_mode = OUT_OUTPUT;
            else if (strcmp(optarg, "plot") == 0)
                cfg->out_mode = OUT_PLOT;
            else {
                fprintf(stderr, "Invalid --out value: %s\n", optarg);
                return EXIT_FAILURE;
            }
            break;

        case 'D':
			if (parse_double_array(optarg, cfg->D_i, 2) != 0) {
				fprintf(stderr, "Invalid format for --D_i. Usage example: --D_i=\"{0.0, 0.0}\"\n");
				exit(EXIT_FAILURE);
			}
			break;
			
		 case 'J':
			if (parse_double_array(optarg, cfg->J_ij, 3) != 0) {
				fprintf(stderr, "Invalid format for --J_ij. Usage example: --J_ij=\"{0.0, 0.0, 0.0}\"\n");
				exit(EXIT_FAILURE);
			}
			break;
			
		case 's':
			cfg->seed = atof(optarg);
    		break;
    	
    	case 'T':
			cfg->T = atof(optarg);
    		break;

        case 'h':
            printf("Usage: %s [options]\n", argv[0]);
            printf("  --out=monitor|output|plot\n");
            printf("  --D_i={0.0, 0.0}\n");
            printf("  --J_ij={0.0, 0.0, 0.0}\n");
            printf("  --seed=1\n");
            printf("  --T=6/n");
            exit(EXIT_SUCCESS);

        default:
            return EXIT_FAILURE;
        }
    }

    return 0;
}

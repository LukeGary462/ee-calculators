/**
*     @file:    goertzel-configure.c
*     @name:    Luke Gary
*  @company:    <company>
*     @date:    2021/2/18
********************************************************************************
* @copyright
*   Copyright 2020 <company> as an  unpublished work.
*   All Rights Reserved.
*
* @license The information contained herein is confidential
*   property of <company>. The user, copying, transfer or
*   disclosure of such information is prohibited except
*   by express written agreement with <company>.
********************************************************************************
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

/**
 * k = (Block_Size * Target_Frequency) / Sampling_Frequency
 * w = 2*pi * (k / Block_Size)
 * a0 = 1
 * a1 = 2*cos(w)
 * a2 = -1
 * b0 = 1
 * b1 = -e ^(sin(w))
 * b2 = 0
 */

void main(int argc, char *argv[]){

    float sampling_frequency = 30e3;// argv[1]
    float target_frequency = 1e3;   // argv[2]
    unsigned int block_size = 100;  // argv[3]

    for(int i = 0; i < argc; i++)
    {
        printf("\nargv[%d] - %s", i, argv[i]);
        if(strncmp(argv[i], "-fs", sizeof("-fs")) == 0)
        {
            sampling_frequency = atof(argv[i+1]);
            printf(" - %s", argv[i+1]);
            i += 1;
        }
        else if(strncmp(argv[i], "-ft", sizeof("-ft")) == 0)
        {
            target_frequency = atof(argv[i+1]);
            printf(" - %s", argv[i+1]);
            i += 1;
        }
        else if(strncmp(argv[i], "-bs", sizeof("-ft")) == 0)
        {
            block_size = atoi(argv[i+1]);
            printf(" - %s", argv[i+1]);
            i += 1;
        }
    }

    printf("\n\n           Fs - %f Hz", sampling_frequency);
    printf("\n           Ft - %f Hz", target_frequency);
    printf("\n   Block Size - %d samples", block_size);

    float k = (block_size * target_frequency) / sampling_frequency;
    float w = 2.0*M_PI * (k/block_size);
    printf("\n      K value - %f", k);
    printf("\n        omega - %f", w);

    printf("\n\nDirect Form 2 Transposed IIR Filter Gains:");
    float a1 = 2*cos(w);
    float b1 = -1.0*exp(sin(w));
    printf("\n           a0 -  %f", 1.0);
    printf("\n           a1 -  %f", a1);
    printf("\n           a2 - %f", -1.0);
    printf("\n           b0 -  %f", 1.0);
    printf("\n           b1 - %f", b1);
    printf("\n           b2 -  %f", 0.0);

    // calculate "settling time" of filter. i.e. time to result
    printf("\n\n Filter Performance Metrics:");
    float ts = ((1.0/sampling_frequency) * block_size) * 1000;
    float bin_width = sampling_frequency / block_size;
    printf("\nsettling time - %f ms (sample taken every %d samples)", ts, block_size);
    printf("\n    bin width - %f Hz", bin_width);

}
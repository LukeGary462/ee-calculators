/**
* @file:                goertzel.h
* @par
* @company              Biomeme, Inc
* @author               Luke R Gary
* @version              0.0.0
* @date                 2018/7/14
* @brief
* @verbatim
* @endverbatim
 *
****************************************************************
* @copyright
*   Copyright 2018 [Biomeme, Inc] as an  unpublished work.
*   All Rights Reserved.
*
* @license The information contained herein is confidential
*   property of [Biomeme, Inc]. The user, copying, transfer or
*   disclosure of such information is prohibited except
*   by express written agreement with [Biomeme, Inc].
****************************************************************
*/


#ifndef GOERTZEL_H_
#define GOERTZEL_H_

#include <arm_math.h>
#include <stdint.h>
#include "common/error.h"

#pragma pack(1)
typedef struct
{
    /// state variables
    float32_t       S[3];
    /// sampling frequency, MUST BE REGULAR with minimal jitter
    float32_t       sample_rate_hz;
    /// real coeff
    float32_t coeff_real;
    /// imaginary coeff
    float32_t coeff_imag;
    /// frequency of interest
    float32_t frequency;
}goertzel_filter_t;
#pragma pack()

error_t goertzel_init(goertzel_filter_t *g, float32_t frequency, float32_t sampleRateHz);
float goerzel_calculate_block_power(goertzel_filter_t *g, float32_t *data, size_t length);
error_t goertzel_calculate_block(goertzel_filter_t *g, float32_t *data, size_t length, float32_t *dest, size_t dest_length);

#endif
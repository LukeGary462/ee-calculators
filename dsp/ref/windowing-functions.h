/**
* @file:                windowing-functions.h
* @par
* @company              Biomeme, Inc
* @author               Luke R Gary
* @version              0.0.0
* @date                 2018/7/16
* @brief
* @verbatim
* @endverbatim
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
#ifndef WINDOWING_FUNCTIONS_H_
#define WINDOWING_FUNCTIONS_H_

#include <arm_math.h>
#include <stdint.h>
#include "common/error.h"

typedef error_t (*window_func_t)(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);

error_t window_tri              (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_parzen           (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_welch            (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_sine             (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_squsine          (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_hamming          (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_hanning          (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_nuttall          (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_blackman_nuttall (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_blackman_harris  (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_flattop          (float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
error_t window_apply(window_func_t *window, float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length);
void    window_print(window_func_t *window);

#endif

/**
* @file:                goertzel.c
* @par
* @company              Biomeme, Inc
* @author               Luke R Gary
* @version              0.0.0
* @date                 2018/7/14
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
/*******************************************************************************
* Includes
*******************************************************************************/
#include "goertzel.h"
#include <arm_math.h>

/*******************************************************************************
* Defines
*******************************************************************************/
#define GOERTZEL_RETURN_IF(x, ret) \
    do{\
    if((x))\
    {\
        return (ret);\
    }\
    }while(0)

/*******************************************************************************
* Local Types and Typedefs
*******************************************************************************/


/*******************************************************************************
* Static Function Prototypes
*******************************************************************************/


/*******************************************************************************
* Global Variables
*******************************************************************************/


/*******************************************************************************
* Static Variables
*******************************************************************************/


/*******************************************************************************
* Functions
*******************************************************************************/

/**
 * @brief      initialize goertzel filter
 *
 * @param      g             goertzle filter object
 * @param[in]  frequency     The frequency
 * @param[in]  sampleRateHz  The sample rate hz
 *
 * @return     init status
 */
error_t goertzel_init(goertzel_filter_t *g, float32_t frequency, float32_t sampleRateHz)
{
    GOERTZEL_RETURN_IF(g == NULL, ERR_NULL);
    GOERTZEL_RETURN_IF((frequency >= (sampleRateHz / 2.0f)), ERR_PARAM);

    g->S[0] = 0.0f;
    g->S[1] = 0.0f;
    g->S[2] = 0.0f;
    g->sample_rate_hz = sampleRateHz;
    g->frequency = frequency;

    float32_t omega = 2.0f * g->frequency * PI;
    g->coeff_real = 2.0f * arm_cos_f32(omega);
    g->coeff_imag = arm_sin_f32(omega);

    return ERR_NONE;
}

/**
 * @brief      calculate goertzel filter result in terms of signal power
 *
 * @param      g       goertzel filter object
 * @param      data    The data
 * @param[in]  length  The length
 *
 * @return     signal power
 */
float goerzel_calculate_block_power(goertzel_filter_t *g, float32_t *data, size_t length)
{
    GOERTZEL_RETURN_IF(g == NULL, ERR_NULL);
    GOERTZEL_RETURN_IF(data == NULL, ERR_NULL);

    float32_t k = (float32_t)length * 0.5f;
    for(unsigned int i = 0; i < length; i++)
    {
        g->S[0] = data[i] + g->coeff_real * g->S[1] - g->S[2];
        g->S[2] = g->S[1];
        g->S[1] = g->S[0];
    }
    float32_t power = (g->S[2] * g->S[2]) + (g->S[2] * g->S[1]) - (g->S[1] * g->S[2] * g->coeff_real);
    power = power / k;
    g->S[0] = 0.0f;
    g->S[1] = 0.0f;
    g->S[2] = 0.0f;
    return (float)power;
}

/**
 * @brief      calculate complete results of goertzel
 *
 * @param      g         goertzel filter object
 * @param      data      The data
 * @param[in]  length    The length
 * @param      dest      The destination
 * @param[in]  dest_len  The destination length
 *
 * @return     error code
 */
error_t goertzel_calculate_block(goertzel_filter_t *g, float32_t *data, size_t length, float32_t *dest, size_t dest_length)
{
    GOERTZEL_RETURN_IF(g == NULL, ERR_NULL);
    GOERTZEL_RETURN_IF(data == NULL, ERR_NULL);
    GOERTZEL_RETURN_IF(dest == NULL, ERR_NULL);
    GOERTZEL_RETURN_IF((dest_len != 4), ERR_PARAM);

    float32_t k = (float32_t)length * 0.5f;
    for(unsigned int i = 0; i < length; i++)
    {
        g->S[0] = data[i] + g->coeff_real * g->S[1] - g->S[2];
        g->S[2] = g->S[1];
        g->S[1] = g->S[0];
    }
    float32_t r, i, m, p;

    r = 0.5f * g->coeff_real * g->S[1] - g->S[2];
    i = g->coeff_imag * g->S[1];
    m = arm_sqrt_f32((r*r + i*i)) / (length / 4);
    p = (g->S[2] * g->S[2]) + (g->S[2] * g->S[1]) - (g->S[1] * g->S[2] * g->coeff_real);

    results[0] = r;
    results[1] = i;
    results[2] = m;
    results[3] = p;
    return ERR_NONE;
}



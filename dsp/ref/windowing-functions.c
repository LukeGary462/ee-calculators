/**
* @file:                windowing-functions.c
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
/*******************************************************************************
* Includes
*******************************************************************************/
#include "windowing-functions.h"


/*******************************************************************************
* Defines
*******************************************************************************/
#ifndef COUNTOF
    #define COUNTOF(x) (sizeof(x)/sizeof(x[0]))
#endif

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

error_t window_tri(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window = 1.0f - ((i - (length-1.0f)/2.0f)/(length/2.0f));
        dest[i] = data[i] * (window);
    }
    return ERR_NONE;
}
error_t window_parzen(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);

    return ERR_NONE;
}
error_t window_welch(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window = 1.0f - ((i - (length-1.0f)/2.0f)/(length/2.0f))*((i - (length-1.0f)/2.0f)/(length/2.0f));
        dest[i] = data[i] * (window);
    }
    return ERR_NONE;
}
error_t window_sine(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    for(unsigned int i = 0; i < length; i++)
    {
        dest[i] = data[i] * arm_sin_f32((PI*i)/(length-1.0f));
    }
    return ERR_NONE;
}
error_t window_squsine(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    for(unsigned int i = 0; i < length; i++)
    {
        dest[i] = data[i] * arm_sin_f32((PI*i)/(length-1.0f)) * arm_sin_f32((PI*i)/(length-1.0f));
    }
    return ERR_NONE;
}

error_t window_hanning(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window = 0.5f * (1.0f - arm_cos_f32((2.0f*PI*i)/(length/2.0f)));
        dest[i] = data[i] * (window);
    }
    return ERR_NONE;
}

error_t window_hamming(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window = (25.0f/46.0f) * (1.0f - arm_cos_f32((2.0f*PI*i)/(length/2.0f)));
        dest[i] = data[i] * (window);
    }
    return ERR_NONE;
}

error_t window_nuttall(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window1 = 1.0f;
    float32_t window2 = 1.0f;
    float32_t window3 = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window1 = 0.487396f * arm_cos_f32((2.0f*PI*i)/(length-1.0f));
        window2 = 0.144232f * arm_cos_f32((4.0f*PI*i)/(length-1.0f));
        window3 = 0.012604f * arm_cos_f32((6.0f*PI*i)/(length-1.0f));
        dest[i] = data[i] * (0.355768f - window1 + window2 - window3)
    }
    return ERR_NONE;
}
error_t window_blackman_nuttall(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window1 = 1.0f;
    float32_t window2 = 1.0f;
    float32_t window3 = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window1 = 0.4891775f * arm_cos_f32((2.0f*PI*i)/(length-1.0f));
        window2 = 0.1365995f * arm_cos_f32((4.0f*PI*i)/(length-1.0f));
        window3 = 0.0106411f * arm_cos_f32((6.0f*PI*i)/(length-1.0f));
        dest[i] = data[i] * (0.3635819f - window1 + window2 - window3)
    }
    return ERR_NONE;
}
error_t window_blackman_harris(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window1 = 1.0f;
    float32_t window2 = 1.0f;
    float32_t window3 = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window1 = 0.48829f * arm_cos_f32((2.0f*PI*i)/(length-1.0f));
        window2 = 0.14128f * arm_cos_f32((4.0f*PI*i)/(length-1.0f));
        window3 = 0.01168f * arm_cos_f32((6.0f*PI*i)/(length-1.0f));
        dest[i] = data[i] * (0.35875f - window1 + window2 - window3)
    }
    return ERR_NONE;
}
error_t window_flattop(float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    WINDOW_RETURN_If((length != dest_length), ERR_BOUNDS);
    WINDOW_RETURN_IF((data == NULL), ERR_NULL);
    WINDOW_RETURN_IF((dest == NULL), ERR_NULL);
    float32_t window1 = 1.0f;
    float32_t window2 = 1.0f;
    float32_t window3 = 1.0f;
    float32_t window4 = 1.0f;
    for(unsigned int i = 0; i < length; i++)
    {
        window1 = 1.930f * arm_cos_f32((2.0f*PI*i)/(length-1.0f));
        window2 = 1.290f * arm_cos_f32((4.0f*PI*i)/(length-1.0f));
        window3 = 0.388f * arm_cos_f32((6.0f*PI*i)/(length-1.0f));
        window4 = 0.028f * arm_cos_f32((8.0f*PI*i)/(length-1.0f));
        dest[i] = data[i] * (1.0f - window1 + window2 - window3 + window4)
    }
    return ERR_NONE;
}


error_t window_apply(window_func_t *window, float32_t *data, unsigned int length, float32_t *dest, unsigned int dest_length)
{
    return window(data, length, dest, dest_length);
}

void window_print(window_func_t *window)
{
    float32_t testData[50] = {1.0f};
    error_t result = window_apply(window, testData, COUNTOF(testData), testData, COUNTOF(testData));
    if(result == ERR_NONE)
    {
        for(unsigned int i = 0; i < COUNTOF(testData); i++)
        {
            printf("%u,\t%1.4f\r\n", i, testData[i])
        }
    }
}

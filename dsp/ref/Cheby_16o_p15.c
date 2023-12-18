/**************************************************************
WinFilter version 0.8
http://www.winfilter.20m.com
akundert@hotmail.com

Filter type: Low Pass
Filter model: Chebyshev
Filter order: 16
Sampling Frequency: 1000 Hz
Cut Frequency: 150.000000 Hz
Pass band Ripple: 1.000000 dB
Coefficents Quantization: float

Z domain Zeros
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000

Z domain Poles
z = 0.759113 + j -0.551469
z = 0.759113 + j 0.551469
z = 0.824710 + j -0.423034
z = 0.824710 + j 0.423034
z = 0.693670 + j -0.650938
z = 0.693670 + j 0.650938
z = 0.638368 + j -0.723622
z = 0.638368 + j 0.723622
z = 0.878456 + j -0.267297
z = 0.878456 + j 0.267297
z = 0.600346 + j -0.773194
z = 0.600346 + j 0.773194
z = 0.908905 + j -0.091565
z = 0.908905 + j 0.091565
z = 0.584175 + j -0.802908
z = 0.584175 + j 0.802908
***************************************************************/
#define NCoef 16
float iir(float NewSample) {
    float ACoef[NCoef+1] = {
        0.00000000034153766348,
        0.00000000546460261563,
        0.00000004098451961725,
        0.00000019126109154716,
        0.00000062159854752826,
        0.00000149183651406784,
        0.00000273503360912437,
        0.00000390719087017766,
        0.00000439558972894987,
        0.00000390719087017766,
        0.00000273503360912437,
        0.00000149183651406784,
        0.00000062159854752826,
        0.00000019126109154716,
        0.00000004098451961725,
        0.00000000546460261563,
        0.00000000034153766348
    };

    float BCoef[NCoef+1] = {
        1.00000000000000000000,
        -11.77548837155684900000,
        67.63924999183449000000,
        -250.87991359096398000000,
        671.16046658394760000000,
        -1371.09720021446700000000,
        2210.03293388376690000000,
        -2864.75848413555200000000,
        3016.33608298621040000000,
        -2587.45512162244220000000,
        1802.06901761634500000000,
        -1008.38411252439910000000,
        444.57141097788246000000,
        -149.36671276372485000000,
        36.09666225695465900000,
        -5.61237810237308120000,
        0.42360994066814639000
    };

    static float y[NCoef+1]; //output samples
    static float x[NCoef+1]; //input samples
    int n;

    //shift the old samples
    for(n=NCoef; n>0; n--) {
       x[n] = x[n-1];
       y[n] = y[n-1];
    }

    //Calculate the new output
    x[0] = NewSample;
    y[0] = ACoef[0] * x[0];
    for(n=1; n<=NCoef; n++)
        y[0] += ACoef[n] * x[n] - BCoef[n] * y[n];
    
    return y[0];
}

// usage? I think this is how it would be used... -Luke-
#define NUM_SAMPLES 45

float rawData[NUM_SAMPLES]; 
float filteredData[NUM_SAMPLES];

void runIIR(float * in, float * out, unsigned int x);
void runIIR(float * in, float * out, unsigned int x)
{
    unsigned int i;
    for(i = 0; i < x; i+)
    {
        out[i] = iir(in[i]);
    }
}

//runIIR(&rawData, &filteredData, NUM_SAMPLES);
/**************************************************************
WinFilter version 0.8
http://www.winfilter.20m.com
akundert@hotmail.com

Filter type: Low Pass
Filter model: Bessel
Filter order: 4
Sampling Frequency: 1000 Hz
Cut Frequency: 200.000000 Hz
Coefficents Quantization: float

Z domain Zeros
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000

Z domain Poles
z = 0.160287 + j -0.473657
z = 0.160287 + j 0.473657
z = 0.189964 + j -0.141326
z = 0.189964 + j 0.141326
***************************************************************/
#define Ntap 64

float fir(float NewSample) {
    float FIRCoef[Ntap] = { 
        0.00000000002615645044,
        -0.00000000001013972107,
        -0.00000000012247309377,
        -0.00000000011762606789,
        0.00000000035863399059,
        0.00000000096132829705,
        -0.00000000024662033779,
        -0.00000000435772863403,
        -0.00000000466438551962,
        0.00000001224077671036,
        0.00000003569538957240,
        -0.00000000496619735946,
        -0.00000015764395078488,
        -0.00000018557763575831,
        0.00000042749761627299,
        0.00000135312431223458,
        -0.00000005493401694862,
        -0.00000589193812471466,
        -0.00000750460838220441,
        0.00001573474713802848,
        0.00005352011487077539,
        0.00000115208674552698,
        -0.00023613310875727345,
        -0.00031531280816833249,
        0.00065574596551317300,
        0.00226479143276908050,
        -0.00039661859256209163,
        -0.01194263572979073300,
        -0.01061827594244024400,
        0.07538714674906581100,
        0.26054902010943981000,
        0.36918768850787237000,
        0.26054902010943981000,
        0.07538714674906581100,
        -0.01061827594244024400,
        -0.01194263572979073300,
        -0.00039661859256209163,
        0.00226479143276908050,
        0.00065574596551317300,
        -0.00031531280816833249,
        -0.00023613310875727345,
        0.00000115208674552698,
        0.00005352011487077539,
        0.00001573474713802848,
        -0.00000750460838220441,
        -0.00000589193812471466,
        -0.00000005493401694862,
        0.00000135312431223458,
        0.00000042749761627299,
        -0.00000018557763575831,
        -0.00000015764395078488,
        -0.00000000496619735946,
        0.00000003569538957240,
        0.00000001224077671036,
        -0.00000000466438551962,
        -0.00000000435772863403,
        -0.00000000024662033779,
        0.00000000096132829705,
        0.00000000035863399059,
        -0.00000000011762606789,
        -0.00000000012247309377,
        -0.00000000001013972107,
        0.00000000002615645044,
        0.00000000001061582880
    };

    static float x[Ntap]; //input samples
    float y=0;            //output sample
    int n;

    //shift the old samples
    for(n=Ntap-1; n>0; n--)
       x[n] = x[n-1];

    //Calculate the new output
    x[0] = NewSample;
    for(n=0; n<Ntap; n++)
        y += FIRCoef[n] * x[n];
    
    return y;
}

// usage? I think this is how it would be used... -Luke-
#define NUM_SAMPLES 45

float rawData[NUM_SAMPLES]; 
float filteredData[NUM_SAMPLES];

void fir(float * in, float * out, unsigned int x);
void fir(float * in, float * out, unsigned int x)
{
    unsigned int i;
    for(i = 0; i < x; i+)
    {
        out[i] = fir(in[i]);
    }
}

/** EXAMPLE
    // better way may be to make a generic filter function that can point to multiple implementations based on context... provided all input/output parameters are equal
    void (*filter)(float * in, float * out, uint16_t x);
    
    // fir on set a
    filter = &fir;
    filter(&rawDataSetA, &filteredDataSetA, NUM_SAMPLES);
    // do other shit
    
    // iir on set b
    filter = &iir;
    filter(&rawDataSetB, &filteredDataSetB, NUM_SAMPLES);
    
    
    //fir(&rawData, &filteredData, NUM_SAMPLES);
*/
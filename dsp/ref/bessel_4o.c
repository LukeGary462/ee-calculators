/**************************************************************
WinFilter version 0.8
http://www.winfilter.20m.com
akundert@hotmail.com

Filter type: Low Pass
Filter model: Bessel
Filter order: 4
Sampling Frequency: 10 KHz
Cut Frequency: 0.100000 KHz
Coefficents Quantization: float

Z domain Zeros
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000

Z domain Poles
z = 0.944571 + j -0.016098
z = 0.944571 + j 0.016098
z = 0.958250 + j -0.050055
z = 0.958250 + j 0.050055
***************************************************************/
#define NCoef 4
float iir(float NewSample) {
    float ACoef[NCoef+1] = {
        0.00000087916846575559,
        0.00000351667386302234,
        0.00000527501079453352,
        0.00000351667386302234,
        0.00000087916846575559
    };

    float BCoef[NCoef+1] = {
        1.00000000000000000000,
        -3.80564318443105830000,
        5.43376612211687520000,
        -3.44985353637297990000,
        0.82174475234526467000
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

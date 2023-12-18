/**************************************************************
WinFilter version 0.8
http://www.winfilter.20m.com
akundert@hotmail.com

Filter type: Low Pass
Filter model: Bessel
Filter order: 8
Sampling Frequency: 1000 Hz
Cut Frequency: 50.000000 Hz
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

Z domain Poles
z = 0.747483 + j -0.034213
z = 0.747483 + j 0.034213
z = 0.757107 + j -0.104465
z = 0.757107 + j 0.104465
z = 0.778930 + j -0.182004
z = 0.778930 + j 0.182004
z = 0.821143 + j -0.278007
z = 0.821143 + j 0.278007
***************************************************************/
#define NCoef 8
float iir(float NewSample) {
    float ACoef[NCoef+1] = {
        0.00000015888788812141,
        0.00000127110310497126,
        0.00000444886086739941,
        0.00000889772173479882,
        0.00001112215216849852,
        0.00000889772173479882,
        0.00000444886086739941,
        0.00000127110310497126,
        0.00000015888788812141
    };

    float BCoef[NCoef+1] = {
        1.00000000000000000000,
        -6.20932609764312900000,
        16.98741204084305100000,
        -26.73380707425711500000,
        26.46102374948879900000,
        -16.86246184580533500000,
        6.75416500393939410000,
        -1.55424214536948300000,
        0.15727704627257147000
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

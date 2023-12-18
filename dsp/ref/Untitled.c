/**************************************************************
WinFilter version 0.8
http://www.winfilter.20m.com
akundert@hotmail.com

Filter type: Low Pass
Filter model: Butterworth
Filter order: 8
Sampling Frequency: 1000 Hz
Cut Frequency: 100.000000 Hz
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
z = 0.543429 + j -0.219353
z = 0.543429 + j 0.219353
z = 0.513176 + j -0.072739
z = 0.513176 + j 0.072739
z = 0.609863 + j -0.368417
z = 0.609863 + j 0.368417
z = 0.725790 + j -0.517185
z = 0.725790 + j 0.517185
***************************************************************/
#define NCoef 8
float iir(float NewSample) {
    float ACoef[NCoef+1] = {
        0.00002402605457091591,
        0.00019220843656732727,
        0.00067272952798564539,
        0.00134545905597129080,
        0.00168182381996411360,
        0.00134545905597129080,
        0.00067272952798564539,
        0.00019220843656732727,
        0.00002402605457091591
    };

    float BCoef[NCoef+1] = {
        1.00000000000000000000,
        -4.78451489499581050000,
        10.44504106553466900000,
        -13.45771989024156000000,
        11.12933103916398100000,
        -6.02526039729765460000,
        2.07927380301187850000,
        -0.41721715698978240000,
        0.03720010070484527200
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

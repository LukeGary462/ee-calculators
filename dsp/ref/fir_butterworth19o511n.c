/**************************************************************
WinFilter version 0.8
http://www.winfilter.20m.com
akundert@hotmail.com

Filter type: Low Pass
Filter model: Butterworth
Filter order: 19
Sampling Frequency: 10 KHz
Cut Frequency: 1.250000 KHz
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
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000
z = -1.000000 + j 0.000000

Z domain Poles
z = 0.397194 + j -0.201132
z = 0.397194 + j 0.201132
z = 0.478423 + j -0.152831
z = 0.478423 + j 0.152831
z = 0.458558 + j -0.301255
z = 0.458558 + j 0.301255
z = 0.479960 + j -0.340640
z = 0.479960 + j 0.340640
z = 0.365020 + j -0.068798
z = 0.365020 + j 0.068798
z = 0.508700 + j -0.428591
z = 0.508700 + j 0.428591
z = 0.551011 + j -0.504195
z = 0.551011 + j 0.504195
z = 0.602489 + j -0.584072
z = 0.602489 + j 0.584072
z = 0.474220 + j -0.000000
z = 0.668096 + j -0.665814
z = 0.668096 + j 0.665814
***************************************************************/
#define Ntap 511

float fir(float NewSample) {
    float FIRCoef[Ntap] = { 
        -0.00000000124139913653,
        0.00000000068537311846,
        0.00000000223612950132,
        0.00000000216136618678,
        0.00000000033056306271,
        -0.00000000209067280408,
        -0.00000000336496496050,
        -0.00000000236852038263,
        0.00000000054190615386,
        0.00000000360098755058,
        0.00000000468477912910,
        0.00000000272608423164,
        -0.00000000141862793798,
        -0.00000000529087816268,
        -0.00000000626130211496,
        -0.00000000325301850673,
        0.00000000234092538823,
        0.00000000724181835139,
        0.00000000817159463855,
        0.00000000397688011769,
        -0.00000000335032434696,
        -0.00000000954512973033,
        -0.00000001050681132841,
        -0.00000000493483652755,
        0.00000000448992632543,
        0.00000001230505978047,
        0.00000001337528019816,
        0.00000000617497851041,
        -0.00000000580569547487,
        -0.00000001564202636603,
        -0.00000001690590308873,
        -0.00000000775791347247,
        0.00000000734764592551,
        0.00000001969598666250,
        0.00000002125183573115,
        0.00000000975863374146,
        -0.00000000917091325166,
        -0.00000002462989558997,
        -0.00000002659436381312,
        -0.00000001226859832481,
        0.00000001133668098564,
        0.00000003063309635759,
        0.00000003314682312077,
        0.00000001539794916269,
        -0.00000001391286299786,
        -0.00000003792443793139,
        -0.00000004115830274305,
        -0.00000001927771419460,
        0.00000001697446431440,
        0.00000004675476110544,
        0.00000005091666508795,
        0.00000002406177565806,
        -0.00000002060348317640,
        -0.00000005740820736549,
        -0.00000006275031263552,
        -0.00000002992820951082,
        0.00000002488803034519,
        0.00000007020156572495,
        0.00000007702761897086,
        0.00000003707950252485,
        -0.00000002992046903158,
        -0.00000008548049055857,
        -0.00000009415272164176,
        -0.00000004574075483300,
        0.00000003579405956539,
        0.00000010361097175412,
        0.00000011455558494936,
        0.00000005615480291192,
        -0.00000004259755214732,
        -0.00000012496372084967,
        -0.00000013867349877552,
        -0.00000006857247479674,
        0.00000005040692528003,
        0.00000014988827552649,
        0.00000016691998373646,
        0.00000008323565274460,
        -0.00000005927320464172,
        -0.00000017867237074415,
        -0.00000019963552693890,
        -0.00000010034976870254,
        0.00000006920494573207,
        0.00000021148045605869,
        0.00000023701240591299,
        0.00000012004106248273,
        -0.00000008014351611307,
        -0.00000024826302702795,
        -0.00000027898303460988,
        -0.00000014229211055862,
        0.00000009192870664470,
        0.00000028862540556126,
        0.00000032505732852703,
        0.00000016684674110067,
        -0.00000010425139755298,
        -0.00000033164062238787,
        -0.00000037408937655872,
        -0.00000019307207829461,
        0.00000011658903831889,
        0.00000037558563497112,
        0.00000042394673179442,
        0.00000021976108899157,
        -0.00000012811830616369,
        -0.00000041757298418350,
        -0.00000047104622494717,
        -0.00000024485297397376,
        0.00000013759760898103,
        0.00000045304036976812,
        0.00000050970765091192,
        0.00000026504072803791,
        -0.00000014320977393757,
        -0.00000047504797524056,
        -0.00000053126001404738,
        -0.00000027522452609024,
        0.00000014235228704568,
        0.00000047331627146082,
        0.00000052281260550398,
        0.00000026775516341991,
        -0.00000013135842577635,
        -0.00000043291456893917,
        -0.00000046557354860434,
        -0.00000023139280130666,
        0.00000010512731555952,
        0.00000033248035711708,
        0.00000033255873795159,
        0.00000014988071090639,
        -0.00000005663392447408,
        -0.00000014180946778531,
        -0.00000008548143323894,
        0.00000000000000008517,
        -0.00000002371962954016,
        -0.00000018139649463084,
        -0.00000032945748005264,
        -0.00000025107354481535,
        0.00000014896304175471,
        0.00000069591053825982,
        0.00000098725222525371,
        0.00000064934894580554,
        -0.00000033669646971888,
        -0.00000148286935938415,
        -0.00000199174627140853,
        -0.00000125885294204473,
        0.00000061060305704916,
        0.00000265368063419209,
        0.00000348592297335101,
        0.00000216813759525573,
        -0.00000100246430501965,
        -0.00000436063143387890,
        -0.00000566572068851231,
        -0.00000349902136732839,
        0.00000155485683093670,
        0.00000681111530883926,
        0.00000879855913300086,
        0.00000541830387534832,
        -0.00000232478030273877,
        -0.00001028671434479851,
        -0.00001324816475677095,
        -0.00000815343269537622,
        0.00000338857128585446,
        0.00001516880916397618,
        0.00001950782389961076,
        0.00001201341331671208,
        -0.00000484861370620939,
        -0.00002197299182440917,
        -0.00002824492499196577,
        -0.00001741666294698394,
        0.00000684259060401868,
        0.00003139539080980743,
        0.00004036064346662258,
        0.00002492803696353705,
        -0.00000955638626361395,
        -0.00004437519385632683,
        -0.00005706998454323389,
        -0.00003530794195170891,
        0.00001324231134876751,
        0.00006217932047120444,
        0.00008000926623492085,
        0.00004957731462434454,
        -0.00001824522574215674,
        -0.00008651760228881583,
        -0.00011138071931159021,
        -0.00006910332927028227,
        0.00002504058535171875,
        0.00011970034395776477,
        0.00015414750189727533,
        0.00009571199025335591,
        -0.00003429084383753340,
        -0.00016485539807863759,
        -0.00021229757897623552,
        -0.00013183527021879657,
        0.00004693062088110068,
        0.00022622984717922780,
        0.00029120226664587114,
        0.00018070194466888965,
        -0.00006429788085718558,
        -0.00030961384600378263,
        -0.00039810606626399902,
        -0.00024658250829980250,
        0.00008834003581817113,
        0.00042294392305645398,
        0.00054280047678472874,
        0.00033509858922336588,
        -0.00012194437146646919,
        -0.00057717534527632248,
        -0.00073855910517572475,
        -0.00045360452204788022,
        0.00016947849909153354,
        0.00078756729292055367,
        0.00100345030103683320,
        0.00061163998069901709,
        -0.00023769169915953799,
        -0.00107561763290558170,
        -0.00136220697883297400,
        -0.00082143121624187268,
        0.00033724734485554651,
        0.00147204929034466460,
        0.00184894189246636140,
        0.00109837271096243630,
        -0.00048537889842150225,
        -0.00202155347834156490,
        -0.00251119261153694320,
        -0.00146132801918257530,
        0.00071058853226940472,
        0.00279057870128877940,
        0.00341616240300331810,
        0.00193240812214014480,
        -0.00106115911571784900,
        -0.00388065140570747600,
        -0.00466084567857932750,
        -0.00253555158452754750,
        0.00162105990710554710,
        0.00545240230466023220,
        0.00638973848187822640,
        0.00329265816045798800,
        -0.00254105767213206980,
        -0.00777231182762014310,
        -0.00882953961864718470,
        -0.00421519517893449190,
        0.00410426670764970840,
        0.01131463342979646500,
        0.01236924386865426700,
        0.00528849087743691990,
        -0.00688308350255824060,
        -0.01702556387412924500,
        -0.01778999846063787300,
        -0.00644715100799136530,
        0.01220697719747782100,
        0.02720935472491505300,
        0.02714110357475866700,
        0.00754810635929994630,
        -0.02418044379036590800,
        -0.05000134668116319700,
        -0.04898732808934417500,
        -0.00836878842402770900,
        0.06788816708067009500,
        0.15808349858643331000,
        0.23081984221561810000,
        0.25867696095945730000,
        0.23081984221561810000,
        0.15808349858643331000,
        0.06788816708067009500,
        -0.00836878842402770900,
        -0.04898732808934417500,
        -0.05000134668116319700,
        -0.02418044379036590800,
        0.00754810635929994630,
        0.02714110357475866700,
        0.02720935472491505300,
        0.01220697719747782100,
        -0.00644715100799136530,
        -0.01778999846063787300,
        -0.01702556387412924500,
        -0.00688308350255824060,
        0.00528849087743691990,
        0.01236924386865426700,
        0.01131463342979646500,
        0.00410426670764970840,
        -0.00421519517893449190,
        -0.00882953961864718470,
        -0.00777231182762014310,
        -0.00254105767213206980,
        0.00329265816045798800,
        0.00638973848187822640,
        0.00545240230466023220,
        0.00162105990710554710,
        -0.00253555158452754750,
        -0.00466084567857932750,
        -0.00388065140570747600,
        -0.00106115911571784900,
        0.00193240812214014480,
        0.00341616240300331810,
        0.00279057870128877940,
        0.00071058853226940472,
        -0.00146132801918257530,
        -0.00251119261153694320,
        -0.00202155347834156490,
        -0.00048537889842150225,
        0.00109837271096243630,
        0.00184894189246636140,
        0.00147204929034466460,
        0.00033724734485554651,
        -0.00082143121624187268,
        -0.00136220697883297400,
        -0.00107561763290558170,
        -0.00023769169915953799,
        0.00061163998069901709,
        0.00100345030103683320,
        0.00078756729292055367,
        0.00016947849909153354,
        -0.00045360452204788022,
        -0.00073855910517572475,
        -0.00057717534527632248,
        -0.00012194437146646919,
        0.00033509858922336588,
        0.00054280047678472874,
        0.00042294392305645398,
        0.00008834003581817113,
        -0.00024658250829980250,
        -0.00039810606626399902,
        -0.00030961384600378263,
        -0.00006429788085718558,
        0.00018070194466888965,
        0.00029120226664587114,
        0.00022622984717922780,
        0.00004693062088110068,
        -0.00013183527021879657,
        -0.00021229757897623552,
        -0.00016485539807863759,
        -0.00003429084383753340,
        0.00009571199025335591,
        0.00015414750189727533,
        0.00011970034395776477,
        0.00002504058535171875,
        -0.00006910332927028227,
        -0.00011138071931159021,
        -0.00008651760228881583,
        -0.00001824522574215674,
        0.00004957731462434454,
        0.00008000926623492085,
        0.00006217932047120444,
        0.00001324231134876751,
        -0.00003530794195170891,
        -0.00005706998454323389,
        -0.00004437519385632683,
        -0.00000955638626361395,
        0.00002492803696353705,
        0.00004036064346662258,
        0.00003139539080980743,
        0.00000684259060401868,
        -0.00001741666294698394,
        -0.00002824492499196577,
        -0.00002197299182440917,
        -0.00000484861370620939,
        0.00001201341331671208,
        0.00001950782389961076,
        0.00001516880916397618,
        0.00000338857128585446,
        -0.00000815343269537622,
        -0.00001324816475677095,
        -0.00001028671434479851,
        -0.00000232478030273877,
        0.00000541830387534832,
        0.00000879855913300086,
        0.00000681111530883926,
        0.00000155485683093670,
        -0.00000349902136732839,
        -0.00000566572068851231,
        -0.00000436063143387890,
        -0.00000100246430501965,
        0.00000216813759525573,
        0.00000348592297335101,
        0.00000265368063419209,
        0.00000061060305704916,
        -0.00000125885294204473,
        -0.00000199174627140853,
        -0.00000148286935938415,
        -0.00000033669646971888,
        0.00000064934894580554,
        0.00000098725222525371,
        0.00000069591053825982,
        0.00000014896304175471,
        -0.00000025107354481535,
        -0.00000032945748005264,
        -0.00000018139649463084,
        -0.00000002371962954016,
        0.00000000000000008517,
        -0.00000008548143323894,
        -0.00000014180946778531,
        -0.00000005663392447408,
        0.00000014988071090639,
        0.00000033255873795159,
        0.00000033248035711708,
        0.00000010512731555952,
        -0.00000023139280130666,
        -0.00000046557354860434,
        -0.00000043291456893917,
        -0.00000013135842577635,
        0.00000026775516341991,
        0.00000052281260550398,
        0.00000047331627146082,
        0.00000014235228704568,
        -0.00000027522452609024,
        -0.00000053126001404738,
        -0.00000047504797524056,
        -0.00000014320977393757,
        0.00000026504072803791,
        0.00000050970765091192,
        0.00000045304036976812,
        0.00000013759760898103,
        -0.00000024485297397376,
        -0.00000047104622494717,
        -0.00000041757298418350,
        -0.00000012811830616369,
        0.00000021976108899157,
        0.00000042394673179442,
        0.00000037558563497112,
        0.00000011658903831889,
        -0.00000019307207829461,
        -0.00000037408937655872,
        -0.00000033164062238787,
        -0.00000010425139755298,
        0.00000016684674110067,
        0.00000032505732852703,
        0.00000028862540556126,
        0.00000009192870664470,
        -0.00000014229211055862,
        -0.00000027898303460988,
        -0.00000024826302702795,
        -0.00000008014351611307,
        0.00000012004106248273,
        0.00000023701240591299,
        0.00000021148045605869,
        0.00000006920494573207,
        -0.00000010034976870254,
        -0.00000019963552693890,
        -0.00000017867237074415,
        -0.00000005927320464172,
        0.00000008323565274460,
        0.00000016691998373646,
        0.00000014988827552649,
        0.00000005040692528003,
        -0.00000006857247479674,
        -0.00000013867349877552,
        -0.00000012496372084967,
        -0.00000004259755214732,
        0.00000005615480291192,
        0.00000011455558494936,
        0.00000010361097175412,
        0.00000003579405956539,
        -0.00000004574075483300,
        -0.00000009415272164176,
        -0.00000008548049055857,
        -0.00000002992046903158,
        0.00000003707950252485,
        0.00000007702761897086,
        0.00000007020156572495,
        0.00000002488803034519,
        -0.00000002992820951082,
        -0.00000006275031263552,
        -0.00000005740820736549,
        -0.00000002060348317640,
        0.00000002406177565806,
        0.00000005091666508795,
        0.00000004675476110544,
        0.00000001697446431440,
        -0.00000001927771419460,
        -0.00000004115830274305,
        -0.00000003792443793139,
        -0.00000001391286299786,
        0.00000001539794916269,
        0.00000003314682312077,
        0.00000003063309635759,
        0.00000001133668098564,
        -0.00000001226859832481,
        -0.00000002659436381312,
        -0.00000002462989558997,
        -0.00000000917091325166,
        0.00000000975863374146,
        0.00000002125183573115,
        0.00000001969598666250,
        0.00000000734764592551,
        -0.00000000775791347247,
        -0.00000001690590308873,
        -0.00000001564202636603,
        -0.00000000580569547487,
        0.00000000617497851041,
        0.00000001337528019816,
        0.00000001230505978047,
        0.00000000448992632543,
        -0.00000000493483652755,
        -0.00000001050681132841,
        -0.00000000954512973033,
        -0.00000000335032434696,
        0.00000000397688011769,
        0.00000000817159463855,
        0.00000000724181835139,
        0.00000000234092538823,
        -0.00000000325301850673,
        -0.00000000626130211496,
        -0.00000000529087816268,
        -0.00000000141862793798,
        0.00000000272608423164,
        0.00000000468477912910,
        0.00000000360098755058,
        0.00000000054190615386,
        -0.00000000236852038263,
        -0.00000000336496496050,
        -0.00000000209067280408,
        0.00000000033056306271,
        0.00000000216136618678,
        0.00000000223612950132,
        0.00000000068537311846,
        -0.00000000124139913653
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
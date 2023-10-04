// Automatically generated C++ file on Mon Sep 25 21:58:04 2023
//
// To build with Digital Mars C++ Compiler:
//
//    dmc -mn -WD test_filter_module_x1.cpp kernel32.lib

#include <stdio.h>
#include <malloc.h>
#include <stdarg.h>
#include <time.h>
#include <math.h>

union uData
{
   bool b;
   char c;
   unsigned char uc;
   short s;
   unsigned short us;
   int i;
   unsigned int ui;
   float f;
   double d;
   long long int i64;
   unsigned long long int ui64;
   char *str;
   unsigned char *bytes;
};

// int DllMain() must exist and return 1 for a process to load the .DLL
// See https://docs.microsoft.com/en-us/windows/win32/dlls/dllmain for more information.
int __stdcall DllMain(void *module, unsigned int reason, void *reserved) { return 1; }

void display(const char *fmt, ...)
{ // for diagnostic print statements
   msleep(30);
   fflush(stdout);
   va_list args = { 0 };
   va_start(args, fmt);
   vprintf(fmt, args);
   va_end(args);
   fflush(stdout);
   msleep(30);
}

void bzero(void *ptr, unsigned int count)
{
   unsigned char *first = (unsigned char *) ptr;
   unsigned char *last  = first + count;
   while(first < last)
      *first++ = '\0';
}

// #undef pin names lest they collide with names in any header file(s) you might include.
#undef IN
#undef OUT

struct sTEST_FILTER_MODULE_X1
{
   float S[3u];
   float sample_rate_hz;
   float frequency;
   float A;
   float B;
   float C;
   float N
};

extern "C" __declspec(dllexport) void test_filter_module_x1(struct sTEST_FILTER_MODULE_X1 **opaque, double t, union uData *data)
{
   float    IN    = data[0].f; // input
   float    Fs    = data[1].f;
   float    freq  = data[2].f;
   float    &OUT  = data[3].f; // output


   if(!*opaque)
   {
      *opaque = (struct sTEST_FILTER_MODULE_X1 *) malloc(sizeof(struct sTEST_FILTER_MODULE_X1));
      bzero(*opaque, sizeof(struct sTEST_FILTER_MODULE_X1));
   }

   struct sTEST_FILTER_MODULE_X1 *inst = *opaque;
   if(inst->coeff_real == 0)
   {
      display("%f, %f\n", Fs, freq);
      inst->S[0u] = 0.0f;
      inst->S[1u] = 0.0f;
      inst->S[2u] = 0.0f;
      inst->sample_rate_hz = Fs;
      inst->frequency = freq;
      float omega = 2.0f * inst->frequency * M_PI;
      inst->coeff_real = 2.0f * cos(omega);
      inst->coeff_imag = sin(omega);
      display("%f\n", inst->coeff_real);
      display("%f\n", inst->coeff_imag);
      display("%f\n", omega);
   }

   inst->S[0] = IN + inst->coeff_real * inst->S[1] - inst->S[2];
   inst->S[2] = inst->S[1];
   inst->S[1] = inst->S[0];

   float real = (inst->S[1] - inst->S[2]) * (0.5f * inst->coeff_real);
   float imag = inst->coeff_imag * inst->S[1];
   OUT = sqrt((real*real)+(imag*imag))/4.0f;
   display("in - %f, s[:] - %f %f %f, out - %f\n", IN, inst->S[0], inst->S[1], inst->S[2], OUT);
}

extern "C" __declspec(dllexport) void Destroy(struct sTEST_FILTER_MODULE_X1 *inst)
{
   free(inst);
}

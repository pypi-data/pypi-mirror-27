#ifndef GLOB_OPTS_H
#define GLOB_OPTS_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 Define OSQP compiler flags
 */
// Operative system
#define IS_LINUX
/* #undef IS_MAC */
/* #undef IS_WINDOWS */

// EMBEDDED
/* #undef EMBEDDED */

// PRINTING
#define PRINTING

// PROFILING
#define PROFILING

// CTRLC
#define CTRLC

// DFLOAT
/* #undef DFLOAT */

// DLONG
#define DLONG

// ENABLE_MKL_PARDISO
#define ENABLE_MKL_PARDISO


/* DATA CUSTOMIZATIONS (depending on memory manager)-----------------------   */
// We do not need memory allocation functions if EMBEDDED is enabled
#ifndef EMBEDDED
/* define custom printfs and memory allocation (e.g. matlab or python) */
#ifdef MATLAB
    #include "mex.h"
    static void* c_calloc(size_t num, size_t size){
        void *m = mxCalloc(num,size);
        mexMakeMemoryPersistent(m);
        return m;
    }
    static void* c_malloc(size_t size){
        void *m = mxMalloc(size);
        mexMakeMemoryPersistent(m);
        return m;
    }
    static void* c_realloc(void *ptr, size_t size){
        void *m = mxRealloc(ptr,size);
        mexMakeMemoryPersistent(m);
        return m;
    }
    #define c_free mxFree
#elif defined PYTHON
    // Define memory allocation for python. Note that in Python 2 memory manager
    // Calloc is not implemented
    #include <Python.h>
    #define c_malloc PyMem_Malloc
    #if PY_MAJOR_VERSION >= 3
    #define c_calloc PyMem_Calloc
    #else
    static void * c_calloc(size_t num, size_t size){
      void *m = PyMem_Malloc(num*size);
      memset(m, 0, num*size);
      return m;
    }
    #endif
    // #define c_calloc(n,s) ({
    //         void * p_calloc = c_malloc((n)*(s));
    //         memset(p_calloc, 0, (n)*(s));
    //         p_calloc;
    //     })
    #define c_free PyMem_Free
    #define c_realloc PyMem_Realloc
#else
    #define c_malloc malloc
    #define c_calloc calloc
    #define c_free free
    #define c_realloc realloc
#endif

#include <stdlib.h>


#endif  //end EMBEDDED


/* Use customized number representation -----------------------------------   */
#ifdef DLONG  // long integers
typedef long long c_int;             /* for indices */
#else  // standard integers
typedef int c_int;                   /* for indices */
#endif


#ifndef DFLOAT // Doubles
typedef double c_float;              /* for numerical values  */
#else         // Floats
typedef float c_float;                /* for numerical values  */
#endif



/* Use customized constants -----------------------------------------------   */
#ifndef OSQP_NULL
#define OSQP_NULL 0
#endif

#ifndef OSQP_NAN
#define OSQP_NAN ((c_float)0x7ff8000000000000)     // Not a Number
#endif

#ifndef OSQP_INFTY
#define OSQP_INFTY ((c_float)1e20)   // Infinity
#endif

/* Use customized operations */

#ifndef c_absval
#define c_absval(x) (((x) < 0) ? -(x) : (x))
#endif

#ifndef c_max
#define c_max(a, b) (((a) > (b)) ? (a) : (b))
#endif

#ifndef c_min
#define c_min(a, b) (((a) < (b)) ? (a) : (b))
#endif

// Round x to the nearest multiple of N
#ifndef c_roundmultiple
#define c_roundmultiple(x, N) ((x) + .5 * (N) - c_fmod((x) + .5 * (N), (N)))
#endif


/* Use customized functions -----------------------------------------------   */

#if EMBEDDED != 1

#include <math.h>
#ifndef DFLOAT // Doubles
#define c_sqrt sqrt
#define c_fmod fmod
#else         // Floats
#define c_sqrt sqrtf
#define c_fmod fmodf
#endif

#endif // end EMBEDDED


#ifdef PRINTING
#include <stdio.h>
#include <string.h>

#ifdef MATLAB
#define c_print mexPrintf
// The following trick slows down the performance a lot. Since many solvers actually
//call mexPrintf and immediately force print buffer flush
//otherwise messages don't appear until solver termination
//ugly because matlab does not provide a vprintf mex interface
// #include <stdarg.h>
// static int c_print(char *msg, ...)
// {
//   va_list argList;
//   va_start(argList, msg);
//   //message buffer
//   int bufferSize = 256;
//   char buffer[bufferSize];
//   vsnprintf(buffer,bufferSize-1, msg, argList);
//   va_end(argList);
//   int out = mexPrintf(buffer); //print to matlab display
//   mexEvalString("drawnow;");   // flush matlab print buffer
//   return out;
// }
#elif defined PYTHON
#include <Python.h>
#define c_print PySys_WriteStdout
#else
#define c_print printf
#endif

#endif


#ifdef __cplusplus
}
#endif

#endif

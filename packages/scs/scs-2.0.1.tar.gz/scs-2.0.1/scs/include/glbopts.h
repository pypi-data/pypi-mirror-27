#ifndef GLB_H_GUARD
#define GLB_H_GUARD

#ifdef __cplusplus
extern "C" {
#endif

#include <math.h>

/* redefine printfs and memory allocators as needed */
#ifdef MATLAB_MEX_FILE
#include "mex.h"
#define scs_printf mexPrintf
#define _scs_free mxFree
#define _scs_malloc mxMalloc
#define _scs_calloc mxCalloc
#define _scs_realloc mxRealloc
#elif defined PYTHON
#include <Python.h>
#include <stdlib.h>
#define scs_printf(...)                                                        \
  {                                                                            \
    PyGILState_STATE gilstate = PyGILState_Ensure();                           \
    PySys_WriteStdout(__VA_ARGS__);                                            \
    PyGILState_Release(gilstate);                                              \
  }
#define _scs_free free
#define _scs_malloc malloc
#define _scs_calloc calloc
#define _scs_realloc realloc
#elif(defined(USING_R))
#include <R_ext/Print.h> /* Rprintf etc */
#include <stdio.h>
#include <stdlib.h>
#define scs_printf Rprintf
#define _scs_free free
#define _scs_malloc malloc
#define _scs_calloc calloc
#define _scs_realloc realloc
#else
#include <stdio.h>
#include <stdlib.h>
#define scs_printf printf
#define _scs_free free
#define _scs_malloc malloc
#define _scs_calloc calloc
#define _scs_realloc realloc
#endif

#define scs_free(x)                                                            \
  _scs_free(x);                                                                \
  x = SCS_NULL
#define scs_malloc(x) _scs_malloc(x)
#define scs_calloc(x, y) _scs_calloc(x, y)
#define scs_realloc(x, y) _scs_realloc(x, y)

#ifdef LONG
#ifdef _WIN64
typedef __int64 scs_int;
/* #define scs_int __int64 */
#else
typedef long scs_int;
/* #define scs_int long */
#endif
#else
typedef int scs_int;
/* #define scs_int int */
#endif

#ifndef FLOAT
typedef double scs_float;
#ifndef NAN
#define NAN ((scs_float)0x7ff8000000000000)
#endif
#ifndef INFINITY
#define INFINITY NAN
#endif
#else
typedef float scs_float;
#ifndef NAN
#define NAN ((float)0x7fc00000)
#endif
#ifndef INFINITY
#define INFINITY NAN
#endif
#endif

#define SCS_NULL 0

#ifndef MAX
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#endif

#ifndef MIN
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#endif

#ifndef ABS
#define ABS(x) (((x) < 0) ? -(x) : (x))
#endif

#ifndef POWF
#ifdef FLOAT
#define POWF powf
#else
#define POWF pow
#endif
#endif

#ifndef SQRTF
#ifdef FLOAT
#define SQRTF sqrtf
#else
#define SQRTF sqrt
#endif
#endif

#if EXTRA_VERBOSE > 1
#if (defined _WIN32 || defined _WIN64 || defined _WINDLL)
#define __func__ __FUNCTION__
#endif
#define DEBUG_FUNC                                                             \
  scs_printf("IN function: %s, time: %4f ms, file: %s, line: %i\n", __func__,  \
             tocq(&global_timer), __FILE__, __LINE__);
#define RETURN                                                                 \
  scs_printf("EXIT function: %s, time: %4f ms, file: %s, line: %i\n",          \
             __func__, tocq(&global_timer), __FILE__, __LINE__);               \
  return
#else
#define DEBUG_FUNC
#define RETURN return
#endif

#define EPS_TOL (1E-18)
#define SAFEDIV_POS(X, Y) ((Y) < EPS_TOL ? ((X) / EPS_TOL) : (X) / (Y))

#ifdef __cplusplus
}
#endif
#endif

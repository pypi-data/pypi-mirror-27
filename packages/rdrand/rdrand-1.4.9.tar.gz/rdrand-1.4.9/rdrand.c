/*
 * Copyright (c) 2013, 2017 Chris Stillson <stillson@gmail.com>
 * All rights reserved.
 *
 * portions of this code
 * Copyright � 2012, Intel Corporation.  All rights reserved.
 * (Namely, the cpuid checking code)
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef _LP64
#define IS64BIT 1
#else
#define IS32BIT 1
#endif

#ifdef __GNUC__
#define USING_GCC 1
#elif __clang__
#define USING_CLANG 1
#else
#error Only support for gcc or clang currently
#error if you port to another compiler, please
#error send back the patch to https://github.com/stillson/rdrand
#endif

#if PY_MAJOR_VERSION == 2
#define PYTHON2 1
#elif PY_MAJOR_VERSION == 3
#define PYTHON3 1
#else
#error requires python 2 or 3
#endif

uint64_t get_bits_using_rdrand(void);
uint64_t get_bits_using_rdseed(void);
int RdRand_cpuid(void);
int RdSeed_cpuid(void);

PyDoc_STRVAR(module_doc, "rdrand: Python interface to Intel and AMD hardware RNG\n");

/*! \brief Queries cpuid to see if rdrand is supported
 *
 * rdrand support in a CPU is determined by examining the 30th bit of the ecx
 * register after calling cpuid.
 *
 * \return bool of whether or not rdrand is supported
 */

/*! \def RDRAND_MASK
 *    The bit mask used to examine the ecx register returned by cpuid. The
 *   30th bit is set.
 */
#define RDRAND_MASK   0x40000000


/*! \def RDSEED_MASK
 *    The bit mask used to examine the ebx register returned by cpuid. The
 *   18th bit is set.
 */
#define RDSEED_MASK   0x00040000

# define __cpuid(x,y,s) asm("cpuid":"=a"(x[0]),"=b"(x[1]),"=c"(x[2]),"=d"(x[3]):"a"(y),"c"(s))

void
cpuid(unsigned int op, unsigned int subfunc, unsigned int reg[4])
{

#if USING_GCC && IS64BIT
    __cpuid(reg, op, subfunc);
#else
    asm volatile("pushl %%ebx      \n\t" /* save %ebx */
                 "cpuid            \n\t"
                 "movl %%ebx, %1   \n\t" /* save what cpuid just put in %ebx */
                 "popl %%ebx       \n\t" /* restore the old %ebx */
                 : "=a"(reg[0]), "=r"(reg[1]), "=c"(reg[2]), "=d"(reg[3])
                 : "a"(op), "c"(subfunc)
                 : "cc");
#endif
}

int
RdRand_cpuid(void)
{
    unsigned int info[4] = {-1, -1, -1, -1};

    /* Are we on an Intel or AMD processor? */

    cpuid(0, 0, info);

    if (!(( memcmp((void *) &info[1], (void *) "Genu", 4) == 0 &&
        memcmp((void *) &info[3], (void *) "ineI", 4) == 0 &&
        memcmp((void *) &info[2], (void *) "ntel", 4) == 0 )
        ||
        ( memcmp((void *) &info[1], (void *) "Auth", 4) == 0 &&
        memcmp((void *) &info[3], (void *) "enti", 4) == 0 &&
        memcmp((void *) &info[2], (void *) "cAMD", 4) == 0 )))
        return 0;

    /* Do we have RDRAND? */
    cpuid(1, 0, info);

    int ecx = info[2];
    if ((ecx & RDRAND_MASK) == RDRAND_MASK)
        return 1;
    else
        return 0;
}


int
RdSeed_cpuid(void)
{
    unsigned int info[4] = {-1, -1, -1, -1};

    /* Are we on an Intel or AMD processor? */
    cpuid(0, 0, info);

    if (!(( memcmp((void *) &info[1], (void *) "Genu", 4) == 0 &&
        memcmp((void *) &info[3], (void *) "ineI", 4) == 0 &&
        memcmp((void *) &info[2], (void *) "ntel", 4) == 0 )
        ||
        ( memcmp((void *) &info[1], (void *) "Auth", 4) == 0 &&
        memcmp((void *) &info[3], (void *) "enti", 4) == 0 &&
        memcmp((void *) &info[2], (void *) "cAMD", 4) == 0 )))
        return 0;

    /* Do we have RDSEED? */
    cpuid(7, 0, info);
    int ebx = info[1];
    if ((ebx & RDSEED_MASK) == RDSEED_MASK)
        return 1;
    else
        return info[1];
}

#if IS64BIT
//utility to return 64 random bits from RdRand
uint64_t
get_bits_using_rdrand(void)
{
    unsigned long int rando = 0;
    unsigned char err = 0;

    // Yes, this is inline assembly.
    // should never really fail, may have
    // to reexamine for future versions
    do
    {
#if USING_GCC
        asm volatile(".byte 0x48; .byte 0x0f; .byte 0xc7; .byte 0xf0; setc %1":"=a"(rando), "=qm"(err));

#elif USING_CLANG
        asm("rdrandq %0;\n\t" "setc %1" :"=a"(rando),"=qm"(err) : :);
#endif

    } while (err == 0);

    return rando;
}
#elif IS32BIT
uint64_t
get_bits_using_rdrand(void)
{
    unsigned char err = 0;
    union{
       uint64_t rando;
       struct {
          uint32_t rando1;
          uint32_t rando2;
       } i;
    } un;

    // Yes, this is inline assembly.
    // should never really fail, may have
    // to reexamine for future versions
    do
    {
#if USING_GCC
        asm volatile(".byte 0x0f; .byte 0xc7; .byte 0xf0; setc %1":"=a"(un.i.rando1), "=qm"(err));
#elif USING_CLANG
        asm("rdrandw %0;\n\t" "setc %1" :"=a"(un.i.rando1),"=qm"(err) : :);
#endif
    } while (err == 0);

    do
    {
#if USING_GCC
        asm volatile(".byte 0x0f; .byte 0xc7; .byte 0xf0; setc %1":"=a"(un.i.rando2), "=qm"(err));
#elif USING_CLANG
        asm("rdrandw %0;\n\t" "setc %1" :"=a"(un.i.rando2),"=qm"(err) : :);
#endif
    } while (err == 0);

    return un.rando;
}
#endif

#if IS64BIT
//utility to return 64 random bits from RdSeed
uint64_t
get_bits_using_rdseed(void)
{
    unsigned long int rando = 0;
    unsigned char err = 0;

    // Yes, this is inline assembly.
    // should never really fail, may have
    // to reexamine for future versions
    do
    {
#if USING_GCC
        asm volatile(".byte 0x48; .byte 0x0f; .byte 0xc7; .byte 0xf8; setc %1":"=a"(rando), "=qm"(err));

#elif USING_CLANG
        asm("rdseedq %0;\n\t" "setc %1" :"=a"(rando),"=qm"(err) : :);
#endif

    } while (err == 0);

    return rando;
}
#elif IS32BIT
uint64_t
get_bits_using_rdseed(void)
{
    unsigned char err = 0;
    union{
       uint64_t rando;
       struct {
          uint32_t rando1;
          uint32_t rando2;
       } i;
    } un;

    // Yes, this is inline assembly.
    // should never really fail, may have
    // to reexamine for future versions
    do
    {
#if USING_GCC
        asm volatile(".byte 0x0f; .byte 0xc7; .byte 0xf8; setc %1":"=a"(un.i.rando1), "=qm"(err));
#elif USING_CLANG
        asm("rdseedw %0;\n\t" "setc %1" :"=a"(un.i.rando1),"=qm"(err) : :);
#endif
    } while (err == 0);

    do
    {
#if USING_GCC
        asm volatile(".byte 0x0f; .byte 0xc7; .byte 0xf8; setc %1":"=a"(un.i.rando2), "=qm"(err));
#elif USING_CLANG
        asm("rdseedw %0;\n\t" "setc %1" :"=a"(un.i.rando2),"=qm"(err) : :);
#endif
    } while (err == 0);

    return un.rando;
}
#endif

static PyObject *
rdrand_get_bits(PyObject *self, PyObject *args)
{
    int num_bits, num_bytes, i;
    int num_quads, num_chars;
    unsigned char * data = NULL;
    uint64_t rando;
    unsigned char last_mask, lm_shift;
    PyObject *result;

    if ( !PyArg_ParseTuple(args, "i", &num_bits) )
        return NULL;

    if (num_bits <= 0)
    {
        PyErr_SetString(PyExc_ValueError, "number of bits must be greater than zero");
        return NULL;
    }

    num_bytes   = num_bits / 8;
    lm_shift    = num_bits % 8;
    last_mask   = 0xff >> (8 - lm_shift);

    if (lm_shift)
        num_bytes++;

    num_quads   = num_bytes / 8;
    num_chars   = num_bytes % 8;
    data        = (unsigned char *)PyMem_Malloc(num_bytes);

    if (data == NULL)
    {
        PyErr_NoMemory();
        return NULL;
    }

    for(i = 0; i < num_quads; i++)
    {
        rando = get_bits_using_rdrand();
        bcopy((char*)&rando, &data[i * 8], 8);
    }

    if(num_chars)
    {
        rando = get_bits_using_rdrand();
        bcopy((char*)&rando, &data[num_quads * 8], num_chars);
    }

    if (lm_shift != 0)
        data[num_bytes -1] &= last_mask;

    /* Probably hosing byte order. big deal it's hardware random, has no meaning til we assign it */
    result = _PyLong_FromByteArray(data, num_bytes, 1, 0);
    PyMem_Free(data);
    return result;
}

static PyObject *
rdseed_get_bits(PyObject *self, PyObject *args)
{
    int num_bits, num_bytes, i;
    int num_quads, num_chars;
    unsigned char * data = NULL;
    uint64_t rando;
    unsigned char last_mask, lm_shift;
    PyObject *result;

    if ( !PyArg_ParseTuple(args, "i", &num_bits) )
        return NULL;

    if (num_bits <= 0)
    {
        PyErr_SetString(PyExc_ValueError, "number of bits must be greater than zero");
        return NULL;
    }

    num_bytes   = num_bits / 8;
    lm_shift    = num_bits % 8;
    last_mask   = 0xff >> (8 - lm_shift);

    if (lm_shift)
        num_bytes++;

    num_quads   = num_bytes / 8;
    num_chars   = num_bytes % 8;
    data        = (unsigned char *)PyMem_Malloc(num_bytes);

    if (data == NULL)
    {
        PyErr_NoMemory();
        return NULL;
    }

    for(i = 0; i < num_quads; i++)
    {
        rando = get_bits_using_rdseed();
        bcopy((char*)&rando, &data[i * 8], 8);
    }

    if(num_chars)
    {
        rando = get_bits_using_rdseed();
        bcopy((char*)&rando, &data[num_quads * 8], num_chars);
    }

    if (lm_shift != 0)
        data[num_bytes -1] &= last_mask;

    /* Probably hosing byte order. big deal it's hardware random, has no meaning til we assign it */
    result = _PyLong_FromByteArray(data, num_bytes, 1, 0);
    PyMem_Free(data);
    return result;
}
static PyObject *
rdrand_get_bytes(PyObject *self, PyObject *args)
{
    int num_bytes, i;
    int num_quads, num_chars;
    unsigned char * data = NULL;
    uint64_t rando;
    PyObject *result;

    if ( !PyArg_ParseTuple(args, "i", &num_bytes) )
        return NULL;

    if (num_bytes <= 0)
    {
        PyErr_SetString(PyExc_ValueError, "number of bytes must be greater than zero");
        return NULL;
    }

    data        = (unsigned char *)PyMem_Malloc(num_bytes);
    num_quads   = num_bytes / 8;
    num_chars   = num_bytes % 8;

    if (data == NULL)
    {
        PyErr_NoMemory();
        return NULL;
    }

    for(i = 0; i < num_quads; i++)
    {
        rando = get_bits_using_rdrand();
        bcopy((char*)&rando, &data[i * 8], 8);
    }

    if(num_chars)
    {
        rando = get_bits_using_rdrand();
        bcopy((char*)&rando, &data[num_quads * 8], num_chars);
    }

    /* Probably hosing byte order. big deal it's hardware random, has no meaning til we assign it */
#if PYTHON2 == 1
    result = Py_BuildValue("s#", data, num_bytes);
#else
    result = Py_BuildValue("y#", data, num_bytes);
#endif
    PyMem_Free(data);
    return result;
}


static PyObject *
rdseed_get_bytes(PyObject *self, PyObject *args)
{
    int num_bytes, i;
    int num_quads, num_chars;
    unsigned char * data = NULL;
    uint64_t rando;
    PyObject *result;

    if ( !PyArg_ParseTuple(args, "i", &num_bytes) )
        return NULL;

    if (num_bytes <= 0)
    {
        PyErr_SetString(PyExc_ValueError, "number of bytes must be greater than zero");
        return NULL;
    }

    data        = (unsigned char *)PyMem_Malloc(num_bytes);
    num_quads   = num_bytes / 8;
    num_chars   = num_bytes % 8;

    if (data == NULL)
    {
        PyErr_NoMemory();
        return NULL;
    }

    for(i = 0; i < num_quads; i++)
    {
        rando = get_bits_using_rdseed();
        bcopy((char*)&rando, &data[i * 8], 8);
    }

    if(num_chars)
    {
        rando = get_bits_using_rdseed();
        bcopy((char*)&rando, &data[num_quads * 8], num_chars);
    }

    /* Probably hosing byte order. big deal it's hardware random, has no meaning til we assign it */
#if PYTHON2 == 1
    result = Py_BuildValue("s#", data, num_bytes);
#else
    result = Py_BuildValue("y#", data, num_bytes);
#endif
    PyMem_Free(data);
    return result;
}
static PyMethodDef rdrand_functions[] = {
        {"rdrand_get_bits",       rdrand_get_bits,        METH_VARARGS, "rdrand_get_bits()"},
        {"rdrand_get_bytes",      rdrand_get_bytes,       METH_VARARGS, "rdrand_get_bytes()"},
        {"rdseed_get_bits",       rdseed_get_bits,        METH_VARARGS, "rdseed_get_bits()"},
        {"rdseed_get_bytes",      rdseed_get_bytes,       METH_VARARGS, "rdseed_get_bytes()"},
        {NULL, NULL, 0, NULL}   /* Sentinel */
};

#if PYTHON2 == 1
PyMODINIT_FUNC
init_rdrand(void)
{
        PyObject *m;
        int has_rand, has_seed;

        // I need to verify that cpu type can do rdrand
        has_rand = 1;
        if (RdRand_cpuid() != 1)
            has_rand = 0;

        has_seed = 1;
        if (RdSeed_cpuid() != 1)
            has_seed = 0;

        m = Py_InitModule3("_rdrand", rdrand_functions, module_doc);
        if (m == NULL)
            return;

        PyModule_AddIntConstant(m, "HAS_RAND", has_rand);
        PyModule_AddIntConstant(m, "HAS_SEED", has_seed);
}
#else
static struct PyModuleDef rdrandmodule = {
   PyModuleDef_HEAD_INIT, "_rdrand", module_doc, -1, rdrand_functions
};

PyMODINIT_FUNC
PyInit__rdrand(void)
{
        PyObject *m;
        int has_rand, has_seed;

        // I need to verify that cpu type can do rdrand
        has_rand = 1;
        if (RdRand_cpuid() != 1)
            has_rand = 0;

        has_seed = 1;
        if (RdSeed_cpuid() != 1)
            has_seed = 0;

        m = PyModule_Create(&rdrandmodule);
        if (m == NULL)
            return NULL;

        PyModule_AddIntConstant(m, "HAS_RAND", has_rand);
        PyModule_AddIntConstant(m, "HAS_SEED", has_seed);

        return m;
}


#endif

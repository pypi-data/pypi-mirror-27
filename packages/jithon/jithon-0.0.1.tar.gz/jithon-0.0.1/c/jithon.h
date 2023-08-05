// Copyright 2017 ibelie, Chen Jie, Joungtao. All rights reserved.
// Use of this source code is governed by The MIT License
// that can be found in the LICENSE file.

#ifndef JITHON_H__
#define JITHON_H__

#ifdef _MSC_VER
#	ifndef HAVE_ROUND
#		define HAVE_ROUND
#	endif
#endif
#define PY_SSIZE_T_CLEAN

#define IblPrint_Info PySys_WriteStdout
#define IblPrint_Warn PySys_WriteStdout
#define IblPrint_Err  PySys_WriteStderr

#include "Python.h"
#include "port.h"

#define PY_MODULE_NAME "jithon"
#define FULL_MODULE_NAME "_" PY_MODULE_NAME

#ifndef PyVarObject_HEAD_INIT
#	define PyVarObject_HEAD_INIT(type, size) PyObject_HEAD_INIT(type) size,
#endif
#ifndef Py_TYPE
#	define Py_TYPE(ob) (((PyObject*)(ob))->ob_type)
#endif
#ifndef PyUnbound_Check
#	define PyUnbound_Check(ob) (Py_TYPE(ob)->tp_descr_get && !Py_TYPE(ob)->tp_descr_set && \
		!PyMethod_Check(ob) && !PyFunction_Check(ob) && !PyType_Check(ob) && !PyClass_Check(ob) && \
		!PyObject_TypeCheck(ob, &PyClassMethod_Type) && !PyObject_TypeCheck(ob, &PyStaticMethod_Type))
#endif

#if PY_MAJOR_VERSION >= 3
#	define PyInt_Check PyLong_Check
#	define PyInt_AsLong PyLong_AsLong
#	define PyInt_FromLong PyLong_FromLong
#	define PyInt_FromSize_t PyLong_FromSize_t
#	define PyString_Check PyUnicode_Check
#	define PyString_FromString PyUnicode_FromString
#	define PyString_FromStringAndSize PyUnicode_FromStringAndSize
#	if PY_VERSION_HEX < 0x03030000
#		error "Python 3.0 - 3.2 are not supported."
#	else
#		define PyString_AsString(ob) \
			(PyUnicode_Check(ob) ? PyUnicode_AsUTF8(ob) : PyBytes_AsString(ob))
#		define PyString_AsStringAndSize(ob, charpp, sizep) \
			(PyUnicode_Check(ob) ? \
				(!(*(charpp) = PyUnicode_AsUTF8AndSize(ob, (sizep)))? -1 : 0) : \
				PyBytes_AsStringAndSize(ob, (charpp), (sizep)))
#	endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

extern char* JithonPath;

void FormatTypeError(PyObject*, const char*);

PyBytesObject* Jithon_CheckBytes(PyObject*, const char*);

// Params: module, function, args_format, args
// int Jithon_RunJavascript(const char*, const char*, const char*, ...);

// Virtual function to initialize on different platform.
// return 0: success, -1: fail
int Jithon_Init(const char*);

// Virtual function to run javascript code on different platform.
// return 0: success, -1: fail
int Jithon_RunString(const char*);

// Virtual function to run python code on different platform.
// Params: function, args tuple
// return 0: success, -1: fail
int Jithon_RunPython(const char*, PyObject*);

// Virtual function to read javascript source code on different platform.
char* Jithon_ReadFile(const char*);

#ifdef __cplusplus
}
#endif

#endif // JITHON_H__

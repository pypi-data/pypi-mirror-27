// Copyright 2017 ibelie, Chen Jie, Joungtao. All rights reserved.
// Use of this source code is governed by The MIT License
// that can be found in the LICENSE file.

#include "jithon.h"
#include "longintrepr.h"

#ifdef __cplusplus
extern "C" {
#endif

void FormatTypeError(PyObject* arg, const char* err) {
	PyObject* repr = PyObject_Repr(arg);
	if (!repr) { return; }
	PyErr_Format(PyExc_TypeError, "%.100s%.100s has type %.100s",
		err, PyString_AsString(repr), Py_TYPE(arg)->tp_name);
	Py_DECREF(repr);
}

PyBytesObject* Jithon_CheckBytes(PyObject* arg, const char* err) {
	if (!arg || arg == Py_None) {
		FormatTypeError(arg, err);
		return NULL;
	} else if (PyUnicode_Check(arg)) {
		return (PyBytesObject*)PyUnicode_AsEncodedObject(arg, "utf-8", NULL);
	} else if (PyBytes_Check(arg)) {
		Py_INCREF(arg);
		return (PyBytesObject*)arg;
	} else {
		FormatTypeError(arg, err);
		return NULL;
	}
}

static const char JithonJS[] =
"var $;"
"(function ($) {"
	"$.p = $.p || function(s) {"
		"window.webkit.messageHandlers.p.postMessage([s]);"
	"};"
"})($ || ($ = {}));";

char* JithonPath = NULL;

static const char module_docstring[] =
"_jithon is a module that can run javascript(compiled python) in a embedded browser.";

static PyObject* SetPath(PyObject* _, PyObject* arg) {
	register PyBytesObject* path = Jithon_CheckBytes(arg, "SetPath expect path string, but ");
	if (!path) { return NULL; }

	register PyObject* modules = PyImport_GetModuleDict();
	if (!modules) { return NULL; }

	register PyObject* m = PyDict_GetItemString(modules, PY_MODULE_NAME);
	if (!m) {
		PyErr_Format(PyExc_ImportError, "No module named " PY_MODULE_NAME);
		return NULL;
	}

	register int err = PyObject_SetAttrString(m, "JITHONPATH", (PyObject*)path);
	Py_DECREF(path);
	if (err < 0) { return NULL; }

	JithonPath = PyBytes_AS_STRING(path);

	Py_RETURN_NONE;
}

static PyObject* TestCase(PyObject* _) {
	register char* buf = Jithon_ReadFile("testcase");
	if (buf) {
		Jithon_RunString(buf);
		free(buf);
	} else {
		PySys_WriteStdout("Cannot read testcase!\n");
	}

	Py_RETURN_NONE;
}

static PyMethodDef ModuleMethods[] = {
	{"setPath", (PyCFunction)SetPath, METH_O,
		"set JITHONPATH."},
	{"testcase", (PyCFunction)TestCase, METH_NOARGS,
		"run testcase."},
	{ NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef _module = {
	PyModuleDef_HEAD_INIT,
	FULL_MODULE_NAME,
	module_docstring,
	-1,
	ModuleMethods, /* m_methods */
	NULL,
	NULL,
	NULL,
	NULL
};
#	ifndef INITFUNC
#		define INITFUNC PyInit__jithon
#	endif
#	define INITFUNC_ERRORVAL NULL
#else // Python 2
#	ifndef INITFUNC
#		define INITFUNC init_jithon
#	endif
#	define INITFUNC_ERRORVAL
#endif

PyMODINIT_FUNC INITFUNC(void) {
	PyObject* m;
#if PY_MAJOR_VERSION >= 3
	m = PyModule_Create(&_module);
#else
	m = Py_InitModule3(FULL_MODULE_NAME, ModuleMethods, module_docstring);
#endif
	if (!m) { return INITFUNC_ERRORVAL; }

	if (Jithon_Init(JithonJS) < 0) {
		PyErr_Format(PyExc_RuntimeError, "Jithon Initialize failed!");
		Py_DECREF(m);
		return INITFUNC_ERRORVAL;
	}

#if PY_MAJOR_VERSION >= 3
	return m;
#endif
}

#ifdef __cplusplus
}
#endif

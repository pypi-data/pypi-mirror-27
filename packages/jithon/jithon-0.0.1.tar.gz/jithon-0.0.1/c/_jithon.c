// Copyright 2017 ibelie, Chen Jie, Joungtao. All rights reserved.
// Use of this source code is governed by The MIT License
// that can be found in the LICENSE file.

#include "jithon.h"

#ifdef __cplusplus
extern "C" {
#endif

int Jithon_RunPython(const char* name, PyObject* args) {
	register PyObject* jithon = PyImport_ImportModule(PY_MODULE_NAME);
	if (!jithon) { return -1; }

	register PyObject* result = PyObject_CallMethod(jithon, "delegate", "(sO)", name, args);
	Py_DECREF(jithon);
	if (!result) { return -1; }
	Py_DECREF(result);
	return 0;
}

char* Jithon_ReadFile(const char* filename) {
	register PyObject* fullname = PyString_FromFormat("%s/%s.js", JithonPath, filename);
	if (!fullname) { return NULL; }

	register PyObject* file = PyFile_FromString(PyString_AS_STRING(fullname), "rb");
	Py_DECREF(fullname);
	if (!file) { return NULL; }

	register PyObject* content = PyObject_CallMethod(file, "read", NULL);
	Py_DECREF(file);
	if (!content) { return NULL; }

	register Py_ssize_t size = PyString_GET_SIZE(content);
	char* buf = (char*)calloc(size + 1, sizeof(char));
	if (buf) {
		memcpy(buf, PyString_AS_STRING(content), size * sizeof(char));
	}
	Py_DECREF(content);
	return buf;
}

#ifdef __cplusplus
}
#endif

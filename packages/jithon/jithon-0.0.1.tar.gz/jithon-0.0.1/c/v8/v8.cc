// Copyright 2017 ibelie, Chen Jie, Joungtao. All rights reserved.
// Use of this source code is governed by The MIT License
// that can be found in the LICENSE file.

#include "jithon.h"

#ifdef __cplusplus
extern "C" {
#endif

int Jithon_Init(const char* s) {
	IblPrint_Info("[Jithon] Initialize v8.\n");
	return 0;
}

int Jithon_RunString(const char* s) {
	IblPrint_Err("[Jithon] Not implemented: v8.\n");
	return -1;
}

#ifdef __cplusplus
}
#endif

// Copyright 2017 ibelie, Chen Jie, Joungtao. All rights reserved.
// Use of this source code is governed by The MIT License
// that can be found in the LICENSE file.

#include "jithon.h"

#include <WebKit/WebKit.h>

static inline void _PyPrintString(const char* s) {
	PyObject* args = PyTuple_New(1);
	((PyTupleObject*)args)->ob_item[0] = PyString_FromString(s);
	Jithon_RunPython("p", args);
	Py_XDECREF(args);
}

static PyObject* _ConvertNSPy(id data) {
	if ([data isKindOfClass:[NSNumber class]]) {
		// TODO check number type
		return PyInt_FromLong([(NSNumber*)data intValue]);
	} else if ([data isKindOfClass:[NSString class]]) {
		return PyString_FromString([data UTF8String]);
	} else if ([data isKindOfClass:[NSData class]]) {
		_PyPrintString([[NSString stringWithFormat:@"[Jithon] NSData[%@] of not implemented", data] UTF8String]);
		Py_RETURN_NONE;
	} else if ([data isKindOfClass:[NSArray class]]) {
		NSArray* array = (NSArray*)data;
		PyObject* args = PyTuple_New(array.count);
		if (!args) {
			_PyPrintString([[NSString stringWithFormat:@"[Jithon] NSArray[%@] out of memory: %lu", array, array.count] UTF8String]);
			return NULL;
		}
		PyObject** items = ((PyTupleObject*)args)->ob_item;
		for (Py_ssize_t i = 0; i < array.count; i++) {
			items[i] = _ConvertNSPy([array objectAtIndex:i]);
		}
		return args;
	} else if ([data isKindOfClass:[NSDictionary class]]) {
		_PyPrintString([[NSString stringWithFormat:@"[Jithon] NSDictionary[%@] of not implemented", data] UTF8String]);
		Py_RETURN_NONE;
	} else if ([data isKindOfClass:[NSNull class]]) {
		Py_RETURN_NONE;
	} else {
		_PyPrintString([[NSString stringWithFormat:@"[Jithon] Cannot convert param[%@]", data] UTF8String]);
		return NULL;
	}
}

@interface JithonDelegate: NSObject

- (void)userContentController:(WKUserContentController*)userContentController didReceiveScriptMessage:(WKScriptMessage*)message;

@end

@implementation JithonDelegate

- (void)userContentController:(WKUserContentController*)userContentController didReceiveScriptMessage:(WKScriptMessage*)message {
	PyObject* args = _ConvertNSPy(message.body);
	Jithon_RunPython([message.name UTF8String], args);
	Py_XDECREF(args);
}

@end

static WKWebView* webView = nil;

int Jithon_Init(const char* s) {
	if (webView != nil) { return 0; }

	JithonDelegate* delegate = [[JithonDelegate alloc]init];

	WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
	config.userContentController = [[WKUserContentController alloc] init];
	[config.userContentController addScriptMessageHandler:(id<WKScriptMessageHandler>)delegate name:@"p"];
	[config.userContentController addScriptMessageHandler:(id<WKScriptMessageHandler>)delegate name:@"commonFunction"];
	[config.userContentController addScriptMessageHandler:(id<WKScriptMessageHandler>)delegate name:@"onTestcaseStart"];
	[config.userContentController addScriptMessageHandler:(id<WKScriptMessageHandler>)delegate name:@"onTestcaseEnd"];

	webView = [[WKWebView alloc] initWithFrame:CGRectMake(0, 10, 500, 300) configuration:config];
	[webView evaluateJavaScript:[NSString stringWithUTF8String:s] completionHandler:^(id _Nullable data, NSError* _Nullable error) {
		if (error != nil) {
			_PyPrintString([[NSString stringWithFormat:@"[Jithon] Initialize error: %@", error] UTF8String]);
		} else {
			_PyPrintString("[Jithon] Initialize OK!");
		}
	}];

	return 0;
}

int Jithon_RunString(const char* s) {
	if (webView == nil) {
		_PyPrintString("[Jithon] Web View is nil!");
		return -1;
	}

	[webView evaluateJavaScript:[NSString stringWithUTF8String:s] completionHandler:^(id _Nullable data, NSError* _Nullable error) {
		if (error != nil) {
			_PyPrintString([[NSString stringWithFormat:@"[Jithon] RunString - evaluateJavaScript error: %@", error] UTF8String]);
		} else {
			_PyPrintString([[NSString stringWithFormat:@"[Jithon] RunString - evaluateJavaScript data: %@", data] UTF8String]);
		}
	}];

	return 0;
}

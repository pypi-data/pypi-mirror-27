/*
 * utils.cpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#include "utils.hpp"
#include "notifier/notifier.hpp"


PyObject *maskAsString(PyObject *args,PyObject *keywords) {
	int mask;
	if(!PyArg_ParseTuple(args,"I",&mask)) {
		PyErr_SetString(PyExc_ValueError,"Cannot parse arguments");
		return NULL;
	}
	notify::Event e(mask,"");
	std::stringstream stream;
	stream << e;
	PyObject *str=PyUnicode_FromString(stream.str().c_str());
	if(str==NULL) {
		PyErr_SetString(PyExc_SystemError,"Cannot allocate string value");
		return NULL;
	}
	return str;
}



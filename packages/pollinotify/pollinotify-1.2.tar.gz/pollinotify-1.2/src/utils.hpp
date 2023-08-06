/*
 * utils.hpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#ifndef UTILS_HPP_
#define UTILS_HPP_

#include <list>
#include <string>
#include <iostream>
#include <python3.5/Python.h>
#include <python3.5/structmember.h>

template<class T>
PyObject *listToPy(std::list<T> in,PyObject *(*transformer)(T))
{
	PyObject *out=PyList_New((Py_ssize_t)0);
	if(out==NULL) {
		PyErr_SetString(PyExc_SystemError,"Internal error allocating FileEvent list");
		return NULL;
	};

	for(auto it=in.begin();it!=in.end();it++) {
		auto *item=transformer(*it);

		auto r=PyList_Append(out,item);
		if(r<0) {
			PyErr_SetString(PyExc_SystemError,"Internal error building FileEvent list");
			return NULL;
		}
	}
	return out;
}


 PyObject *maskAsString(PyObject *args,PyObject *keywords);



#endif /* UTILS_HPP_ */

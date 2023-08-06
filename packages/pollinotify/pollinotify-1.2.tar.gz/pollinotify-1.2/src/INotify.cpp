/*
 * INotify.cpp
 *
 *  Created on: 30 Jun 2014
 *      Author: julianporter
 */

#include "INotify.hpp"
#include "utils.hpp"
#include "fileEvent.hpp"
#include "watcher.hpp"
#include "notifier/notifier.hpp"
#include <stdexcept>
#include <sstream>

static const char *ModuleName="pollinotify";
static const char *ErrorName="pollinotify.NotifyError";



















static PyMethodDef ModuleMethods[]={
		{"maskAsString",maskAsString,METH_VARARGS,"String representation of a mask"},
		{NULL,NULL,0,NULL}
};



static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        ModuleName,
        NULL,
        -1,
        ModuleMethods,
        NULL,
        NULL,
        NULL,
        NULL
};

PyMODINIT_FUNC PyInit_pollinotify(void)
{

    PyObject *m = PyModule_Create(&moduledef);
    if (!m) return NULL;

    INotifyError = PyErr_NewException((char *)ErrorName,NULL,NULL);
    Py_INCREF(INotifyError);
    PyModule_AddObject(m,"NotifyError",INotifyError);

    WatcherManager w;
    //inotify_WatcherType.tp_new = PyType_GenericNew;
    if (!w.isReady()) return NULL;
    w.inc();
    w.add(m,"Watcher");

    EventTypeManager et;
    //fe->tp_new = PyType_GenericNew;
    if (!et.isReady()) return NULL;
    et.inc();
    et.add(m,"FileEvent");

    for(auto it=notify::Mask::names.begin();it!=notify::Mask::names.end();it++) {
    	//std::cout << "Adding " << it->second << " for " << static_cast<uint32_t>(it->first) << std::endl;
    	PyModule_AddIntConstant(m,it->second.c_str(),notify::Mask::value(it->first));
    }

    return m;
}














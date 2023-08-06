/*
 * watcher.cpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#include "fileEvent.hpp"
#include "watcher.hpp"



 PyObject *Watcher_new(PyTypeObject *type,PyObject *args,PyObject *keywords) {
	auto self = (Watcher *)type->tp_alloc(type, 0);
	 if (self != NULL) {
		 self->notify = NULL;
	 }
	 return (PyObject *)self;
}

// Release

  void Watcher_dealloc(Watcher *self) {
	if(self->notify) {
		delete self->notify;
	}
	auto p=(PyObject *)self;
    p->ob_type->tp_free(p);
}

// Initialisation


  int Watcher_init(Watcher *self,PyObject *args,PyObject *keywords) {
	auto notifier = new notify::Notifier();
	if(notifier==NULL) {
		PyErr_SetString(PyExc_OSError,"Cannot initialise iNotify service");
		return -1;
	}
	self->notify=notifier;
	return 0;
}

// Add path

static const char *arg_mode="mode";
static char *pathKeywords[]={(char *)arg_mode,NULL};

 PyObject * Watcher_addPath(Watcher *self,PyObject *args,PyObject *keywords) {

	const char *path;
	auto mode=notify::Mask::mask_t::AllEvents;
	if(!PyArg_ParseTupleAndKeywords(args,keywords,"s|I",pathKeywords,&path,&mode)) {
		PyErr_SetString(PyExc_ValueError,"Cannot find path argument");
		return NULL;
	}
	try {
		self->notify->addPath(std::string(path),mode);
	}
	catch(...) {
		PyErr_SetString(PyExc_OSError,"Cannot add path to iNotify service");
		return NULL;
	}
	Py_RETURN_NONE;
}

// Poll

static const char *arg_timeout="timeout";
static char *pollKeywords[]={(char *)arg_timeout,NULL};


PyObject * Watcher_poll(Watcher *self,PyObject *args,PyObject *keywords) {

	unsigned int timeout=0;
	PyArg_ParseTupleAndKeywords(args,keywords,"|I",pollKeywords,&timeout);
	try {
		auto out=self->notify->waitForEvent(timeout);
		if(out) Py_RETURN_TRUE;
		else Py_RETURN_FALSE;
	}
	catch(std::exception & e) {
		PyErr_SetString(PyExc_OSError,"Error polling iNotify service");
		return NULL;
	}
}

// get the events



static const char *arg_match="match";
static char *eventsKeywords[]={(char *)arg_match,NULL};

 PyObject * Watcher_events(Watcher *self,PyObject *args,PyObject *keywords) {

	try {
		auto match=notify::Mask::mask_t::AllEvents;
		PyArg_ParseTupleAndKeywords(args,keywords,"|I",eventsKeywords,&match);
		auto events=self->notify->getEvents();
		PyObject *out=PyList_New((Py_ssize_t)0);
		if(out==NULL) {
			PyErr_SetString(PyExc_SystemError,"Internal error allocating FileEvent list");
			return NULL;
		}

		for(std::list<notify::Event>::iterator it=events.begin();it!=events.end();it++) {
			if(it->matches(match)) {
				EventTypeManager em;
				auto event=em.make();
				if(event==NULL) {
					PyErr_SetString(PyExc_SystemError,"Internal error allocating FileEvent");
					Py_XDECREF(out);
					return NULL;
				}

				PyObject *path=PyUnicode_FromString(it->path.c_str());
				PyObject *mask=PyLong_FromLong((long)(it->mask.code()));
				if(!path||!mask) {
					PyErr_SetString(PyExc_SystemError,"Internal error allocating FileEvent data");
					Py_XDECREF(out);
					Py_XDECREF(event);
					Py_XDECREF(path);
					Py_XDECREF(mask);
					return NULL;
				}

				event->mask=mask;
				event->path=path;

				int r=PyList_Append(out,(PyObject *)event);
				if(r<0) {
					PyErr_SetString(PyExc_SystemError,"Internal error building FileEvent list");
					Py_XDECREF(out);
					Py_XDECREF(event);
					Py_XDECREF(path);
					Py_XDECREF(mask);
					return NULL;
				}
			}
		}
		return out;
	}
	catch(std::exception & e) {
		PyErr_SetString(PyExc_RuntimeError,e.what());
		return NULL;
	}
}

// Number of paths

  PyObject * Watcher_nPaths(Watcher *self,PyObject *args) {
	 try {
		 return PyLong_FromSize_t(self->notify->nPaths());
	 }
	 catch(...) {
		 PyErr_SetString(PyExc_SystemError,"Cannot obtain iNotify service");
		 return  NULL;
	 }
}

// Number of events

  PyObject * Watcher_nEvents(Watcher *self,PyObject *args) {
	 try {
		 return PyLong_FromSize_t(self->notify->nEvents());
	 }
	 catch(...) {
		 PyErr_SetString(PyExc_SystemError,"Cannot obtain iNotify service");
		 return NULL;
	 }
}

 Py_ssize_t Watcher_len(Watcher *self) {
	try {
		return (Py_ssize_t)self->notify->nEvents();
	}
	catch(...) {
		PyErr_SetString(PyExc_SystemError,"Cannot obtain iNotify service");
		return -1;
	}
}

 PyObject * Watcher_getiter(Watcher *self) {
	PyObject *tmp=PyTuple_New(0);
	PyObject *list=Watcher_events(self,tmp,NULL);
	Py_XDECREF(tmp);
	if(list==NULL) {
		return NULL;
	}
	return PyObject_GetIter(list);
}



 PyMethodDef inotify_Wmethods[] = {
 		{"addPath",(PyCFunction)Watcher_addPath,METH_VARARGS|METH_KEYWORDS,"Add a path to be watched"},
 		{"poll",(PyCFunction)Watcher_poll,METH_VARARGS|METH_KEYWORDS,"Poll for events"},
 		{"events",(PyCFunction)Watcher_events,METH_VARARGS|METH_KEYWORDS,"Return all events, optionally matching some mask"},
 		{"nPaths",(PyCFunction)Watcher_nPaths,METH_NOARGS,"Number of paths registered to be watched"},
 		{"nEvents",(PyCFunction)Watcher_nEvents,METH_NOARGS,"Number of events detected"},
 		{NULL}
 };

 PyMemberDef inotify_Wmembers[] = {
 		{
 				(char *)"_notify",
 				T_OBJECT_EX,
 				offsetof(Watcher,notify),
 				READONLY,
 				(char *)"opaque notifier object"},
     {NULL}  /* Sentinel */
 };

 PySequenceMethods inotify_Wsequence = {
 		(lenfunc)Watcher_len,			/* sq_length */
 		0,								/* sq_concat */
 		0,								/* sq_repeat */
 		0,								/* sq_item */
 		0,								/* sq_slice */
 		0,								/* sq_ass_item */
 		0,								/* sq_ass_slice */
 		0,								/* sq_contains */
 		0,								/* sq_inplace_concat */
 		0,								/* sq_inplace_repeat */
 };

 const char *watcherName="pollinotify.Watcher";
 const char *watcherDocstr="Watcher for inotify service";


 PyTypeObject inotify_WatcherType = {
 	PyVarObject_HEAD_INIT(NULL,0)
     (char *)watcherName,             		/*tp_name*/
     sizeof(Watcher), 			/*tp_basicsize*/
     0,                         	/*tp_itemsize*/
     (destructor)Watcher_dealloc,		/*tp_dealloc*/
     0,                         			/*tp_print*/
 	0,                         			/*tp_getattr*/
 	0,                         			/*tp_setattr*/
 	0,                         			/*tp_compare*/
 	0,                         			/*tp_repr*/
 	0,                         			/*tp_as_number*/
 	&inotify_Wsequence,                  /*tp_as_sequence*/
 	0,                         			/*tp_as_mapping*/
 	0,                         			/*tp_hash */
 	0,                         			/*tp_call*/
 	0,                         			/*tp_str*/
 	0,                         			/*tp_getattro*/
 	0,                         			/*tp_setattro*/
 	0,                         			/*tp_as_buffer*/
 	Py_TPFLAGS_DEFAULT, 				/*tp_flags*/
 	watcherDocstr,								/* tp_doc */
 	0,   								/* tp_traverse */
 	0,           						/* tp_clear */
 	0,		               				/* tp_richcompare */
 	0,		               				/* tp_weaklistoffset */
 	(getiterfunc)Watcher_getiter,		               				/* tp_iter */
 	0,		               				/* tp_iternext */

 	inotify_Wmethods,             		/* tp_methods */
 	inotify_Wmembers,             		/* tp_members */
 	0,                         			/* tp_getset */
 	0,                         			/* tp_base */
 	0,                         			/* tp_dict */
 	0,                         			/* tp_descr_get */
 	0,                         			/* tp_descr_set */
 	0,                         			/* tp_dictoffset */
 	(initproc)Watcher_init,      		/* tp_init */
 	0,                         			/* tp_alloc */
 	(newfunc)Watcher_new,                 		/* tp_new */
 };

 bool WatcherManager::isReady() { return PyType_Ready(&inotify_WatcherType)>=0; }
 void WatcherManager::inc() { Py_INCREF(&inotify_WatcherType); }
 void WatcherManager::add(PyObject *m,const char *name) {
 	PyModule_AddObject(m,name,(PyObject *)&inotify_WatcherType);
 }
 Watcher * WatcherManager::make() {
 	return (Watcher *)_PyObject_New(&inotify_WatcherType);
 }




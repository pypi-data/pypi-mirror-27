/*
 * fileEvent.cpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#include "fileEvent.hpp"
#include "notifier/notifier.hpp"

PyObject *FileEvent_new(PyTypeObject *type,PyObject *args,PyObject *keywords) {

 	auto self = (FileEvent *)type->tp_alloc(type, 0);
 	if (self==NULL) {
 		PyErr_SetString(PyExc_MemoryError,"Cannot allocate FileEvent object");
 		return NULL;
 	}
 	self->mask=NULL;
 	self->path=NULL;
 	return (PyObject *)self;
 }

void FileEvent_dealloc(FileEvent *self) {
	 Py_XDECREF(self->mask);
	 Py_XDECREF(self->path);
	 auto p=(PyObject *)self;
     p->ob_type->tp_free(p);
 }


// Initialisation


int FileEvent_init(FileEvent *self,PyObject *args,PyObject *keywords) {
	 PyObject *mask=NULL;
	 PyObject *path=NULL;
	 PyObject *tmp;

	 if(!PyArg_ParseTuple(args,"iS",&mask,&path)) {
		 PyErr_SetString(PyExc_ValueError,"Cannot parse arguments");
		 return -1;
	 }

	 tmp=self->mask;
	 Py_XINCREF(mask);
	 self->mask=mask;
	 Py_XDECREF(tmp);

	 tmp=self->path;
	 Py_XINCREF(path);
	 self->path=path;
	 Py_XDECREF(tmp);

	 return 0;
}

int FileEvent_in(FileEvent *self,PyObject *find) {
	try {
		int match=PyLong_AsLong(find);
		if(match==-1 && PyErr_Occurred()) {
			PyErr_SetString(PyExc_ValueError,"Invalid argument");
			return -1;
		}
		int mask=PyLong_AsLong(self->mask);
		return((match&mask)!=0) ? 1 : 0;
	}
	catch(std::exception &e) {
		std::cout << e.what() << std::endl;
		PyErr_SetString(PyExc_RuntimeError,e.what());
		return -1;
	}
}


PyObject *FileEvent_matches(FileEvent *self,PyObject *args) {
	try {

		PyObject *obj=NULL;
		if(!PyArg_ParseTuple(args,"o",obj)) {
			PyErr_SetString(PyExc_ValueError,"Cannot parse arguments");
			return NULL;
		}

		int matched=FileEvent_in(self,obj);
		Py_XDECREF(obj);
		if(matched<0) return NULL;
		else if(matched>0) Py_RETURN_TRUE;
		else Py_RETURN_FALSE;
	}
	catch(std::exception &e) {
		std::cout << e.what() << std::endl;
		PyErr_SetString(PyExc_RuntimeError,e.what());
		return NULL;
	}
}

std::list<std::string> decode(FileEvent *self) {
	int value=PyLong_AsLong((PyObject *)self->mask);
	notify::Mask mask(value);
	auto decoded=mask.decode();
	return decoded;
}



PyObject *string_transformer(std::string in)
{
	return PyUnicode_FromString(in.c_str());
}

PyObject *FileEvent_decode(FileEvent *self) {
	auto decoded=decode(self);
	return listToPy<std::string>(decoded,string_transformer);
}

PyObject *FileEvent_str(FileEvent *self) {
	auto decoded=decode(self);

	std::stringstream out;
	for(auto it=decoded.begin();it!=decoded.end();it++) {
		if(it!=decoded.begin()) out << " ";
		out << *it;
	}
	PyObject *str=PyUnicode_FromString(out.str().c_str());
	if(str==NULL) {
		PyErr_SetString(PyExc_SystemError,"Cannot allocate string value");
		return NULL;
	}
	return str;
}

Py_ssize_t FileEvent_len(FileEvent *self) {
	auto decoded=decode(self);
	return (Py_ssize_t)decoded.size();
}

PyMethodDef FileEvent_methods[] = {
		{"decode",(PyCFunction)FileEvent_decode,METH_NOARGS,"Decode the mask as a list of strings"},
		{"matches",(PyCFunction)FileEvent_matches,METH_VARARGS,"Does event match a particular mask"},
		{NULL}
};

PyMemberDef FileEvent_members[] = {
		{(char *)"mask",T_OBJECT_EX,offsetof(FileEvent,mask),READONLY,(char *)"the inotify mask value"},
		{(char *)"path",T_OBJECT_EX,offsetof(FileEvent,path),READONLY,(char *)"the path of the object causing the event"},
    {NULL}  /* Sentinel */
};

PySequenceMethods FileEvent_sequence = {
		(lenfunc)FileEvent_len,			/* sq_length */
		0,								/* sq_concat */
		0,								/* sq_repeat */
		0,								/* sq_item */
		0,								/* sq_slice */
		0,								/* sq_ass_item */
		0,								/* sq_ass_slice */
		(objobjproc)FileEvent_in,		/* sq_contains */
		0,								/* sq_inplace_concat */
		0,								/* sq_inplace_repeat */
};

static PyTypeObject obj = {
		PyVarObject_HEAD_INIT(NULL,0)
	    "inotify.FileEvent",             	/*tp_name*/
	    sizeof(FileEvent), 					/*tp_basicsize*/
	    0,                         			/*tp_itemsize*/
	    (destructor)FileEvent_dealloc,		/*tp_dealloc*/
	    0,                         			/*tp_print*/
		0,                         			/*tp_getattr*/
		0,                         			/*tp_setattr*/
		0,                         			/*tp_compare*/
		0,                         			/*tp_repr*/
		0,                         			/*tp_as_number*/
		&FileEvent_sequence,                /*tp_as_sequence*/
		0,                         			/*tp_as_mapping*/
		0,                         			/*tp_hash */
		0,                         			/*tp_call*/
		(reprfunc)FileEvent_str,            /*tp_str*/
		0,                         			/*tp_getattro*/
		0,                         			/*tp_setattro*/
		0,                         			/*tp_as_buffer*/
		Py_TPFLAGS_DEFAULT, 				/*tp_flags*/
		"inotify event mask and path",		/* tp_doc */
		0,   								/* tp_traverse */
		0,           						/* tp_clear */
		0,		               				/* tp_richcompare */
		0,		               				/* tp_weaklistoffset */
		0,		               				/* tp_iter */
		0,		               				/* tp_iternext */
		FileEvent_methods,             		/* tp_methods */
		FileEvent_members,             		/* tp_members */
		0,                         			/* tp_getset */
		0,                         			/* tp_base */
		0,                         			/* tp_dict */
		0,                         			/* tp_descr_get */
		0,                         			/* tp_descr_set */
		0,                         			/* tp_dictoffset */
		(initproc)FileEvent_init,      		/* tp_init */
		0,                         			/* tp_alloc */
		FileEvent_new,                 		/* tp_new */
};

bool EventTypeManager::isReady() { return PyType_Ready(&obj) >=0; }
void EventTypeManager::inc() { Py_INCREF(&obj); }
void EventTypeManager::add(PyObject *m,const char *name) {
	PyModule_AddObject(m,name,(PyObject *)&obj);
}
FileEvent * EventTypeManager::make() {
	return (FileEvent *)_PyObject_New(&obj);
}



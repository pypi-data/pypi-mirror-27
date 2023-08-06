/*
 * fileEvent.hpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#ifndef FILEEVENT_HPP_
#define FILEEVENT_HPP_

#include "utils.hpp"

typedef struct {
    PyObject_HEAD
    PyObject *mask;
    PyObject *path;
} FileEvent;



 PyObject *FileEvent_new(PyTypeObject *type,PyObject *args,PyObject *keywords);
 void FileEvent_dealloc(FileEvent *self);
 int FileEvent_init(FileEvent *self,PyObject *args,PyObject *keywords);
 int FileEvent_in(FileEvent *self,PyObject *find);
 PyObject *FileEvent_matches(FileEvent *self,PyObject *args);
 std::list<std::string> decode(FileEvent *self);
 PyObject *FileEvent_decode(FileEvent *self);
 PyObject *FileEvent_str(FileEvent *self);
 Py_ssize_t FileEvent_len(FileEvent *self);

 class EventTypeManager {
 public:
	 EventTypeManager() {};

	 bool isReady();
	 void inc();
	 void add(PyObject *m,const char *name);
	 FileEvent * make();
 };




#endif /* FILEEVENT_HPP_ */

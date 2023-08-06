/*
 * watcher.hpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#ifndef WATCHER_HPP_
#define WATCHER_HPP_

#include "utils.hpp"
#include "notifier/notifier.hpp"

typedef struct {
    PyObject_HEAD
    notify::Notifier *notify;
} Watcher;

 PyObject *Watcher_new(PyTypeObject *type,PyObject *args,PyObject *keywords);
 void Watcher_dealloc(Watcher *self);
 int Watcher_init(Watcher *self,PyObject *args,PyObject *keywords);
 PyObject * Watcher_addPath(Watcher *self,PyObject *args,PyObject *keywords);
 PyObject * Watcher_poll(Watcher *self,PyObject *args,PyObject *keywords);
 PyObject * Watcher_events(Watcher *self,PyObject *args,PyObject *keywords);
 PyObject * Watcher_nPaths(Watcher *self,PyObject *args);
 PyObject * Watcher_nEvents(Watcher *self,PyObject *args);
 Py_ssize_t Watcher_len(Watcher *self);
 PyObject * Watcher_getiter(Watcher *self);

 class WatcherManager {
  public:
 	 WatcherManager() {};

 	 bool isReady();
 	 void inc();
 	 void add(PyObject *m,const char *name);
 	 Watcher * make();
  };

#endif /* WATCHER_HPP_ */

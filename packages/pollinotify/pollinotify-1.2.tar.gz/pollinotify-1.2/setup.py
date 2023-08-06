#!/usr/local/bin/python3.6

'''
Created on 30 Jun 2014

@author: julianporter
'''

from setuptools import setup, Extension
from setuptools.config import read_configuration

configuration=read_configuration('setup.cfg')
metadata=configuration['metadata']

package=metadata['name']
version=metadata['version']

libsrc=['errors.cpp','event.cpp','mask.cpp','notifier.cpp']
src=['notifier/'+x for x in libsrc]
src.extend(['utils.cpp','fileEvent.cpp','watcher.cpp','INotify.cpp'])


majorV,minorV = version.split('.')

module1 = Extension('pollinotify',
                    define_macros = [('MAJOR_VERSION', majorV),
                                     ('MINOR_VERSION', minorV)],
                    language = 'c++',
                    sources = ['src/'+s for s in src])


setup (ext_modules = [module1],
       test_suite = 'tests')

1 Summary
=========

**pollinotify** is a simple extension module that wraps the Linux **inotify** service, providing a way to watch for 
specific kinds of file events happening to specified files or in specified directories.  Its major selling points are
that:

  1 It is *polled*, so instead of having to set up a background thread, or attach a   separate event-watching package, the programmer calls it with an optional timeout, so it reports event that have already occurred, or waits for at most the specified time, or until an event occurs;
  
  2 The polling can wait for specific kinds of event.

As the module depends on the **inotify** service, **it is only available on Linux**.
 

2 Module Structure
==================

2.1 Constants
-------------

A number of constants representing common Linux file system event codes, with friendly names:

=============    ================  =================================================================
Constant Name    Linux Name        Interpretation
=============    ================  =================================================================
Access           IN_ACCESS         Object accessed
Modify           IN_MODIFY         Object modified
Attributes       IN_ATTRIB         Object attributes modified
Open             IN_OPEN		   File opened
CloseWrite       IN_CLOSE_WRITE    File closed after contents changed
CloseOther       IN_CLOSE_NOWRITE  File closed without contents changed
Close            IN_CLOSE          File closed
MoveFrom         IN_MOVED_FROM     Object moved from location
MoveTo           IN_MOVED_TO       Object moved to location
Move             IN_MOVE           Object moved
MoveSelf         IN_MOVE_SELF      Object being monitored is deleted
Create           IN_CREATE         Object created
Delete           IN_DELETE         Object deleted
DeleteSelf       IN_DELETE_SELF    Object being monitored is deleted
Ignored          IN_IGNORED        Ignored
DirEvent         IN_ISDIR          The monitored object to which the event occurred is a directory
AllEvents        IN_ALL_EVENTS	   Any event
=============    ================  =================================================================



2.2 Utility functions
---------------------

*maskAsString(mask)*
	Takes a value equal to one or more of the event constants *or*-ed together
	and returns a readable string representation, consisting of a space-separated
	list of the names of the matching events
	
2.3 *FileEvent* class
---------------------

*FileEvent* represents an event detected by the **inotify** service.  The event information is held
in the attributes:

*self.path*
	The path to the file or directory suffering the event
*self.mask*
	Value representing the event(s) it suffered, represented as an *or*-ed collection of event codes, one for
	each kind of event that was detected
*self.decode()*
	Returns a list of the names of the event types to which the event corresponds
*self.matches(mask)*
	Returns **True** if the argument is the code for one of the event types that the object represents, **False** 
	otherwise
	
	
In addition, if *e* is a *FileEvent* object then

::

	str(e) = maskAsString(e.mask)
	len(e) = len(e.decode())
	x in e = e.matches(x)
	

2.4 *Watcher* class
-------------------

The fundamental class of the module.  It connects to the system **inotify** service and uses it to 
poll for events in one or more specified file system paths.  Polling is based on a timeout,
and so can be non-blocking.  

It has the following methods:
     

*__init__()*			
	No-args constructor
*addPath(path,mode=AllEvents)*
	Adds *path* to the list of directories to be polled for events; polling 
	will collect only events that match the *or*-ed event code mask 
	specified in the optional argument *mode* (defaults to all events)
*poll(timeout=0)*
	Polls for events occurring on the specified paths, returning
	**True** if any occur, **False** otherwise; times out
	after *timeout* milliseconds, in which case it returns **False**
*events(match=AllEvents)*		
	Returns a list of *FileEvent* objects, one for
	each event detected during last polling session
	that matches the specified optional *or*-ed event code mask
*nPaths()*			
	Returns the number of paths currently registered with the Watcher
*nEvents()*			
	Returns the number of events detected in the last polling session


If *w* is a *Watcher* instance then

::

	len(w)  = w.nEvents()
	iter(w) = iter(w.events())
	

3 EXAMPLE
=========

A simple example that polls with a timeout of 1 second and lists those events
corresponding to file creation or modification (including **touch**) in the
user's home directory.

::

    import pollinotify

    n=pollinotify.Watcher()
    n.addPath('~')
    while True:
        got=n.poll(timeout=1000)
        if got:
            events=n.events(match=notify.CloseWrite)
            print('Got{} events'.format(len(events))
            for event in events:
                print('{} : {} : {}'.format(event.path,event.mask,str(event)))
                

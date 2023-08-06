/*
 * Notifier.cpp
 *
 *  Created on: 28 Jun 2014
 *      Author: julianporter
 */

#include "notifier.hpp"


namespace notify {







Notifier::Notifier() : nevents(0), watches(), events() {
	fd=inotify_init1(IN_NONBLOCK);
	if(fd<0) {
		throw NotifyError("Cannot start service",errno);
	}
}




void Notifier::addPath(std::string path,Mask::mask_t mode) {
	auto n=path.length()-1;
	if(n>=0 && path[n]=='/') {
		path.resize(n);
	}
	auto watch=inotify_add_watch(fd,path.c_str(),Mask::value(mode));
	if(watch<0) throw NotifyError("Cannot add path",errno);
	Watch newWatch(watch,mode,path);
	watches[watch]=newWatch;
}

bool Notifier::waitForEvent(unsigned int timeout) {


	struct pollfd pfd = {fd,POLLIN | POLLPRI,0};
	struct pollfd p[]={pfd};
	nevents=poll(p,1,timeout);
	if(p[0].revents & POLLIN) {
		unsigned char buffer[8192];
		unsigned get=8192;
		unsigned size=0;
		while(get>0) {
			auto got=read(fd,buffer+size,get);
			//std::cout << "Got " << got << " Get " << get << " Size " << size << " N " << nevents << " ERRNO " << errno << std::endl;
			//std::cout.flush();

			if(got<0 && errno!=11) {
				throw NotifyError("Problem reading events",errno);
			}
			get-=got;
			size+=got;
			if(got==0 || errno==11) break;
		}
		events.clear();
		unsigned pos=0;
		while(pos<size) {
			//std::cout << "Pos " << pos << " Size " << size << std::endl;
			struct inotify_event* event = (struct inotify_event*) &buffer[pos];
			//std::cout << "WD " << event->wd << " NAME " << std::string(event->name,event->len) << " MASK " << event->mask << std::endl;
			auto watch=watches[event->wd];
			std::stringstream out;
			out << watch.path << "/" << std::string(event->name,event->len);
			Event e(event->mask,out.str());
			events.push_back(e);
			//std::cout << "EVENT " << e << std::endl;
			pos+=sizeof(inotify_event)+event->len;
		}
		return true;
	}
	else return false;
}


} /* namespace inotify */

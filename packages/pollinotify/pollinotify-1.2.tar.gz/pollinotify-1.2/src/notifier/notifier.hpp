/*
 * Notifier.h
 *
 *  Created on: 28 Jun 2014
 *      Author: julianporter
 */

#ifndef NOTIFIER_HPP_
#define NOTIFIER_HPP_

#include "base.hpp"
#include "errors.hpp"
#include "mask.hpp"
#include "event.hpp"
#include "watch.hpp"
#include <sys/inotify.h>
#include <poll.h>


#include <unistd.h>




//#define INOTIFY_EVENT_SIZE (sizeof(struct inotify_event))
//#define INOTIFY_BUFLEN (1024 * (INOTIFY_EVENT_SIZE + 16))


namespace notify {




using watches_t = std::map<Watch::watch_t,Watch>;
using watchset_t = std::list<Watch>;

class Notifier {
private:
	int fd;
	unsigned nevents;
	watches_t watches;
	std::list<Event> events;
public:

	Notifier();
	virtual ~Notifier() { Close(); };

	void addPath(std::string path,Mask::mask_t mode=Mask::mask_t::AllEvents);
	unsigned nPaths() const { return watches.size(); };
	std::list<Event> getEvents() const { return std::list<Event>(events); };
	unsigned nEvents() const { return nevents; };
	bool waitForEvent(unsigned int timeout=0);
	void Close() { close(fd); };

};



} /* namespace inotify */

#endif /* NOTIFIER_HPP_ */

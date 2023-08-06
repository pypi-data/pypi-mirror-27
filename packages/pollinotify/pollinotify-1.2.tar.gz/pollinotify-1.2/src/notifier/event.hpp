/*
 * event.hpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#ifndef EVENT_HPP_
#define EVENT_HPP_

#include "base.hpp"
#include "mask.hpp"

namespace notify {

struct Event {
public:

	Mask mask;
	std::string path;

	Event(uint32_t m,const std::string &p) : mask(m), path(p) {};
	Event(const Mask::mask_t m,const std::string &p) : mask(m), path(p) {};
	Event(const Event &m) : mask(m.mask), path(m.path) {};
	Event() : mask(), path() {};

	bool matches(const Mask::mask_t m) const { return mask.matches(m); };
	bool writtenTo() const { return mask.matches(Mask::mask_t::CloseWrite); };
	uint32_t code() const { return mask.code(); };
};



} /* namespace notify */

std::ostream & operator <<(std::ostream & stream,notify::Event & e);

#endif /* EVENT_HPP_ */

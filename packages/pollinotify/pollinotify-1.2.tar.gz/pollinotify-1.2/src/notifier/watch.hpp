/*
 * watch.hpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#ifndef WATCH_HPP_
#define WATCH_HPP_

#include "base.hpp"
#include "mask.hpp"

namespace notify {

struct Watch {
public:
	using watch_t = uint32_t;

	watch_t id;
	Mask::mask_t mask;
	std::string path;

	Watch(watch_t w,Mask::mask_t m,std::string p) : id(w), mask(m), path(p) {};
	Watch(const Watch &m) : id(m.id), mask(m.mask), path(m.path) {};
	Watch() : id(0), mask(Mask::mask_t::None), path() {};

};

} /* namespace notify */

#endif /* WATCH_HPP_ */

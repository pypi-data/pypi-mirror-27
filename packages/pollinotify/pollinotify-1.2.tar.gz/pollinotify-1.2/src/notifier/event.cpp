/*
 * event.cpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#include "event.hpp"

std::ostream & operator <<(std::ostream & stream,notify::Event & e) {
	auto out=e.mask.decode();
	for(auto it=out.begin();it!=out.end();it++) {
		stream << *it << " ";
	}
	return stream;
}

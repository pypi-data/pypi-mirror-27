/*
 * Mask.cpp
 *
 *  Created on: 29 Jun 2014
 *      Author: julianporter
 */

#include "mask.hpp"

#include <iomanip>

namespace notify {



const std::map<Mask::mask_t,std::string> Mask::names = {
		{mask_t::Access,"Access"},
			{mask_t::Modify,"Modify"},
			{mask_t::Attributes,"Attributes"},
			{mask_t::CloseWrite,"CloseWrite"},
			{mask_t::CloseOther,"CloseOther"},
			{mask_t::Open,"Open"},
			{mask_t::MoveFrom,"MoveFrom"},
			{mask_t::MoveTo,"MoveTo"},
			{mask_t::Create,"Create"},
			{mask_t::Delete,"Delete"},
			{mask_t::DirEvent,"DirEvent"},
			{mask_t::Overflow,"Overflow"},
			{mask_t::Ignored,"Ignored"},
			{mask_t::AllEvents,"AllEvents"}
};


bool Mask::matches(const Mask::mask_t match) const {
	 return (value(match) & value(mask)) != 0;
}


std::list<std::string> Mask::decode() {
	std::list<std::string> out;
	for(auto it=names.begin();it!=names.end();it++) {
		if(matches(it->first)) out.push_back(it->second);
	}
	return out;
}

} /* namespace inotify */

std::ostream & operator <<(std::ostream & stream,const notify::Mask & m) {
	stream << std::hex << std::setfill('0') << std::setw(8) << m.code() << std::setfill(' ') << std::setw(0) << std::dec;
	return stream;
}



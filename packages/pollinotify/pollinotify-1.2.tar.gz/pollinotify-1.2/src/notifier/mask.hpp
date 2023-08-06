/*
 * Mask.h
 *
 *  Created on: 29 Jun 2014
 *      Author: julianporter
 */

#ifndef MASK_HPP_
#define MASK_HPP_

#include "base.hpp"
#include <sys/inotify.h>


namespace notify {



class Mask {
public:
	enum class mask_t : uint32_t {
		Access		= IN_ACCESS,
		Modify		= IN_MODIFY,
		Attributes	= IN_ATTRIB,
		CloseWrite	= IN_CLOSE_WRITE,
		CloseOther 	= IN_CLOSE_NOWRITE,
		Close		= IN_CLOSE,
		Open		= IN_OPEN,
		MoveFrom	= IN_MOVED_FROM,
		MoveTo		= IN_MOVED_TO,
		Move 		= IN_MOVE,
		Create		= IN_CREATE,
		Delete		= IN_DELETE,
		DeleteSelf 	= IN_DELETE_SELF,
		MoveSelf   	= IN_MOVE_SELF,
		DirEvent	= IN_ISDIR,
		AllEvents	= IN_ALL_EVENTS,

		Unmounted	= IN_UNMOUNT,
		Overflow	= IN_Q_OVERFLOW,
		Ignored		= IN_IGNORED,

		None        = 0

	};
	const static std::map<mask_t,std::string> names;
	using maskset_t = std::map<mask_t,std::string>;
	using maskval_t = std::pair<mask_t,std::string>;
private:

	mask_t mask;
public:
	static uint32_t value(const Mask::mask_t m) { return static_cast<uint32_t>(m); }
		Mask() : mask(mask_t::None) {};
		Mask(const mask_t m) : mask(m) {};
		Mask(const uint32_t m) : mask(static_cast<mask_t>(m)) {};
		Mask(const Mask &) = default;
		Mask & operator=(const Mask &) = default;
		virtual ~Mask() = default;

		std::list<std::string> decode();
		bool matches(const mask_t match) const;
		uint32_t code() const { return value(mask); };

	};



} /* namespace inotify */



std::ostream & operator <<(std::ostream & stream,const notify::Mask & m);

#endif /* MASK_HPP_ */

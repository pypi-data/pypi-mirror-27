/*
 * errors.hpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#ifndef ERRORS_HPP_
#define ERRORS_HPP_

#include "base.hpp"
#include <exception>
#include <cerrno>
#include <sstream>

namespace notify {

class NotifyError : public std::exception
{
protected:
	std::string message;
	int error;
public:
	NotifyError(const std::string & msg, int err) : std::exception(), message(msg), error(err) {};
	NotifyError(const std::string & msg) : NotifyError(msg,errno) {};

	virtual ~NotifyError() = default;
	virtual const char * what() const noexcept;
	int errorNumber() const noexcept { return error; };
};


} /* namespace notify */

#endif /* ERRORS_HPP_ */

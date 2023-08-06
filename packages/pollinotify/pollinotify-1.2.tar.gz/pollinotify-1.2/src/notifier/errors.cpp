/*
 * errprs.cpp
 *
 *  Created on: 25 Dec 2017
 *      Author: julianporter
 */

#include "errors.hpp"

namespace notify {

const char * NotifyError::what() const noexcept {
		std::stringstream out;
		out << message << " Error number: " << error;
		return out.str().c_str();
	};

} /* namespace notify */

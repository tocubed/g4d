#include <g4d/log.hpp>

#include <iostream>

namespace g4d
{

std::ostream& getLogger()
{
	return std::cout;
}

}

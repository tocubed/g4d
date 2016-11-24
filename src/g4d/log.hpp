#include <ostream>

namespace g4d
{

#define log()                                                                 \
	g4d::getLogger() << __func__ << "(" << __FILE__ << ":" << __LINE__ << "): "

std::ostream& getLogger();

}

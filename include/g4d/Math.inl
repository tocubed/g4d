#include <glm/mat3x3.hpp>
#include <glm/vec3.hpp>
#include <glm/vec4.hpp>

namespace g4d { namespace math
{

glm::dvec4 cross(const glm::dvec4& a, const glm::dvec4& b, const glm::dvec4& c)
{
	glm::dvec3 x(a.x, b.x, c.x);
	glm::dvec3 y(a.y, b.y, c.y);
	glm::dvec3 z(a.z, b.z, c.z);
	glm::dvec3 w(a.w, b.w, c.w);

	return glm::dvec4( glm::determinant(glm::dmat3(y, z, w)),
	                  -glm::determinant(glm::dmat3(x, z, w)),
	                   glm::determinant(glm::dmat3(x, y, w)),
	                  -glm::determinant(glm::dmat3(x, y, z)));
}

}}

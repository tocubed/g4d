#include <g4d/transform.hpp>

#include <glm/trigonometric.hpp>

namespace g4d
{

const Transform Transform::Identity;

Transform::Transform()
    : linear_map()
    , translation()
{
}

const glm::dmat4& Transform::getLinearMap() const
{
	return linear_map;
}

const glm::dvec4& Transform::getTranslation() const
{
	return translation;
}

glm::dvec4 Transform::transform(const glm::dvec4& vector) const
{
	return (linear_map * vector) + translation;
}

Transform& Transform::combine(const Transform& transform)
{
	translation += linear_map * transform.translation;
	linear_map *= transform.linear_map;

	return *this;
}

Transform& Transform::translate(glm::dvec4 offset)
{
	translation += linear_map * offset;

	return *this;
}

Transform& Transform::translate(double x, double y, double z, double w)
{
	return translate(glm::dvec4(x, y, z, w));
}

Transform& Transform::rotate(double theta, glm::dvec4 u, glm::dvec4 v)
{
	u = glm::normalize(u);
	v = glm::normalize(v - u * glm::dot(u, v));

	glm::dmat4 proj = glm::outerProduct(u, u) + glm::outerProduct(v, v);
	glm::dmat4 wedge = glm::outerProduct(v, u) - glm::outerProduct(u, v);

	linear_map *=
	    glm::dmat4() + (glm::cos(theta) - 1) * proj + sin(theta) * wedge;

	return *this;
}

Transform& Transform::scale(glm::dvec4 factors)
{
	linear_map *= glm::dmat4(factors[0], 0, 0, 0,
	                         0, factors[1], 0, 0,
							 0, 0, factors[2], 0,
							 0, 0, 0, factors[3]);

	return *this;
}

Transform& Transform::scale(double x, double y, double z, double w)
{
	return scale(glm::dvec4(x, y, z, w));
}

}

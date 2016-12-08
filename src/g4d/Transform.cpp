#include <g4d/Transform.hpp>

#include <g4d/Math.hpp>

#include <glm/trigonometric.hpp>

#include <iostream>

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

Transform& Transform::lookAt(const glm::dvec4& eye, const glm::dvec4& center, 
                             const glm::dvec4& up, const glm::dvec4& over)
{
	glm::dvec4 f = glm::normalize(center - eye);
	glm::dvec4 s = glm::normalize(g4d::math::cross(f, up, over));
	glm::dvec4 u = glm::normalize(g4d::math::cross(f, over, s));
	glm::dvec4 o = glm::normalize(g4d::math::cross(f, s, u));

	linear_map *= glm::transpose(glm::dmat4(s, u, o, f));
	translate(-eye);
}

/*
void printTransform(glm::dmat4 linear_map, glm::dvec4 translation)
{
	for(auto i = 0; i < 4; i++)
	{
		for(auto j = 0; j < 4; j++)
		{
			std::cout << linear_map[j][i] << ' ';
		}
		std::cout << '\n';
	}

	for(auto i = 0; i < 4; i++)
		std::cout << translation[i] << ' ';
	std::cout << '\n';
}
*/

Transform& Transform::viewSpace(const glm::dvec4& x, const glm::dvec4& y,
                                const glm::dvec4& negative_z)
{
	glm::dvec4 w = -math::cross(x, y, -negative_z);

	lookAt(glm::dvec4(), w, y, -negative_z);
}

Transform operator*(const Transform& left, const Transform& right)
{
	return Transform(left).combine(right);
}

}

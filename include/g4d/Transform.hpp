#pragma once

#include <glm/mat4x4.hpp>
#include <glm/vec4.hpp>

namespace g4d
{

class Transform
{
public:
	Transform();

	const glm::dmat4& getLinearMap() const;
	const glm::dvec4& getTranslation() const;

	glm::dvec4 transform(const glm::dvec4& vector) const;

	Transform& combine(const Transform& transform);

	Transform& translate(glm::dvec4 offset);
	Transform& translate(double x, double y, double z, double w);

	Transform& rotate(double theta, glm::dvec4 u, glm::dvec4 v);

	Transform& scale(glm::dvec4 factors);
	Transform& scale(double x, double y, double z, double w);

	Transform& lookAt(const glm::dvec4& eye, const glm::dvec4& center, 
	                  const glm::dvec4& up, const glm::dvec4& over);

	static const Transform Identity;

private:
	glm::dmat4 linear_map;
	glm::dvec4 translation;
};

Transform operator*(const Transform& left, const Transform& right);

}

#pragma once

#include <g4d/OpenGL.hpp>
#include <g4d/Shader.hpp>

#include <string>

namespace g4d
{

class ShaderProgram
{
public:
	ShaderProgram();
	~ShaderProgram();

	GLuint getId() const;

	bool link(Shader& vertex, Shader& fragment);
	bool link(Shader& vertex, Shader& geometry, Shader& fragment);
	bool isLinked() const;

	std::string getLog() const;

	void bind();
	void release();

	GLint getUniformLocation(const char* name) const;
	GLint getUniformLocation(const std::string& name) const;

private:
	GLuint program;
};

} // namespace g4d

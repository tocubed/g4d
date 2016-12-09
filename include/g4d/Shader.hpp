#pragma once

#include <g4d/OpenGL.hpp>

#include <string>

namespace g4d
{

class Shader
{
public:
	enum class Type : GLenum
	{
		Vertex   = GL_VERTEX_SHADER,
	   	Fragment = GL_FRAGMENT_SHADER, 
		Geometry = GL_GEOMETRY_SHADER
	};

	explicit Shader(Type type);
	~Shader();

	GLuint getId() const;

	Shader::Type getType() const;

	bool compile(const char *source);
	bool compile(const std::string& source);
	bool isCompiled() const;

	std::string getLog() const;

private:
	Shader::Type type;

	GLuint shader;
};

}

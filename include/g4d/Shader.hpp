#pragma once

#include <g4d/OpenGL.hpp>

#include <string>

namespace g4d
{

class Shader
{
public:
	enum class Type
	{
		Vertex   = 1 << 0,
	   	Fragment = 1 << 1, 
		Geometry = 1 << 2
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

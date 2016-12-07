#include <g4d/Shader.hpp>

namespace g4d
{

Shader::Shader(Shader::Type type)
	: type(type)
{
	switch(type)
	{
		case Type::Vertex:
			shader = glCreateShader(GL_VERTEX_SHADER);
			break;
		case Type::Fragment:
			shader = glCreateShader(GL_FRAGMENT_SHADER);
			break;
		case Type::Geometry:
			shader = glCreateShader(GL_GEOMETRY_SHADER);
			break;
	}
}

Shader::~Shader()
{
	glDeleteShader(shader);
}

GLuint Shader::getId() const
{
	return shader;
}

Shader::Type Shader::getType() const
{
	return type;
}

bool Shader::compile(const char* source)
{
	glShaderSource(shader, 1, &source, nullptr);
	glCompileShader(shader);

	return isCompiled();
}

bool Shader::compile(const std::string& source)
{
	return compile(source.c_str());
}

bool Shader::isCompiled() const
{
	GLint compile_status;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &compile_status);

	return (compile_status == GL_TRUE);
}

std::string Shader::getLog() const
{
	GLint log_size;
	glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &log_size);

	std::string buffer(log_size, '\0');
	glGetShaderInfoLog(shader, log_size, nullptr, &buffer[0]);

	return buffer;
}

}

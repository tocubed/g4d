#include <g4d/ShaderProgram.hpp>

namespace
{

GLuint currently_bound;

}

namespace g4d
{

ShaderProgram::ShaderProgram()
{
	program = glCreateProgram();
}

ShaderProgram::~ShaderProgram()
{
	glDeleteProgram(program);
}

GLuint ShaderProgram::getId() const
{
	return program;
}

bool ShaderProgram::link(Shader& vertex, Shader& fragment)
{
	glAttachShader(program, vertex.getId());
	glAttachShader(program, fragment.getId());

	glLinkProgram(program);

	glDetachShader(program, vertex.getId());
	glDetachShader(program, fragment.getId());

	return isLinked();
}

bool ShaderProgram::link(Shader& vertex, Shader& geometry, Shader& fragment)
{
	glAttachShader(program, vertex.getId());
	glAttachShader(program, geometry.getId());
	glAttachShader(program, fragment.getId());

	glLinkProgram(program);

	glDetachShader(program, vertex.getId());
	glDetachShader(program, geometry.getId());
	glDetachShader(program, fragment.getId());

	return isLinked();
}

bool ShaderProgram::isLinked() const
{
	GLint link_status;
	glGetProgramiv(program, GL_LINK_STATUS, &link_status);

	return (link_status == GL_TRUE);
}

std::string ShaderProgram::getLog() const
{
	GLint log_size;
	glGetProgramiv(program, GL_INFO_LOG_LENGTH, &log_size);

	std::string buffer(log_size, '\0');
	glGetProgramInfoLog(program, log_size, nullptr, &buffer[0]);

	return buffer;
}

void ShaderProgram::bind()
{
	currently_bound = program;

	glUseProgram(program);
}

void ShaderProgram::release()
{
	currently_bound = 0;

	glUseProgram(0);
}

GLint ShaderProgram::getUniformLocation(const char* name) const
{
	return glGetUniformLocation(program, name);
}

GLint ShaderProgram::getUniformLocation(const std::string& name) const
{
	return getUniformLocation(name.c_str());
}

}

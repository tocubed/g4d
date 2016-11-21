#include <glad/glad.h>
#include <g4d/shader.hpp>

#include <fstream>
#include <sstream>

namespace
{

bool readFile(const std::string& filepath, std::string& buffer)
{
	std::ifstream file(filepath.c_str());
	std::stringstream bufferss;

	if (file)
	{
		bufferss << file.rdbuf();

		return true;
	}

	return false;
}

}

namespace g4d
{

Shader::Shader()
{
	program = glCreateProgram();
}

Shader::~Shader()
{
	glDeleteProgram(program);
}

bool Shader::loadFromFile(
	const std::string& vert_filepath, const std::string& geom_filepath,
	const std::string& frag_filepath) 
{

}

} // namespace g4d

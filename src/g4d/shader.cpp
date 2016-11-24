#include <g4d/shader.hpp>

#include <g4d/log.hpp>

#include <glad/glad.h>

#include <fstream>
#include <string>

namespace
{

bool readFile(const std::string& filepath, std::string& buffer)
{
	std::ifstream file(filepath.c_str(), std::ios_base::binary);
	if (file)
	{
		std::size_t size;

		file.seekg(0, std::ios_base::end);
		size = file.tellg();
		file.seekg(0, std::ios_base::beg);

		buffer.resize(size);
		file.read(&buffer[0], size);

		return true;
	}
	else
	{
#ifdef G4D_DEBUG
		log() << "File couldn't be read: " << filepath << "\n";
#endif
		return false;
	}
}

bool checkShaderCompilation(GLuint shader)
{
	GLint compile_status;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &compile_status);

#ifdef G4D_DEBUG
	{
		GLint log_size;
		glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &log_size);

		if (log_size > 1) 
		{
			std::string log;
			log.resize(log_size);

			glGetShaderInfoLog(shader, log_size, nullptr, &log[0]);
			log() << "Shader information: " << log;
		}
	}

	if (compile_status == GL_FALSE)
		log() << "Shader compiled unsuccessfully\n";
#endif

	return compile_status == GL_TRUE;
}

bool checkProgramLinking(GLuint program)
{
	GLint link_status;
	glGetProgramiv(program, GL_LINK_STATUS, &link_status);

#ifdef G4D_DEBUG
	{
		GLint log_size;
		glGetProgramiv(program, GL_INFO_LOG_LENGTH, &log_size);

		if (log_size > 1) 
		{
			std::string log;
			log.resize(log_size);

			glGetProgramInfoLog(program, log_size, nullptr, &log[0]);
			log() << "Program information: " << log;
		}
	}

	if (link_status == GL_FALSE)
		log() << "Program linked unsuccessfully\n";
#endif

	return link_status == GL_TRUE;
}

GLuint makeCompiledShader(const char* source, GLenum type)
{
	GLuint shader = glCreateShader(type);

	glShaderSource(shader, 1, &source, nullptr); 
	glCompileShader(shader);

	if (!checkShaderCompilation(shader)) 
	{
		glDeleteShader(shader);
		return 0;
	}
	
	return shader;
}

GLuint makeLinkedProgram(
    const char* vert_source, const char* geom_source,
    const char* frag_source)
{
	GLuint vert_shader = makeCompiledShader(vert_source, GL_VERTEX_SHADER);
	GLuint geom_shader = makeCompiledShader(geom_source, GL_GEOMETRY_SHADER);
	GLuint frag_shader = makeCompiledShader(frag_source, GL_FRAGMENT_SHADER);

	if (!vert_shader || !geom_shader || !frag_shader) 
	{
		if (vert_shader)
			glDeleteShader(vert_shader);
		if (geom_shader)
			glDeleteShader(geom_shader);
		if (frag_shader)
			glDeleteShader(frag_shader);
		
		return 0;
	}

	GLuint program = glCreateProgram();

	glAttachShader(program, vert_shader);
	glAttachShader(program, geom_shader);
	glAttachShader(program, frag_shader);

	glLinkProgram(program);

	glDetachShader(program, vert_shader);
	glDetachShader(program, geom_shader);
	glDetachShader(program, frag_shader);
	glDeleteShader(vert_shader);
	glDeleteShader(geom_shader);
	glDeleteShader(frag_shader);

	if (!checkProgramLinking(program))
	{
		glDeleteProgram(program);
		return 0;
	}

	return program;
}

}

namespace g4d
{

Shader::Shader() : program()
{
}

Shader::~Shader()
{
	if (program)
		glDeleteProgram(program);
}

bool Shader::loadFromFile(
	const std::string& vert_filepath, const std::string& geom_filepath,
	const std::string& frag_filepath) 
{
	std::string vert_source;
	std::string geom_source;
	std::string frag_source;

	if (!readFile(vert_filepath, vert_source) ||
	    !readFile(geom_filepath, geom_source) ||
	    !readFile(frag_filepath, frag_source))
		return false;

	if (program)
		glDeleteProgram(program);

	program = makeLinkedProgram(
	    vert_source.c_str(), geom_source.c_str(), frag_source.c_str());

	return program;
}

} // namespace g4d

#pragma once

#include <g4d/OpenGL.hpp>

#include <cstddef>

namespace g4d
{

class Buffer
{
public:
	enum class Type : GLenum
	{
		Vertex = GL_ARRAY_BUFFER,
		Index = GL_ELEMENT_ARRAY_BUFFER
	};

	explicit Buffer(Type type);
	~Buffer();

	GLuint getId() const;

	Buffer::Type getType() const;

	void bind();
	void release();

	void allocate(const void* data, std::size_t size); 

private:
	Buffer::Type type;

	GLuint buffer;
};

}

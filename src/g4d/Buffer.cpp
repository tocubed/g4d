#include <g4d/Buffer.hpp>

#include <unordered_map>

namespace g4d
{

namespace
{

std::unordered_map<Buffer::Type, GLuint> currently_bound;

class BufferBinder
{
public:
	BufferBinder(Buffer& buffer)
		: buffer(buffer)
	{
		last_bound = currently_bound[buffer.getType()];

		if(last_bound != buffer.getId())
			buffer.bind();
	}

	~BufferBinder()
	{
		if(last_bound != buffer.getId())
		{
			glBindBuffer(static_cast<GLenum>(buffer.getType()), last_bound);

			currently_bound[buffer.getType()] = last_bound;
		}
	}

private:
	Buffer& buffer;

	GLuint last_bound;
};

}

Buffer::Buffer(Buffer::Type type)
	: type(type)
{
	glGenBuffers(1, &buffer);
}

Buffer::~Buffer()
{
	glDeleteBuffers(1, &buffer);
}

GLuint Buffer::getId() const
{
	return buffer;
}

Buffer::Type Buffer::getType() const
{
	return type;
}

void Buffer::bind()
{
	glBindBuffer(static_cast<GLenum>(type), buffer);

	currently_bound[type] = buffer;
}

void Buffer::release()
{
	glBindBuffer(static_cast<GLenum>(type), 0);

	currently_bound[type] = 0;
}

void Buffer::allocate(const void* data, std::size_t size)
{
	BufferBinder binder(*this);

	// TODO Support more than just STATIC_DRAW
	glBufferData(static_cast<GLenum>(type), size, data, GL_STATIC_DRAW);
}

}

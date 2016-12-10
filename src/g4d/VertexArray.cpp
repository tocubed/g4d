#include <g4d/VertexArray.hpp>

namespace g4d
{

namespace
{

GLuint currently_bound;

class VertexArrayBinder
{
public:
	VertexArrayBinder(VertexArray& vertex_array)
		: vertex_array(vertex_array)
	{
		last_bound = currently_bound;

		if(last_bound != vertex_array.getId())
			vertex_array.bind();
	}

	~VertexArrayBinder()
	{
		if(last_bound != vertex_array.getId())
		{
			glBindVertexArray(last_bound);

			currently_bound = last_bound;
		}
	}

private:
	VertexArray& vertex_array;

	GLuint last_bound;
};

}

VertexArray::VertexArray()
{
	glGenVertexArrays(1, &vertex_array);
}

VertexArray::~VertexArray()
{
	glDeleteVertexArrays(1, &vertex_array);
}

GLuint VertexArray::getId() const
{
	return vertex_array;
}

void VertexArray::bind()
{
	glBindVertexArray(vertex_array);

	currently_bound = vertex_array;
}

void VertexArray::release()
{
	glBindVertexArray(0);

	currently_bound = 0;
}

void VertexArray::enableAttribute(GLuint attribute)
{
	VertexArrayBinder(*this);

	glEnableVertexAttribArray(attribute);
}

void VertexArray::disableAttribute(GLuint attribute)
{
	VertexArrayBinder(*this);

	glDisableVertexAttribArray(attribute);
}

void VertexArray::addAttributeBuffer(Buffer& buffer, const AttributeLayout& layout)
{
	VertexArrayBinder(*this);

	// TODO Use BufferBinder to avoid overwriting the bound buffer state
	buffer.bind();

	if(layout.integral)
		glVertexAttribIPointer(layout.attribute, layout.size, layout.type, 
		                       layout.stride, layout.offset);
	else
		glVertexAttribPointer(layout.attribute, layout.size, layout.type, 
		                      layout.normalized, layout.stride, layout.offset);
}

}

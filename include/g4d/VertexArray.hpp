#pragma once

#include <g4d/Buffer.hpp>

namespace g4d
{

class VertexArray
{
public:
	VertexArray();
	~VertexArray();

	GLuint getId() const;

	void bind();
	void release();

	void enableAttribute(GLuint attribute);
	void disableAttribute(GLuint attribute);

	struct AttributeLayout
	{
		GLuint attribute;
		GLint size;
		GLenum type;
		GLboolean normalized;
		GLsizei stride;
		const GLvoid* offset;
		bool integral;
	};

	void addAttributeBuffer(Buffer& buffer, const AttributeLayout& layout);

private:
	GLuint vertex_array;
};

}

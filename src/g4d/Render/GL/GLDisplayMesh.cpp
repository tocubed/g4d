#include <g4d/Render/GL/GLDisplayMesh.hpp>

namespace g4d { namespace GL
{


void GLDisplayMesh::draw()
{
	glBindVertexArray(vao);

	if(index_data != nullptr)
		glDrawElements(gl_primitive_type, index_count, gl_index_type, nullptr);
	else
		glDrawArrays(gl_primitive_type, 0, vertex_count);
}


namespace
{


GLenum toGLAttributeType(VertexAttributeType type)
{
	switch(type)
	{
	case VertexAttributeType::Float: 
		return GL_FLOAT;
	case VertexAttributeType::Byte: 
		return GL_BYTE;
	case VertexAttributeType::Short:
		return GL_SHORT;
	case VertexAttributeType::Int:
		return GL_INT;
	case VertexAttributeType::UByte: 
		return GL_UNSIGNED_BYTE;
	case VertexAttributeType::UShort:
		return GL_UNSIGNED_SHORT;
	case VertexAttributeType::UInt:
		return GL_UNSIGNED_INT;
	default:
		// this should never happen
		return GL_INVALID_ENUM;
		break;
	}
}

GLenum toGLBool(bool b)
{
	if(b)
		return GL_TRUE;
	else
		return GL_FALSE;
}


}


void GLDisplayMesh::end()
{
	glGenVertexArrays(1, &vao);
	glBindVertexArray(vao);

	if(index_data != nullptr)
	{
		glGenBuffers(1, &index_buffer);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer);

		std::size_t index_type_size;	
		switch(index_type)
		{
		case IndexType::Byte:
			index_type_size = 1;
			break;
		
		case IndexType::Short:
			index_type_size = 2;
			break;
		
		case IndexType::Int:
			index_type_size = 4;
			break;
		}
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_type_size * index_count, 
				index_data, GL_STATIC_DRAW);
	}

	vertex_buffers.resize(vertex_data.size());
	glGenBuffers(vertex_buffers.size(), &vertex_buffers[0]);
	for(std::size_t i = 0; i < vertex_data.size(); i++)
	{
		const GLuint buffer = vertex_buffers[i];
		const VertexData& data = vertex_data[i];

		glBindBuffer(GL_ARRAY_BUFFER, buffer);
		glBufferData(GL_ARRAY_BUFFER, vertex_count * data.layout.getSize(),
				data.pointer, GL_STATIC_DRAW);

		for(const VertexElement* element = data.layout.elementsBegin(); 
				element != data.layout.elementsEnd(); element++)
		{
			glEnableVertexAttribArray((GLuint)element->attribute);
			if(element->integral)
				glVertexAttribIPointer((GLuint)element->attribute, element->count,
						toGLAttributeType(element->type), data.layout.getSize(),
						(const void*)element->offset);
			else
				glVertexAttribPointer((GLuint)element->attribute, element->count,
						toGLAttributeType(element->type), 
						toGLBool(element->normalized), data.layout.getSize(), 
						(const void*)element->offset);
		}
	}

	switch(primitive_type)
	{
	case PrimitiveType::Point:
		gl_primitive_type = GL_POINTS;
		break;

	case PrimitiveType::Line:
		gl_primitive_type = GL_LINES;
		break;

	case PrimitiveType::Triangle:
		gl_primitive_type = GL_TRIANGLES;
		break;

	case PrimitiveType::Tetrahedron:
		gl_primitive_type = GL_LINES_ADJACENCY;
		break;
	}

	switch(index_type)
	{
	case IndexType::Byte:
		gl_index_type = GL_UNSIGNED_BYTE;
		break;
	
	case IndexType::Short:
		gl_index_type = GL_UNSIGNED_SHORT;
		break;
	
	case IndexType::Int:
		gl_index_type = GL_UNSIGNED_INT;
		break;
	}
}


}}

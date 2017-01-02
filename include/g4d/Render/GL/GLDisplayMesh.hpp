#pragma once

#include "../DisplayMesh.hpp"

#include <glad/glad.h>


namespace g4d { namespace GL
{


class GLDisplayMesh : public DisplayMesh
{
public:
	virtual void draw() override;

public:
	virtual void end() override;

private:
	GLuint vao;

	std::vector<GLuint> vertex_buffers;
	GLuint index_buffer;

	GLenum gl_primitive_type;
	GLenum gl_index_type;
};


}}

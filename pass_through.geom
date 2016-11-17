#version 330 core

layout (lines_adjacency) in;
layout (triangle_strip, max_vertices = 4) out;

void main()
{
	gl_Position = gl_in[0].gl_Position;
	EmitVertex();
	gl_Position = gl_in[1].gl_Position;
	EmitVertex();
	gl_Position = gl_in[2].gl_Position;
	EmitVertex();
	gl_Position = gl_in[3].gl_Position;
	EmitVertex();

	return;
}

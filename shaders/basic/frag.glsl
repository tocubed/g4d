#version 330

in Vertex
{
	smooth vec4 color;
} vert_in;

out vec4 color;

void main()
{
	color = vert_in.color;
}

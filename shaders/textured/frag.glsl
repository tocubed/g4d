#version 330

uniform sampler3D hypertexture;

in Vertex
{
	smooth vec3 texcoord;
} vert_in;

out vec4 color;

void main()
{
	color = texture(hypertexture, vert_in.texcoord);
}

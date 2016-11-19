#version 330

/* 4D model-view transformation */
uniform mat4 ModelView; 

/* 4D vertex position */
in vec4 position; 

in vec4 color; 

out Vertex
{
	vec4 color;
} vert_out;


void main()
{
	gl_Position = ModelView * position;
	vert_out.color = color;
}

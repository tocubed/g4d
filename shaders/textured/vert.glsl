#version 330

/* 4D model-view transformation */
uniform mat4 ModelViewLinearMap; 

/* 4D translation after model-view */
uniform vec4 ModelViewTranslation;

/* 4D vertex position */
layout(location = 0) in vec4 position; 

layout(location = 1) in vec4 color; 
layout(location = 2) in vec3 texcoord; 

out Vertex
{
	vec4 color;
	vec3 texcoord;
} vert_out;


void main()
{
	gl_Position = (ModelViewLinearMap * position) + ModelViewTranslation;

	vert_out.color = color;
	vert_out.texcoord = texcoord;
}

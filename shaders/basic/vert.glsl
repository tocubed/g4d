#version 330

/* 4D model-view transformation */
uniform mat4 ModelViewLinearMap; 

/* 4D translation after model-view */
uniform vec4 ModelViewTranslation;

/* 4D vertex position */
layout in vec4 position; 

layout in vec4 color; 

out Vertex
{
	vec4 color;
} vert_out;


void main()
{
	gl_Position = (ModelViewLinearMap * position) + ModelViewTranslation;
	vert_out.color = color;
}

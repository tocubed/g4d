#version 330

/* 4D model-view transformation */
uniform mat4 ModelViewLinearMap; 

/* 4D translation after model-view */
uniform vec4 ModelViewTranslation;

/* 4D vertex position */
in vec4 position; 

in vec3 texcoord; 

out Vertex
{
	vec3 texcoord;
} vert_out;


void main()
{
	gl_Position = (ModelViewLinearMap * position) + ModelViewTranslation;

	vert_out.texcoord = texcoord;
}

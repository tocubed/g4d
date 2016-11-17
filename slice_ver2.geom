#version 330 core

layout (lines_adjacency) in;
layout (triangle_strip, max_vertices = 4) out;

uint mix(uint a, uint b, bool ab)
{
	return ab ? a : b;
}

float intersect_xyz(vec4 a, vec4 b)
{
	return b.w / (b.w - a.w);
}

void main()
{
	float e1 = intersect_xyz(gl_in[0].gl_Position, gl_in[1].gl_Position);
	float e2 = intersect_xyz(gl_in[0].gl_Position, gl_in[2].gl_Position);
	float e3 = intersect_xyz(gl_in[0].gl_Position, gl_in[3].gl_Position);
	float e4 = intersect_xyz(gl_in[1].gl_Position, gl_in[2].gl_Position);
	float e5 = intersect_xyz(gl_in[1].gl_Position, gl_in[3].gl_Position);
	float e6 = intersect_xyz(gl_in[2].gl_Position, gl_in[3].gl_Position);

	if(e1 > 0 && 1 > e1)
	{
		gl_Position = mix(gl_in[0].gl_Position, gl_in[1].gl_Position, e1);
		EmitVertex();
	}
	if(e2 > 0 && 1 > e2)
	{
		gl_Position = mix(gl_in[0].gl_Position, gl_in[2].gl_Position, e2);
		EmitVertex();
	}
	if(e3 > 0 && 1 > e3)
	{
		gl_Position = mix(gl_in[0].gl_Position, gl_in[3].gl_Position, e3);
		EmitVertex();
	}
	if(e4 > 0 && 1 > e4)
	{
		gl_Position = mix(gl_in[1].gl_Position, gl_in[2].gl_Position, e4);
		EmitVertex();
	}
	if(e5 > 0 && 1 > e5)
	{
		gl_Position = mix(gl_in[1].gl_Position, gl_in[3].gl_Position, e5);
		EmitVertex();
	}
	if(e6 > 0 && 1 > e6)
	{
		gl_Position = mix(gl_in[2].gl_Position, gl_in[3].gl_Position, e6);
		EmitVertex();
	}

	return;
}

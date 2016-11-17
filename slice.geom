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
	uint a, b, c, d;

	a = uint(gl_in[0].gl_Position.w < gl_in[1].gl_Position.w);
	b = 1 - a;
	c = uint(gl_in[2].gl_Position.w < gl_in[3].gl_Position.w) + 2;
	d = 5 - c;

	bool ac = gl_in[a].gl_Position.w < gl_in[c].gl_Position.w;
	uint tempa = a; a = mix(a, c, ac); c = mix(c, tempa, ac);

	bool bd = gl_in[b].gl_Position.w < gl_in[d].gl_Position.w;
	uint tempb = b; b = mix(b, d, bd); d = mix(d, tempb, bd);

	bool bc = gl_in[b].gl_Position.w < gl_in[c].gl_Position.w;
	tempb = b; b = mix(b, c, bc); c = mix(c, tempb, bc);

	if(gl_in[a].gl_Position.w < 0 && 0 < gl_in[b].gl_Position.w)
	{
		// Triangle intersection with first vertex

		float e1 = intersect_xyz(gl_in[a].gl_Position, gl_in[b].gl_Position);
		float e2 = intersect_xyz(gl_in[a].gl_Position, gl_in[c].gl_Position);
		float e3 = intersect_xyz(gl_in[a].gl_Position, gl_in[d].gl_Position);

		gl_Position = mix(gl_in[a].gl_Position, gl_in[b].gl_Position, e1);
		EmitVertex();
		gl_Position = mix(gl_in[a].gl_Position, gl_in[c].gl_Position, e2);
		EmitVertex();
		gl_Position = mix(gl_in[a].gl_Position, gl_in[d].gl_Position, e3);
		EmitVertex();

		return;
	}
	if(gl_in[c].gl_Position.w < 0 && 0 < gl_in[d].gl_Position.w)
	{
		// Triangle intersection with last vertex

		float e1 = intersect_xyz(gl_in[a].gl_Position, gl_in[d].gl_Position);
		float e2 = intersect_xyz(gl_in[b].gl_Position, gl_in[d].gl_Position);
		float e3 = intersect_xyz(gl_in[c].gl_Position, gl_in[d].gl_Position);

		gl_Position = mix(gl_in[a].gl_Position, gl_in[d].gl_Position, e1);
		EmitVertex();
		gl_Position = mix(gl_in[b].gl_Position, gl_in[d].gl_Position, e2);
		EmitVertex();
		gl_Position = mix(gl_in[c].gl_Position, gl_in[d].gl_Position, e3);
		EmitVertex();

		return;
	}
	if(gl_in[b].gl_Position.w < 0 && 0 < gl_in[c].gl_Position.w)
	{
		// Quad intersection with middle vertices

		float e1 = intersect_xyz(gl_in[a].gl_Position, gl_in[c].gl_Position);
		float e2 = intersect_xyz(gl_in[a].gl_Position, gl_in[d].gl_Position);
		float e3 = intersect_xyz(gl_in[b].gl_Position, gl_in[c].gl_Position);
		float e4 = intersect_xyz(gl_in[b].gl_Position, gl_in[d].gl_Position);
		
		gl_Position = mix(gl_in[a].gl_Position, gl_in[c].gl_Position, e1);
		EmitVertex();
		gl_Position = mix(gl_in[a].gl_Position, gl_in[d].gl_Position, e2);
		EmitVertex();
		gl_Position = mix(gl_in[b].gl_Position, gl_in[c].gl_Position, e3);
		EmitVertex();
		gl_Position = mix(gl_in[b].gl_Position, gl_in[d].gl_Position, e4);
		EmitVertex();

		return;
	}

	// None or degenerate intersection

	return;
}

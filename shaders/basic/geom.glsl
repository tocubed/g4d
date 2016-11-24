#version 330

/* Tetrahedron in 4D space as 4 vertices */
layout (lines_adjacency) in;

/* Intersection of tetrahedron and XYZ hyperplane transformed to screen space */
layout (triangle_strip, max_vertices = 4) out;

/* Projection from 3D to screen space */
uniform mat4 Projection;

/* Other vertex attributes */
in Vertex
{
	vec4 color;
} vert_in[];

out Vertex
{
	smooth vec4 color;
} vert_out;


/*
   Finds the intersection of the edge (a, b) and the XYZ hyperplane.
   Returns a value `t` such that `mix(a, b, t).w == 0`
*/
float intersectEdge(vec4 a, vec4 b)
{
	return b.w / (b.w - a.w);
}


/*
   Emits a vertex on the XYZ hyperplane if an intersection is found with the edge
   (a, b). Interpolates vertex attributes appropriately.
*/
void emitEdgeIntersection(uint a, uint b)
{
	float t = intersectEdge(gl_in[a].gl_Position, gl_in[b].gl_Position);

	if(0 < t && t < 1)
	{
		gl_Position = mix(gl_in[a].gl_Position, gl_in[b].gl_Position, t);
		gl_Position = Projection * vec4(gl_Position.xyz, 1.0);

		vert_out.color = mix(vert_in[a].color, vert_in[b].color, t);

		EmitVertex();
	}
}


void main()
{
	emitEdgeIntersection(0u, 1u);
	emitEdgeIntersection(0u, 2u);
	emitEdgeIntersection(0u, 3u);
	emitEdgeIntersection(1u, 2u);
	emitEdgeIntersection(1u, 3u);
	emitEdgeIntersection(2u, 3u);
}

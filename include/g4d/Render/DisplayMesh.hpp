#pragma once

#include "VertexLayout.hpp"

#include <cstddef>
#include <vector>


namespace g4d
{


enum class PrimitiveType
{
	Point,
	Line,
	Triangle,
	Tetrahedron
};


// TODO Move this?
enum class IndexType
{
	Byte,
	Short,
	Int
};


class DisplayMesh
{
public:
	virtual void draw() = 0;

public:
	void begin();
	virtual void end() = 0;

	void setVertexCount(std::size_t count);
	void setIndexCount(std::size_t count);
	void setPrimitiveType(PrimitiveType type);

	template <typename Vertex>
	void addVertices(const Vertex* vertices)
	{
		addVertices(vertices, Vertex::vertex_layout);
	}
	void addVertices(const void* vertices, VertexLayout layout);

	void addIndices(const std::uint8_t* indices);
	void addIndices(const std::uint16_t* indices);
	void addIndices(const std::uint32_t* indices);
	void addIndices(const void* indices, IndexType type);

// TODO Change this to private, and provide a protected interface
protected:
	struct VertexData
	{
		const void* pointer;
		VertexLayout layout;
	};

	std::vector<VertexData> vertex_data;
	std::size_t vertex_count;

protected:
	const void* index_data;
	IndexType index_type;
	std::size_t index_count;

	PrimitiveType primitive_type;
};


}

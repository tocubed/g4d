#include <g4d/Render/DisplayMesh.hpp>


namespace g4d
{
	

void DisplayMesh::begin()
{
	vertex_data.clear();
	vertex_count = 0;

	index_data = nullptr;
	index_count = 0;

	primitive_type = PrimitiveType::Tetrahedron;
}

void DisplayMesh::setVertexCount(std::size_t count)
{
	vertex_count = count;
}

void DisplayMesh::setIndexCount(std::size_t count)
{
	index_count = count;
}

void DisplayMesh::setPrimitiveType(PrimitiveType type)
{
	primitive_type = type;
}

void DisplayMesh::addVertices(const void* vertices, VertexLayout layout)
{
	vertex_data.push_back(VertexData{vertices, layout});
}

void DisplayMesh::addIndices(const std::uint8_t* indices)
{
	addIndices(indices, IndexType::Byte);
}

void DisplayMesh::addIndices(const std::uint16_t* indices)
{
	addIndices(indices, IndexType::Short);
}

void DisplayMesh::addIndices(const std::uint32_t* indices)
{
	addIndices(indices, IndexType::Int);
}

void DisplayMesh::addIndices(const void* indices, IndexType type)
{
	index_data = indices;
	index_type = type;
}


}

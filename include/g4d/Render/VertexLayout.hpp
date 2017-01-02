#pragma once

#include <array>
#include <cstddef>


namespace g4d 
{


enum class VertexAttribute
{
	Position,
	Normal,
	Color,
	TexCoord,

	Count
};


enum class VertexAttributeType
{
	Float,
	Byte, 
	Short,
	Int,
	UByte,
	UShort,
	UInt,

	Count
};


struct VertexElement
{
	std::size_t offset;
	VertexAttribute attribute;
	VertexAttributeType type;
	std::uint8_t count;
	bool normalized;
	bool integral;
};


class VertexLayout
{
public:
	VertexLayout();

	VertexLayout& add(VertexElement element);
	VertexLayout& setSize(std::size_t size);

	const VertexElement* elementsBegin() const;
	const VertexElement* elementsEnd() const;

	std::size_t getSize() const;

private:
	std::array<VertexElement, (unsigned int)VertexAttribute::Count> elements;
	std::uint8_t num_elements;
	
	std::size_t size;
};


}

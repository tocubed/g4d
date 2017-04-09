#include <g4d/Render/VertexLayout.hpp>


namespace g4d
{


VertexLayout::VertexLayout()
	: num_elements{}, size{}
{
}

VertexLayout& VertexLayout::add(VertexElement element)
{
	elements[num_elements] = element;
	num_elements++;

	return *this;
}

VertexLayout& VertexLayout::setSize(std::size_t size)
{
	this->size = size;

	return *this;
}

const VertexElement* VertexLayout::elementsBegin() const
{
	return elements.data();
}

const VertexElement* VertexLayout::elementsEnd() const
{
	return elements.data() + num_elements;
}

std::size_t VertexLayout::getSize() const
{
	return size;
}


}

#include <glad/glad.h>

#include <string>

namespace g4d
{

class Shader
{
public:

	Shader();
	~Shader();

	bool loadFromFile(
	    const std::string& vert_filepath, const std::string& geom_filepath,
	    const std::string& frag_filepath);

private:

	GLuint program;
};

} // namespace g4d

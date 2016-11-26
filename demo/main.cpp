#include <g4d/shader.hpp>
#include <g4d/transform.hpp>

#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/trigonometric.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <iostream>

void print(const g4d::Transform& t)
{
	for (unsigned int i = 0; i < 4; i++)
	{
		for (unsigned int j = 0; j < 4; j++)
			std::cout << (int)t.getLinearMap()[j][i] << " ";
		std::cout << std::endl;
	}
	for (unsigned int i = 0; i < 4; i++)
		std::cout << (int)t.getTranslation()[i] << " ";
	std::cout << std::endl;
}

int main()
{
    glfwInit();

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

	GLFWwindow* window =
	    glfwCreateWindow(800, 600, "G4D Demo", nullptr, nullptr);
	glfwMakeContextCurrent(window);

    gladLoadGLLoader((GLADloadproc) glfwGetProcAddress);

	g4d::Shader shader;
	shader.loadFromFile(
	    "../shaders/basic/vert.glsl", "../shaders/basic/geom.glsl",
	    "../shaders/basic/frag.glsl");

	g4d::Transform transform;
	print(transform);
	transform.rotate(
	    glm::radians(90.0), glm::dvec4(0, 0, 1, 0), glm::dvec4(0, 0, 0, 1));
	print(transform);
	transform.rotate(
	    glm::radians(90.0), glm::dvec4(0, 1, 0, 0), glm::dvec4(0, 0, 1, 0));
	print(transform);
	transform.rotate(
	    glm::radians(90.0), glm::dvec4(1, 0, 0, 0), glm::dvec4(0, 1, 0, 0));
	print(transform);
	transform
	    .scale(2, 2, 2, 2)
		.translate(0, 0, 0, 2)
	    .scale(0.5, 0.5, 0.5, 0.5)
	    .translate(-1, -1, -1, 0);
	print(transform);

	glm::dvec4 result = transform.transform(glm::dvec4(1, 0, 0, 0));
	for (unsigned int i = 0; i < 4; i++)
		std::cout << (int)result[i] << " ";
	std::cout << std::endl;

	while (!glfwWindowShouldClose(window))
    {
        glfwPollEvents();

        glClearColor(0.2f, 0.2f, 0.2f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glfwSwapBuffers(window);
    }

    glfwTerminate();

    return 0;
}

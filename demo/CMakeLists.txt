add_executable(demo main.cpp)

# GLFW3 Dependency
find_package(glfw3 3.2 REQUIRED)
target_link_libraries(demo ${GLFW_LIBRARIES})
target_include_directories(demo PRIVATE ${GLFW_INCLUDE_DIRS})

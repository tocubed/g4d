add_executable(demo "main.cpp")

target_link_libraries(demo ${G4D_LIBRARIES})

target_link_libraries(demo ${GLAD_LIBRARIES})
target_include_directories(demo PRIVATE ${GLAD_INCLUDE_DIRS})

target_link_libraries(demo ${GLFW_LIBRARIES})

add_executable(demo "main.cpp")

target_link_libraries(demo PRIVATE ${G4D_LIBRARIES})
target_link_libraries(demo PRIVATE ${GLFW_LIBRARIES})
target_link_libraries(demo PRIVATE ${STB_LIBRARIES})

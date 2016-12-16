set(GLAD_PROFILE "core" CACHE STRING "OpenGL profile")
set(GLAD_API "gl=3.3" CACHE STRING "API type/version pairs, like \"gl=3.2,gles=\", no version means latest")
set(GLAD_GENERATOR "c" CACHE STRING "Language to generate the binding for")
set(GLAD_EXTENSIONS "" CACHE STRING "Path to extensions file or comma separated list of extensions, if missing all extensions are included")
set(GLAD_SPEC "gl" CACHE STRING "Name of the spec")
set(GLAD_NO_LOADER ON CACHE BOOL "No loader")

add_subdirectory(glad)
set(GLAD_LIBRARIES ${GLAD_LIBRARIES} PARENT_SCOPE)
set(GLAD_INCLUDE_DIRS ${GLAD_INCLUDE_DIRS} PARENT_SCOPE)


set(GLM_INCLUDE_DIR "${CMAKE_CURRENT_BINARY_DIR}/glm/include")
add_custom_command(OUTPUT ${GLM_INCLUDE_DIR} 
	COMMAND ${CMAKE_COMMAND} -E copy_directory 
			"${CMAKE_CURRENT_SOURCE_DIR}/glm/glm"
			"${GLM_INCLUDE_DIR}/glm"
	DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/glm/glm"
	COMMENT "Isolate glm include directory from its source tree")
add_custom_target(glm_headers DEPENDS ${GLM_INCLUDE_DIR})

add_library(glm INTERFACE)
add_dependencies(glm glm_headers)
target_include_directories(glm INTERFACE ${GLM_INCLUDE_DIR})

set(GLM_LIBRARIES glm PARENT_SCOPE)

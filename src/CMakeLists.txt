list(APPEND G4D_SOURCES
	"g4d/Shader.cpp"
	"g4d/ShaderProgram.cpp"
	"g4d/Transform.cpp"
	"g4d/Render/DisplayMesh.cpp"
	"g4d/Render/VertexLayout.cpp"
	"g4d/Render/GL/GLDisplayMesh.cpp"
)

add_library(g4d STATIC ${G4D_SOURCES})
target_include_directories(g4d PUBLIC "../include")
target_include_directories(g4d PRIVATE ".")

target_link_libraries(g4d PUBLIC ${GLAD_LIBRARIES})
target_include_directories(g4d PUBLIC ${GLAD_INCLUDE_DIRS})

target_link_libraries(g4d PUBLIC ${GLM_LIBRARIES})

if(G4D_DEBUG)
	target_compile_definitions(g4d PRIVATE G4D_DEBUG=1)
endif()

set(G4D_LIBRARIES g4d PARENT_SCOPE)

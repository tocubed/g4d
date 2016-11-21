list(APPEND G4D_INCLUDE_DIRS
	"../include"
)

list(APPEND G4D_SOURCES
	"g4d/shader.cpp"
)

add_library(g4d STATIC ${G4D_SOURCES})
target_include_directories(g4d PUBLIC ${G4D_INCLUDE_DIRS})

target_link_libraries(g4d ${GLAD_LIBRARIES})
target_include_directories(g4d PRIVATE ${GLAD_INCLUDE_DIRS})

set(G4D_LIBRARIES g4d PARENT_SCOPE)

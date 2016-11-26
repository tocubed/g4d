list(APPEND G4D_SOURCES
	"g4d/log.cpp"
	"g4d/shader.cpp"
	"g4d/transform.cpp"
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

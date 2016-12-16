cmake_minimum_required(VERSION 3.5)
project(g4d LANGUAGES CXX)

option(G4D_DEBUG "Enable logging in the G4D library" ON)

add_subdirectory(deps)
add_subdirectory(src)

get_directory_property(HAS_PARENT PARENT_DIRECTORY)
if(HAS_PARENT)
	set(G4D_LIBRARIES ${G4D_LIBRARIES} PARENT_SCOPE)
endif()

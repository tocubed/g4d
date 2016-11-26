cmake_minimum_required(VERSION 3.5)
project(g4d LANGUAGES CXX)

option(G4D_DEBUG "Enable logging in the G4D library" ON)

add_subdirectory(deps)
add_subdirectory(src)
add_subdirectory(demo)

cmake_minimum_required(VERSION 3.16)
project(eliot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

option(PROFILING "Enable profiling mode" OFF)

set(GENERATED_DIR "generated" CACHE STRING "Generated sources directory")
set(BACKEND_DIR "" CACHE PATH "Path to backend directory")

if(NOT EXISTS "${BACKEND_DIR}" OR NOT EXISTS "${BACKEND_DIR}/CMakeLists.txt")
    message(FATAL_ERROR "BACKEND_DIR not set or invalid (must contain CMakeLists.txt), ${BACKEND_DIR}")
endif()

set(TRAITS_DIR "" CACHE STRING "Directory containing backend traits")

if(NOT EXISTS "${TRAITS_DIR}")
    message(FATAL_ERROR "TRAITS_DIR not set or invalid")
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${GENERATED_DIR}")
    message(FATAL_ERROR "GENERATED_DIR does not exist: ${GENERATED_DIR}")
endif()

find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
    set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
endif()

if(PROFILING)
    add_compile_options(-O1 -g -fno-inline -fno-omit-frame-pointer)
else()
    add_compile_options(-O3)
endif()

add_subdirectory(${BACKEND_DIR} backend_build)

add_subdirectory(${GENERATED_DIR}/static)

target_include_directories(eliot_generated PUBLIC ${TRAITS_DIR})

add_executable(eliot ${GENERATED_DIR}/eliot.cpp)

get_property(BACKEND_TARGETS DIRECTORY ${BACKEND_DIR} PROPERTY BUILDSYSTEM_TARGETS)

foreach(t ${BACKEND_TARGETS})
    target_link_libraries(eliot_generated PUBLIC ${t})
endforeach()

target_link_libraries(eliot PRIVATE eliot_generated)


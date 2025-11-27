cmake_minimum_required(VERSION 3.16)
project(eliot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

option(PROFILING "Enable profiling mode" OFF)

if(PROFILING)
    set(CMAKE_CXX_FLAGS "-O1 -g -fno-inline -fno-omit-frame-pointer")
    add_subdirectory(mocks/profiling)
else()
    set(CMAKE_CXX_FLAGS "-O3")
    add_subdirectory(mocks/mock)
endif()

add_subdirectory(generated)

if(PROFILING)
    target_link_libraries(eliot_generated PUBLIC nf_queue_profiling)
else()
    target_link_libraries(eliot_generated PUBLIC nf_queue_mock)
endif()

add_executable(eliot generated/eliot.cpp)

target_link_libraries(eliot PUBLIC eliot_generated)

if(PROFILING)
    target_link_libraries(eliot PUBLIC nf_queue_profiling)
else()
    target_link_libraries(eliot PUBLIC nf_queue_mock)
endif()

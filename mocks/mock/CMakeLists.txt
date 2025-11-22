cmake_minimum_required(VERSION 3.16)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_library(nf_queue_mock STATIC 
    nf_queue_mock.cpp
    core/nf_core.cpp
    config/config.cpp
)

target_include_directories(nf_queue_mock
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR} 
        ${CMAKE_CURRENT_SOURCE_DIR}/core 
        ${CMAKE_CURRENT_SOURCE_DIR}/config
)

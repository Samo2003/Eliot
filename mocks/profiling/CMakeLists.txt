cmake_minimum_required(VERSION 3.16)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_library(nf_queue_profiling INTERFACE)

target_include_directories(nf_queue_profiling
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}
)

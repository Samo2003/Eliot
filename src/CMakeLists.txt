cmake_minimum_required(VERSION 3.16)
project(nf_queue_code_generator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY build)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY build/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY build/lib)

add_subdirectory(mock/anchor)

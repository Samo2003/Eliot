cmake_minimum_required(VERSION 3.16)
project(eliot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_subdirectory(mock)

add_executable(eliot
    ${CMAKE_SOURCE_DIR}/generated/eliot.cpp
    ${CMAKE_SOURCE_DIR}/generated/Processor.cpp
    ${CMAKE_SOURCE_DIR}/generated/calendar/Calendar.cpp
)

target_include_directories(eliot PRIVATE
    ${CMAKE_SOURCE_DIR}/generated
)

target_link_libraries(eliot PRIVATE nf_queue_mock)

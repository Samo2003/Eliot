cmake_minimum_required(VERSION 3.16)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

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

set_target_properties(nf_queue_mock PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)

add_executable(nf_queue_test ../test.cpp)

target_link_libraries(nf_queue_test PRIVATE nf_queue_mock)

target_include_directories(nf_queue_test PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/core
    ${CMAKE_CURRENT_SOURCE_DIR}/config
)

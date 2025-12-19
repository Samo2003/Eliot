cmake_minimum_required(VERSION 3.16)
project(eliot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

option(PROFILING "Enable profiling mode" OFF)
option(TESTING "Enable testing mode" OFF)

set(GENERATED_DIR "generated" CACHE STRING "Generated sources directory")

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${GENERATED_DIR}")
    message(FATAL_ERROR "GENERATED_DIR does not exist: ${GENERATED_DIR}")
endif()

if(PROFILING)
    set(NFQUEUE_LIB nf_queue_profiling)
    add_compile_options(-O1 -g -fno-inline -fno-omit-frame-pointer)
    add_subdirectory(mocks/profiling)
elseif(TESTING)
    set(NFQUEUE_LIB nf_queue_echo)
    add_compile_options(-O3)
    add_subdirectory(mocks/echo)
else()
    set(NFQUEUE_LIB nf_queue_mock)
    add_compile_options(-O3)
    add_subdirectory(mocks/mock)
endif()

add_subdirectory(${GENERATED_DIR}/static)

target_link_libraries(eliot_generated PUBLIC ${NFQUEUE_LIB})
add_executable(eliot ${GENERATED_DIR}/eliot.cpp)
target_link_libraries(eliot PUBLIC eliot_generated ${NFQUEUE_LIB})

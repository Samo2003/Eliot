cmake_minimum_required(VERSION 3.16)
project(eliot LANGUAGES CXX)

# Enforce C++20 standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Export compile_commands.json 
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Place all build outputs into predictable directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Optional build modes
option(PROFILING "Enable profiling mode" OFF)
option(TESTING "Enable testing mode" OFF)

# Directory containing generated sources
set(GENERATED_DIR "generated" CACHE STRING "Generated sources directory")

# Path to selected backend implementation
set(BACKEND_DIR "" CACHE PATH "Path to backend directory")

# Validate backend directory
if(NOT EXISTS "${BACKEND_DIR}" OR NOT EXISTS "${BACKEND_DIR}/CMakeLists.txt")
    message(FATAL_ERROR "BACKEND_DIR not set or invalid (must contain CMakeLists.txt), ${BACKEND_DIR}")
endif()

# Directory containing backend-specific traits
set(TRAITS_DIR "" CACHE STRING "Directory containing backend traits")

# Validate traits directory
if(NOT EXISTS "${TRAITS_DIR}")
    message(FATAL_ERROR "TRAITS_DIR not set or invalid")
endif()

# Ensure generated sources exist
if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${GENERATED_DIR}")
    message(FATAL_ERROR "GENERATED_DIR does not exist: ${GENERATED_DIR}")
endif()

# Enable ccache if available
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
    set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
endif()

# Build configuration flags
if(TESTING)
    # Disable optimizations for faster build
    add_compile_options(-O0)
elseif(PROFILING)
    # Minimal optimization + debug symbols for profiling tools
    add_compile_options(-O1 -g -fno-inline -fno-omit-frame-pointer)
else()
    # Maximum optimization for production build
    add_compile_options(-O3)
endif()

# Add backend as separate subproject
add_subdirectory(${BACKEND_DIR} backend_build)

# Add generated static library
add_subdirectory(${GENERATED_DIR}/static)

# Expose backend traits to generated code
target_include_directories(eliot_generated PUBLIC ${TRAITS_DIR})

# Define final executable entry point
add_executable(eliot ${GENERATED_DIR}/eliot.cpp)

# Collect all backend targets defined in backend directory
get_property(BACKEND_TARGETS DIRECTORY ${BACKEND_DIR} PROPERTY BUILDSYSTEM_TARGETS)

# Link backend targets into generated library
foreach(t ${BACKEND_TARGETS})
    target_link_libraries(eliot_generated PUBLIC ${t})
endforeach()

# Link generated library into final executable
target_link_libraries(eliot PRIVATE eliot_generated)

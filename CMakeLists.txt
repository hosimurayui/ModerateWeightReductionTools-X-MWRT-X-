cmake_minimum_required(VERSION 3.10)
project(MWRT_CoreEngine VERSION 2.0.0)

# Set C++ standard to modern C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Configure output directories for compiled binary files
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/build)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/build)

# Collect all 10 C++ source files from the cpp directory
set(SOURCES
    cpp/memory_bridge.cpp
    cpp/mesh_analyzer.cpp
    cpp/texture_resizer.cpp
    cpp/anim_compressor.cpp
    cpp/atlas_packer.cpp
    cpp/planar_dissolver.cpp
    cpp/frustum_culler.cpp
    cpp/normal_transfer.cpp
    cpp/vram_refresher.cpp
    cpp/cache_purger.cpp
)

# Define the shared library target (Outputs: mwrt_core.dll / libmwrt_core.so / libmwrt_core.dylib)
add_library(mwrt_core SHARED ${SOURCES})

# Windows specific configurations to match standard DLL exports
if(WIN32)
    set_target_properties(mwrt_core PROPERTIES PREFIX "")
endif()

# Print success confirmation status message during configuration setup
message(STATUS "MWRT Pro: CMake successfully configured. Target binary will output to ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")

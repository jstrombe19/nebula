cmake_minimum_required(VERSION 3.15)

project(nebula VERSION 0.0.1)

# find_package(zyre REQUIRED)

# set(ZYRE_INCLUDE_DIR "/home/jaredstromberg/Development/C++/zyre/include")
set(ZYRE_INCLUDE_DIR "/usr/local/include")
set(ZYRE_LIBRARY_DIR "/usr/local/lib")

include_directories(${ZYRE_INCLUDE_DIR})

link_directories(${ZYRE_LIBRARY_DIR})

add_executable(nebula src/main.cpp)

target_link_libraries(nebula zyre zmq czmq)

target_compile_options(nebula PRIVATE -Wall -Wextra -Werror)

install(TARGETS nebula DESTINATION bin)


# Add optional configuration for debug/release builds
set(CMAKE_BUILD_TYPE Debug)

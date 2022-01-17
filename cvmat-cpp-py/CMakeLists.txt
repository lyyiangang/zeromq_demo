cmake_minimum_required(VERSION 3.5.1)
project(cpp-py)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../cmake")
list(APPEND CMAKE_MODULE_PATH "/home/lyy/331G/code/libzmq/output/x86_linux/lib/cmake/")
set (CMAKE_CXX_STANDARD 14)

find_package(OpenCV REQUIRED PATHS /install_x86/)
set(ZeroMQ_DIR "/home/lyy/331G/code/libzmq/output/x86_linux/lib/cmake/ZeroMQ")
find_package(ZeroMQ)
find_package(Protobuf)

if(NOT ${ZeroMQ_FOUND})
    message("can not found zermmq library")
endif()
#   ZeroMQ_STATIC_LIBRARY, ZeroMQ_LIBRARY
message(${ZeroMQ_INCLUDE_DIR})
message(${ZeroMQ_LIBRARY})
message(${Protobuf_INCLUDE_DIRS})
message(${Protobuf_LIBRARIES})
message(${Protobuf_PROTOC_LIBRARIES})
message(${Protobuf_LITE_LIBRARIES})
message("CMAKE_RUNTIME_OUTPUT_DIRECTORY:${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

include_directories(${ZeroMQ_INCLUDE_DIR} ${OpenCV_INCLUDE_DIRS}  ${Protobuf_INCLUDE_DIR})
include_directories("${PROJECT_SOURCE_DIR}/../cppzmq")
include_directories("${PROJECT_SOURCE_DIR}/")

# build cpp from proto
PROTOBUF_GENERATE_CPP(PROTO_SRC PROTO_HEADER msg.proto)
add_executable(pub "pub.cpp" ${PROTO_HEADER} ${PROTO_SRC})
target_link_libraries(pub  ${Protobuf_LIBRARIES} ${ZeroMQ_LIBRARY} ${OpenCV_LIBS})

# build python script from proto
PROTOBUF_GENERATE_PYTHON(PROTO_PY msg.proto)
add_custom_target(myTarget ALL DEPENDS ${PROTO_PY})
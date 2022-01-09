cmake_minimum_required(VERSION 3.5.1)
project(cpp-py)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../cmake")
set (CMAKE_CXX_STANDARD 14)

find_package(OpenCV REQUIRED PATHS /install_x86/)
find_package(ZMQ)
find_package(Protobuf)

message(${ZMQ_INCLUDE_DIRS})
message(${ZMQ_LIBRARIES})
message(${Protobuf_INCLUDE_DIRS})
message(${Protobuf_LIBRARIES})
message(${Protobuf_PROTOC_LIBRARIES})
message(${Protobuf_LITE_LIBRARIES})
message("CMAKE_RUNTIME_OUTPUT_DIRECTORY:${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

include_directories(${ZMQ_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS}  ${Protobuf_INCLUDE_DIR})
include_directories("${PROJECT_SOURCE_DIR}/../cppzmq")
include_directories("${PROJECT_SOURCE_DIR}/")

# build cpp from proto
PROTOBUF_GENERATE_CPP(PROTO_SRC PROTO_HEADER msg.proto)
add_executable(pub "pub.cpp" ${PROTO_HEADER} ${PROTO_SRC})
target_link_libraries(pub  ${Protobuf_LIBRARIES} ${ZMQ_LIBRARIES} ${OpenCV_LIBS})

# build python script from proto
PROTOBUF_GENERATE_PYTHON(PROTO_PY msg.proto)
add_custom_target(myTarget ALL DEPENDS ${PROTO_PY})
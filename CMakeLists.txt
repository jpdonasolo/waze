cmake_minimum_required(VERSION 3.22.1)
project(waze)

file(GLOB SOURCE "src/*cpp")

add_executable(${PROJECT_NAME} ${SOURCE})

include_directories(includes)

add_subdirectory(external/jsoncpp)
get_target_property(JSON_INC_PATH jsoncpp_lib INTERFACE_INCLUDE_DIRECTORIES)
include_directories(${JSON_INC_PATH})

target_link_libraries(${PROJECT_NAME} jsoncpp_lib)
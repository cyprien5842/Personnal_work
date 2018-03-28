cmake_minimum_required(VERSION 3.1)
project(sampleplugin)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

set(SOURCE_FILES "helloWorld.cpp")

find_package(Maya REQUIRED)

add_library(sampleplugin SHARED ${SOURCE_FILES})
target_link_libraries(sampleplugin PRIVATE Maya::Maya)
target_include_directories(sampleplugin PRIVATE Maya::Maya)
MAYA_PLUGIN(sampleplugin)
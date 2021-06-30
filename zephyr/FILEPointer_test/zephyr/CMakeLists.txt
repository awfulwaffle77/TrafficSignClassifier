cmake_minimum_required(VERSION 3.13.1)
include($ENV{ZEPHYR_BASE}/cmake/app/boilerplate.cmake NO_POLICY_SCOPE)
include_directories("/home/awfulwaffle/repos/tensorflow")
include_directories("/home/awfulwaffle/repos/flatbuffers/include")
project(FILEPointer_test)

FILE(GLOB app_sources ../src/*.c*)
target_sources(app PRIVATE ${app_sources})

cmake_minimum_required(VERSION 3.15)
project(qfold)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(nanobind CONFIG REQUIRED)

# Add include directory for C++ headers
include_directories(cpp/include)

nanobind_add_module(_core cpp/src/_core.cpp)

# Install the module to the package directory
# scikit-build-core will handle placement for both regular and editable installs
install(TARGETS _core LIBRARY DESTINATION qfold)


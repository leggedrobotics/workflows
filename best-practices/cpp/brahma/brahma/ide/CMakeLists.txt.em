cmake_minimum_required( VERSION 3.5 )
project( @(project) )

## Allow duplicate targets
set_property(GLOBAL PROPERTY ALLOW_DUPLICATE_CUSTOM_TARGETS 1)

## Include our project helper utility
include( clion_macros.cmake )

## Setup CMake paths
set(ROS_INSTALLATION_PATH @(ros_path))
set(PYTHON_EXECUTABLE /usr/bin/@(python_executable))
set(CATKIN_DEVEL_OR_INSTALL_PATH @(catkin_devel_or_install_space))
list(APPEND CMAKE_PREFIX_PATH "${CATKIN_DEVEL_OR_INSTALL_PATH}" "${ROS_INSTALLATION_PATH}")

## Find Catkin
find_package(catkin REQUIRED)

## Include messages
if(EXISTS ${CATKIN_DEVEL_OR_INSTALL_PATH}/include)
  include_directories(${CATKIN_DEVEL_OR_INSTALL_PATH}/include)
endif()

## Packages
@[for pkg in packages]add_module(@pkg@)@\n@[end for]

## Account for unused includes
add_unused_includes_target()

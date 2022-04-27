cmake_minimum_required(VERSION 3.1.3)
project(cmake_code_coverage)

# Find depencendies
find_package(catkin REQUIRED)

# Include macros
include(cmake/cmake_code_coverage.cmake)

# Configure catkin package
catkin_package(
    CFG_EXTRAS cmake_code_coverage.cmake
)

install(DIRECTORY cmake
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

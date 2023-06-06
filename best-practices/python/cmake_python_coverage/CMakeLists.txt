cmake_minimum_required(VERSION 3.1.3)
project(cmake_python_coverage)

# Find depencendies
find_package(catkin REQUIRED COMPONENTS
  rospy
)

# Include macros
# include(cmake/cmake_python_coverage.cmake)

# Python setup
catkin_python_setup()

# Configure catkin package
catkin_package(
    CFG_EXTRAS add_pytests.cmake cmake_python_coverage.cmake
)

install(DIRECTORY cmake
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

catkin_install_python(PROGRAMS
  scripts/runner
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

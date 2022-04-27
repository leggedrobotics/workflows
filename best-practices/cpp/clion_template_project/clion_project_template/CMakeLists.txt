cmake_minimum_required( VERSION 3.5 )
project( clion_project_template )

# Include our project helper utility
include(ProjectHelper.cmake)

## Initialize project
project_initialize("$ENV{HOME}/catkin_ws/devel")

## Project configurations (THIS IS OPTIONAL)
# Provide a user-specied version of Eigen, e.g. (https://bitbucket.org/leggedrobotics/eigen)
project_set_user_eigen($ENV{HOME}/git/eigen)

## Project Modules
project_add_module(src/<PACKAGE>)
project_add_module(src/<PACKAGE>)
project_add_module(src/<PACKAGE>)

## THIS STEP IS NECESSARY, DO NOT REMOVE
project_finalize()

# EOF

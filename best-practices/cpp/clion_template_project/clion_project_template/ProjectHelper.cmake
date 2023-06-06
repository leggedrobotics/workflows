macro(project_set_user_eigen EIGEN_PATH)
  set(EIGEN3_INCLUDE_DIR ${EIGEN_PATH})
endmacro()

macro(project_initialize CATKIN_WS_DEVEL_DIR)
  list(APPEND CMAKE_PREFIX_PATH "${CATKIN_WS_DEVEL_DIR}")
  list(APPEND CMAKE_PREFIX_PATH "/opt/ros/$ENV{ROS_DISTRO}")
  include_directories(${CATKIN_WS_DEVEL_DIR}/include)
  find_package(catkin REQUIRED) # Speeds up sourcing
endmacro()

macro(project_add_module MODULE)
  add_subdirectory(${MODULE})
  get_property(curr_hack_includes DIRECTORY ${MODULE} PROPERTY INCLUDE_DIRECTORIES)
  list(APPEND hack_includes ${curr_hack_includes})
endmacro()

macro(project_finalize)
  list(REMOVE_DUPLICATES hack_includes)
  foreach(dir ${hack_includes})
    if((NOT ${dir} MATCHES "^${CMAKE_CURRENT_LIST_DIR}/src") OR (NOT EXISTS ${dir}))
      list(REMOVE_ITEM hack_includes ${dir})
      if(NOT EXISTS ${dir})
        message(WARNING "Directory '${dir}' was included but does not exist. Please fix the corresponding CMakeLists.txt" )
      endif()
    endif()
  endforeach()
  add_library(lib_include_hack ${hack_includes} src/.include_hack.cpp )
endmacro()

# EOF

# Copyright (c) 2012 - 2017, Lars Bilke
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The original version (https://github.com/bilke/cmake-modules/blob/master/CodeCoverage.cmake) was edited by:
# @authors     Gabriel Hottiger
# @affiliation ANYbotics

# Coverage target to collect all coverage targets
if(NOT TARGET run_coverage)
  add_custom_target(run_coverage)
endif(NOT TARGET run_coverage)


macro(ADD_CATCH_COVERAGE)
  ADD_TEST_COVERAGE(
    TEST_TYPE "catch"
    ${ARGN}
  )
endmacro(ADD_CATCH_COVERAGE)


macro(ADD_GTEST_COVERAGE)
  ADD_TEST_COVERAGE(
    TEST_TYPE "gtest"
    ${ARGN}
  )
endmacro(ADD_GTEST_COVERAGE)


macro(ADD_ROSTEST_COVERAGE)
  ADD_TEST_COVERAGE(
    TEST_TYPE "rostest"
    ${ARGN}
  )
endmacro(ADD_ROSTEST_COVERAGE)


macro(ADD_TEST_COVERAGE)

  # Check build type
  if(CMAKE_BUILD_TYPE)
    string(TOUPPER ${CMAKE_BUILD_TYPE} COVERAGE_BUILD_TYPE)
  else(CMAKE_BUILD_TYPE)
    set(COVERAGE_BUILD_TYPE "None")
  endif(CMAKE_BUILD_TYPE)

  ## Argument parsing.
  # Input arguments
  set(options INCLUDE_TEST_SOURCE ALLOW_OPTIMIZED)
  set(oneValueArgs NAME OUTPUT_DIR TEST_TYPE)
  set(multiValueArgs TEST_BUILD_TARGETS TEST_EXECUTION_TARGETS LCOV_ARGS GENHTML_ARGS SOURCE_PATTERN SOURCE_EXCLUDE_PATTERN)
  cmake_parse_arguments(COVERAGE "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Check unparsed args
  if(COVERAGE_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "[cmake_code_coverage::ADD_TEST_COVERAGE] Called with unrecognized arguments (${COVERAGE_UNPARSED_ARGUMENTS})!")
  endif(COVERAGE_UNPARSED_ARGUMENTS)

  # Use project name as default coverage name
  if (NOT COVERAGE_NAME)
    set(COVERAGE_NAME "${PROJECT_NAME}")
  endif(NOT COVERAGE_NAME)

  # Use a folder in the binary dir as default output directory
  if (NOT COVERAGE_OUTPUT_DIR)
    set(COVERAGE_OUTPUT_DIR "${PROJECT_BINARY_DIR}/cmake_code_coverage")
  endif(NOT COVERAGE_OUTPUT_DIR)

  # Check for test targets
  if (NOT COVERAGE_TEST_BUILD_TARGETS)
    if(COVERAGE_TEST_TYPE STREQUAL "gtest" OR COVERAGE_TEST_TYPE STREQUAL "catch")
      set(COVERAGE_TEST_BUILD_TARGETS "test_${PROJECT_NAME}")
    elseif(COVERAGE_TEST_TYPE STREQUAL "rostest")
      set(COVERAGE_TEST_BUILD_TARGETS "test_${PROJECT_NAME}_node")
    else()
      message(FATAL_ERROR "[cmake_code_coverage::ADD_TEST_COVERAGE] No test build targets and test type specified.")
    endif()
  endif(NOT COVERAGE_TEST_BUILD_TARGETS)

  if (NOT COVERAGE_TEST_EXECUTION_TARGETS)
    if(COVERAGE_TEST_TYPE STREQUAL "gtest" OR COVERAGE_TEST_TYPE STREQUAL "catch")
      foreach (COVERAGE_TEST_BUILD_TARGET ${COVERAGE_TEST_BUILD_TARGETS})
        list(APPEND COVERAGE_TEST_EXECUTION_TARGETS "_run_tests_${PROJECT_NAME}_${COVERAGE_TEST_TYPE}_${COVERAGE_TEST_BUILD_TARGET}")
      endforeach(COVERAGE_TEST_BUILD_TARGET)
    elseif(COVERAGE_TEST_TYPE STREQUAL "rostest")
      set(COVERAGE_TEST_EXECUTION_TARGETS "_run_tests_${PROJECT_NAME}_rostest")
    else()
      message(FATAL_ERROR "[cmake_code_coverage::ADD_TEST_COVERAGE] No test execution targets and test type specified.")
    endif()
  endif(NOT COVERAGE_TEST_EXECUTION_TARGETS)

  # Use project source dir as default source pattern
  if (NOT COVERAGE_SOURCE_PATTERN)
    set(COVERAGE_SOURCE_PATTERN "'${PROJECT_SOURCE_DIR}/*'")
  endif(NOT COVERAGE_SOURCE_PATTERN)

  # Per default create an empty excludes list
  if (NOT COVERAGE_SOURCE_EXCLUDE_PATTERN)
    set(COVERAGE_SOURCE_EXCLUDE_PATTERN "")
  endif(NOT COVERAGE_SOURCE_EXCLUDE_PATTERN)

  # Exclude test directories if not otherwise specified.
  if (NOT COVERAGE_INCLUDE_TEST_SOURCE)
    list(APPEND COVERAGE_SOURCE_EXCLUDE_PATTERN "'${PROJECT_SOURCE_DIR}/tests/*'" "'${PROJECT_SOURCE_DIR}/test/*'")
  endif(NOT COVERAGE_INCLUDE_TEST_SOURCE)

  ## Coverage analysis
  if(${COVERAGE_BUILD_TYPE} STREQUAL "DEBUG" OR COVERAGE_ALLOW_OPTIMIZED)
    # Find programs to compute and visualize code coverage
    find_program( GCOV_PATH gcov )
    find_program( LCOV_PATH  NAMES lcov lcov.bat lcov.exe lcov.perl)
    find_program( GENHTML_PATH NAMES genhtml genhtml.perl genhtml.bat )

    if(NOT GCOV_PATH)
      message(FATAL_ERROR "gcov not found! Aborting...")
    endif() # NOT GCOV_PATH

    if(NOT LCOV_PATH)
      message(FATAL_ERROR "lcov not found! Aborting...")
    endif() # NOT LCOV_PATH

    if(NOT GENHTML_PATH)
      message(FATAL_ERROR "genhtml not found! Aborting...")
    endif() # NOT GENHTML_PATH

    # Check compiler version
    if("${CMAKE_CXX_COMPILER_ID}" MATCHES "(Apple)?[Cc]lang")
      if("${CMAKE_CXX_COMPILER_VERSION}" VERSION_LESS 3)
        message(FATAL_ERROR "Clang version must be 3.0.0 or greater! Aborting...")
      endif()
    elseif(NOT CMAKE_COMPILER_IS_GNUCXX)
      message(FATAL_ERROR "Compiler is not GNU gcc! Aborting...")
    endif()

    # Setup compiler flags
    set(COVERAGE_COMPILER_FLAGS "-g --coverage -fprofile-arcs -ftest-coverage"
        CACHE INTERNAL "")

    set(CMAKE_CXX_FLAGS_COVERAGE
        ${COVERAGE_COMPILER_FLAGS}
        CACHE STRING "Flags used by the C++ compiler during coverage builds."
        FORCE )
    set(CMAKE_C_FLAGS_COVERAGE
        ${COVERAGE_COMPILER_FLAGS}
        CACHE STRING "Flags used by the C compiler during coverage builds."
        FORCE )
    set(CMAKE_EXE_LINKER_FLAGS_COVERAGE
        ""
        CACHE STRING "Flags used for linking binaries during coverage builds."
        FORCE )
    set(CMAKE_SHARED_LINKER_FLAGS_COVERAGE
        ""
        CACHE STRING "Flags used by the shared libraries linker during coverage builds."
        FORCE )
    mark_as_advanced(
        CMAKE_CXX_FLAGS_COVERAGE
        CMAKE_C_FLAGS_COVERAGE
        CMAKE_EXE_LINKER_FLAGS_COVERAGE
        CMAKE_SHARED_LINKER_FLAGS_COVERAGE )

    # Set compiler flags
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${COVERAGE_COMPILER_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${COVERAGE_COMPILER_FLAGS}")
    message(STATUS "Appending code coverage compiler flags: ${COVERAGE_COMPILER_FLAGS}")

    # Link against gcov
    if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
      link_libraries(gcov)
    else()
      set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
    endif()

    # Setup target
    if(NOT TARGET ${COVERAGE_NAME}_prepare)
      add_custom_target(${COVERAGE_NAME}_prepare
          # Cleanup lcov, set counters to zero
          COMMAND ${LCOV_PATH} ${COVERAGE_LCOV_ARGS} --gcov-tool ${GCOV_PATH} --directory ${PROJECT_BINARY_DIR} --zerocounters --quiet
          # Create baseline to make sure untouched files show up in the report
          COMMAND ${LCOV_PATH} ${COVERAGE_LCOV_ARGS} --gcov-tool ${GCOV_PATH} --directory ${PROJECT_BINARY_DIR} --base-directory ${PROJECT_SOURCE_DIR} --capture --output-file ${COVERAGE_NAME}.base --initial
          # Working dir is binary dir of project
          WORKING_DIRECTORY ${PROJECT_BINARY_DIR}
          # Inform the user
          COMMENT "Resetting code coverage counters to zero."
      )
    endif()

    # Tests depend on prepare step
    foreach (COVERAGE_TEST_BUILD_TARGET ${COVERAGE_TEST_BUILD_TARGETS})
      if(TARGET ${COVERAGE_TEST_BUILD_TARGET})
        add_dependencies(${COVERAGE_NAME}_prepare ${COVERAGE_TEST_BUILD_TARGET})
      else()
        message(WARNING "[cmake_code_coverage::ADD_TEST_COVERAGE] Test build target ${COVERAGE_TEST_BUILD_TARGET} does not exists. Not adding dependency.")
      endif()
    endforeach(COVERAGE_TEST_BUILD_TARGET)

    foreach (COVERAGE_TEST_EXECUTION_TARGET ${COVERAGE_TEST_EXECUTION_TARGETS})
      if(TARGET ${COVERAGE_TEST_EXECUTION_TARGET})
        add_dependencies(${COVERAGE_TEST_EXECUTION_TARGET} ${COVERAGE_NAME}_prepare)
      else()
        message(WARNING "[cmake_code_coverage::ADD_TEST_COVERAGE] Test execution target ${COVERAGE_TEST_EXECUTION_TARGET} does not exists. Not adding dependency.")
      endif()
    endforeach(COVERAGE_TEST_EXECUTION_TARGET)

    # Create output folder
    set(COVERAGE_OUTPUT_NAMED_DIR "${COVERAGE_OUTPUT_DIR}/${COVERAGE_NAME}")
    if(NOT TARGET ${COVERAGE_NAME}_coverage_folder)
      add_custom_target(${COVERAGE_NAME}_coverage_folder
          COMMAND ${CMAKE_COMMAND} -E make_directory ${COVERAGE_OUTPUT_NAMED_DIR}
      )
    endif()

    # Setup target
    if(NOT TARGET ${COVERAGE_NAME}_coverage)
      add_custom_target(${COVERAGE_NAME}_coverage
          # Capturing lcov counters and generate report
          COMMAND ${LCOV_PATH} ${COVERAGE_LCOV_ARGS} --gcov-tool ${GCOV_PATH} --directory ${PROJECT_BINARY_DIR} --base-directory ${PROJECT_SOURCE_DIR} --capture --output-file ${COVERAGE_NAME}.info
          # Combining info with base line
          COMMAND ${LCOV_PATH} ${COVERAGE_LCOV_ARGS} --gcov-tool ${GCOV_PATH} --add-tracefile ${COVERAGE_NAME}.base --add-tracefile ${COVERAGE_NAME}.info --output-file ${COVERAGE_NAME}.total.all
          # Filter for entries that match the source pattern
          COMMAND ${LCOV_PATH} ${COVERAGE_LCOV_ARGS} --gcov-tool ${GCOV_PATH} --extract ${COVERAGE_NAME}.total.all ${COVERAGE_SOURCE_PATTERN} --output-file ${COVERAGE_NAME}.total.source
          # Remove files matching the source exclude pattern
          COMMAND ${LCOV_PATH} ${COVERAGE_LCOV_ARGS} --gcov-tool ${GCOV_PATH} --remove ${COVERAGE_NAME}.total.source ${COVERAGE_SOURCE_EXCLUDE_PATTERN} --output-file ${COVERAGE_NAME}.total
          # Generate HTML report from cleaned tracefile (if not empty)
          COMMAND [ -s ${COVERAGE_NAME}.total ] && ${GENHTML_PATH} ${COVERAGE_GENHTML_ARGS} --output-directory ${COVERAGE_OUTPUT_NAMED_DIR} ${COVERAGE_NAME}.total || true
          # Remove tracefiles
          COMMAND ${CMAKE_COMMAND} -E remove ${COVERAGE_NAME}.base ${COVERAGE_NAME}.info ${COVERAGE_NAME}.total.all ${COVERAGE_NAME}.total.source ${COVERAGE_NAME}.total
          # Working dir is binary dir of project
          WORKING_DIRECTORY ${PROJECT_BINARY_DIR}
          # Inform the user
          COMMENT "Processing code coverage counters and generating report."
      )

      # Show info where to find the report
      add_custom_command(TARGET ${COVERAGE_NAME}_coverage POST_BUILD
        COMMAND ;
        COMMENT "Open ${COVERAGE_OUTPUT_NAMED_DIR}/index.html in your browser to view the coverage report."
      )
    endif()

    # Run tests before creating report
    add_dependencies(run_coverage ${COVERAGE_NAME}_coverage)
    add_dependencies(${COVERAGE_NAME}_coverage ${COVERAGE_NAME}_coverage_folder)
    foreach (COVERAGE_TEST_EXECUTION_TARGET ${COVERAGE_TEST_EXECUTION_TARGETS})
      if(TARGET ${COVERAGE_TEST_EXECUTION_TARGET})
        add_dependencies(${COVERAGE_NAME}_coverage ${COVERAGE_TEST_EXECUTION_TARGET})
      else()
        message(WARNING "[cmake_code_coverage::ADD_TEST_COVERAGE] Test execution target ${COVERAGE_TEST_EXECUTION_TARGET} does not exists. Not adding dependency.")
      endif()
    endforeach(COVERAGE_TEST_EXECUTION_TARGET)

  else(${COVERAGE_BUILD_TYPE} STREQUAL "DEBUG" OR COVERAGE_ALLOW_OPTIMIZED)
    message(STATUS "Code coverage is not run for optimised (non-Debug) build type ${COVERAGE_BUILD_TYPE}.")
  endif(${COVERAGE_BUILD_TYPE} STREQUAL "DEBUG" OR COVERAGE_ALLOW_OPTIMIZED)

endmacro(ADD_TEST_COVERAGE)

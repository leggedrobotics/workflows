# Code coverage cmake helper for python catkin packages.
# @authors     Gabriel Hottiger
# @affiliation ANYbotics

# Pytest support (can be removed with ROS2)
include(${CMAKE_CURRENT_LIST_DIR}/add_pytests.cmake)

# Dummy target for CI.
if(NOT TARGET run_coverage)
  add_custom_target(run_coverage)
endif(NOT TARGET run_coverage)

# Coverage executable.
set(COVERAGE_EXECUTABLE python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}-coverage)

# Output paths to store coverage information.
set(COVERAGE_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/cmake_python_coverage/${PROJECT_NAME})
set(COVERAGE_DATA_OUTPUT_DIR ${COVERAGE_OUTPUT_DIR}/data)

# Create output directory.
file(MAKE_DIRECTORY ${COVERAGE_DATA_OUTPUT_DIR})

# Flag to check if report should be generated.
set(COVERAGE_REPORT_REQUESTED FALSE)

# Add coverage to a pytest.
macro(ADD_PYTEST_WITH_COVERAGE TEST_PATH PYTHON_MODULE)
  # Define output directories
  set(CACHE_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/cmake_python_coverage/cache)
  set(COVERAGE_CONFIG ${COVERAGE_OUTPUT_DIR}/.coveragerc)

  # Generate pytest coverage config
  string(MD5 DATA_FILE ${TEST_PATH})
  file(WRITE ${COVERAGE_CONFIG} "[run]\ndata_file=${COVERAGE_DATA_OUTPUT_DIR}/${DATA_FILE}")

  # Execute the tests with coverage
  if(PYTEST)
    set(PYTEST_TEMP ${PYTEST})
    set(PYTEST "${COVERAGE_EXECUTABLE} run --source=${PYTHON_MODULE} --rcfile=${COVERAGE_CONFIG} ${PYTEST}") # Make sure we execute tests with the right python version
    add_pytests(${TEST_PATH} OPTIONS "-o cache_dir=${CACHE_OUTPUT_DIR}")
    set(PYTEST ${PYTEST_TEMP})

    # Generate report (if not yet requested)
    generate_pytest_coverage_report()
  else()
    message(STATUS "Skipping pytests in project '${PROJECT_NAME}'.")
  endif()
endmacro(ADD_PYTEST_WITH_COVERAGE)

# Add coverage to a pytest rostest.
macro(ADD_ROSTEST_PYTEST_WITH_COVERAGE FILE)
  if(PYTEST)
    # Execute the tests with coverage
    find_package(rostest REQUIRED)
    string(MD5 DATA_FILE ${FILE})
    add_rostest(${FILE} ARGS coverage_file:=${COVERAGE_DATA_OUTPUT_DIR}/${DATA_FILE})

    # Generate report (if not yet requested)
    generate_pytest_coverage_report()
  else()
    message(STATUS "Skipping rostest-pytests in project '${PROJECT_NAME}'.")
  endif()
endmacro(ADD_ROSTEST_PYTEST_WITH_COVERAGE)

# Add coverage generation report command.
macro(GENERATE_PYTEST_COVERAGE_REPORT)
  if(NOT COVERAGE_REPORT_REQUESTED)
    set(COVERAGE_REPORT_REQUESTED TRUE)
    # Generate a HTML coverage report using python-coverage.
    add_custom_command(
      TARGET "_run_tests_${PROJECT_NAME}"
      POST_BUILD
      WORKING_DIRECTORY ${COVERAGE_DATA_OUTPUT_DIR}
      COMMAND ${COVERAGE_EXECUTABLE} combine `ls -d ${COVERAGE_DATA_OUTPUT_DIR}/*`
      COMMAND ${COVERAGE_EXECUTABLE} html -d ${COVERAGE_OUTPUT_DIR}
      COMMENT "Coverage: Combining data files and creating HTML report."
    )
  endif(NOT COVERAGE_REPORT_REQUESTED)
endmacro(GENERATE_PYTEST_COVERAGE_REPORT)

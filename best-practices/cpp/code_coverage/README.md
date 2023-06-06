# cmake_code_coverage

## Generate test coverage report for your project

### Package.xml

Add this package as a test dependency to the `package.xml` file of your project.
``` xml
<test_depend>cmake_code_coverage</test_depend>
```

### CMakeLists.txt

Add the following lines to the `CMakeLists.txt` of your project.

#### GTest

If not otherwise specified it is assumed that the test target name is `test_${PROJECT_NAME}` and the test executable is named `_run_tests_${PROJECT_NAME}_gtest_${TEST_TARGET_NAME}`.
``` cmake
find_package(cmake_code_coverage QUIET)
if(cmake_code_coverage_FOUND)
    add_gtest_coverage()
endif(cmake_code_coverage_FOUND)
```

#### Rostest

If not otherwise specified it is assumed that the test target name is `test_${PROJECT_NAME}_node` and the test executable is named `_run_tests_${PROJECT_NAME}_rostest`.
``` cmake
find_package(cmake_code_coverage QUIET)
if(cmake_code_coverage_FOUND)
    add_rostest_coverage()
endif(cmake_code_coverage_FOUND)
```

#### Important Macro Arguments
* `[TEST_BUILD_TARGETS target1 .. targetN]` Multiple test targets can be combined into a single macro call using the `TEST_BUILD_TARGETS` argument.

* `[NAME name]` Multiple macro calls within a project are combined to a single test report. Use different `NAME` arguments to create separate reports.

### Build Test Report

To create the test coverage report for package `my_package` execute the following command.

``` bash
catkin build --verbose --catkin-make-args run_coverage -- my_package --no-deps --force-cmake -DCMAKE_BUILD_TYPE=Debug
```

By default the report is available at `catkin_ws/build/my_package/cmake_code_coverage/my_package/index.html`.



## Advanced usage

The `add_gtest_coverage` and `add_rostest_coverage` macros wrap around the `add_test_coverage` macro which provides the following arguments.

```
ADD_TEST_COVERAGE([INCLUDE_TEST_SOURCE]
                  [NAME name]
                  [OUTPUT_DIR directory]
                  [TEST_BUILD_TARGETS target1 .. targetN]
                  [TEST_EXECUTION_TARGETS target1 .. targetN]
                  [SOURCE_PATTERN pattern1 .. patternN]
                  [SOURCE_EXCLUDE_PATTERN pattern1 .. patternN]
                  [ALLOW_OPTIMIZED])
```
**INCLUDE_TEST_SOURCE**  Per default the `test` and `tests` folder are excluded from the coverage calculation. Use this flag to enable coverage calculations for the test folders.

**NAME** Prefix used for test report, intermediate targets and temporary files. *Default: ${PROJECT_NAME}*

**TEST_BUILD_TARGETS** CMake targets that build the tests. *Default: NONE*

**TEST_EXECUTION_TARGETS** CMake targets that execute the tests. *Default: NONE*

**OUTPUT_DIR** Output directory of the test coverage report in HTML. *Default: ${PROJECT_BINARY_DIR}/cmake_code_coverage*

**SOURCE_PATTERN** Whitelist pattern that matches the source file paths. *Default: '${PROJECT_SOURCE_DIR}/\*'*

**SOURCE_EXCLUDE_PATTERN** Blacklist pattern to exclude source file paths. *Default: ''*

**ALLOW_OPTIMIZED** Flag that can be set to perform unit coverage analysis on optimized builds (E.g. `-O2, -O3`).

### Example for pattern usage

``` cmake

find_package(cmake_code_coverage QUIET)
if(cmake_code_coverage_FOUND)
    add_test_coverage(
        SOURCE_PATTERN '${PROJECT_SOURCE_DIR}/include/*' '${PROJECT_SOURCE_DIR}/src/*'
        SOURCE_EXCLUDE_PATTERN '${PROJECT_SOURCE_DIR}/src/exclude/*' '*.tpp'
    )
endif(cmake_code_coverage_FOUND)

```

This example will generate a test coverage report for the `include` and `src` folder of the current source directory.
However, the `src/exclude` folder will be excluded. Also all `.tpp` files are ignored.

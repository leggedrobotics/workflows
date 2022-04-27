# cmake_python_coverage

NOTE: Copy-pasted some content from https://github.com/machinekoder/ros_pytest.

## Generate test coverage report for your project

### Package.xml

Add this package as a test dependency to the `package.xml` file of your python catkin package.
``` xml
<test_depend>cmake_python_coverage</test_depend>
```

### CMakeLists.txt

Add the following lines to the `CMakeLists.txt` of your project. If you add multiple tests the coverage will be automatically combined by the `cmake_python_coverage` tool.

#### PyTest

To run the pytest file `test/my_test.py` for the `my_python_module` python module add the following lines. This runs the test file with pytest and generates a coverage report.

``` cmake
if(CATKIN_ENABLE_TESTING)
  find_package(cmake_python_coverage REQUIRED)
  add_pytest_with_coverage(test/my_test.py my_python_module)
endif()
```

#### Rostest

To run the pytest file `test/my_rostest.py` for the `my_python_module` python module follow the following structure in your `.test` file (e.g. `test/my_rostest.test`). The `coverage_file` argument is set by `cmake_python_coverage` to set the coverage output directory to the current binary directory.

```xml
<launch>
  <arg name="coverage_file" default=".coverage"/>
  <test test-name="action" pkg="cmake_python_coverage" type="runner" args="--test=$(find my_package)/test/my_rostest.py --module=my_python_module --coverage_file=$(arg coverage_file)"/>
</launch>
```

To enable the rostest file `test/my_rostest.test` add the following lines.

``` cmake
if(CATKIN_ENABLE_TESTING)
  find_package(cmake_python_coverage REQUIRED)
  add_rostest_pytest_with_coverage(test/action.test)
endif()
```



## Run the tests

To run the tests with coverage enabled run:

```bash
catkin run_tests my_package
```

To check the coverage results open `catkin_ws/build/my_package/cmake_python_coverage/my_package/index.html` in the web browser of your choosing.

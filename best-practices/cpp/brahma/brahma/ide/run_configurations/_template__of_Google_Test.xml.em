<component name="ProjectRunConfigurationManager">
  <configuration default="true" type="CMakeGoogleTestRunConfigurationType" factoryName="Google Test" REDIRECT_INPUT="false"
                 PASS_PARENT_ENVS_2="true" PROJECT_NAME="" TARGET_NAME="" CONFIG_NAME="Debug" RUN_TARGET_PROJECT_NAME=""
                 RUN_TARGET_NAME="" TEST_MODE="SUITE_TEST">
    <envs>
      <env name="CMAKE_PREFIX_PATH" value="$PROJECT_DIR$/.clion/cmake-build-debug/devel:@(ros_path)" />
      <env name="LD_LIBRARY_PATH" value="$PROJECT_DIR$/.clion/cmake-build-debug/devel/lib:@(ros_path)/lib" />
      <env name="PKG_CONFIG_PATH" value="$PROJECT_DIR$/.clion/cmake-build-debug/devel/lib/pkgconfig:@(ros_path)/lib/pkgconfig" />
      <env name="PYTHONPATH" value="@(ros_path)/lib/@(python_executable)/dist-packages" />
      <env name="ROS_PACKAGE_PATH" value="$PROJECT_DIR$/.clion/cmake-build-debug/devel/share:@(ros_path)/share" />
      <env name="ROSLISP_PACKAGE_DIRECTORIES" value="$PROJECT_DIR$/.clion/cmake-build-debug/devel/share/common-lisp" />
    </envs>
    <method v="2">
      <option name="com.jetbrains.cidr.execution.CidrBuildBeforeRunTaskProvider$BuildBeforeRunTask" enabled="true"/>
      <option name="BeforeTestRunTask" enabled="true"/>
    </method>
  </configuration>
</component>

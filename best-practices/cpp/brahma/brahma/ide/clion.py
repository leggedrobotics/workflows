#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import os
import shutil
import sys

from catkin_pkg.topological_order import topological_order

import brahma.utils as utils


def setupCLionProject(git_dir, ide_dir, project, packages, catkin_ws):
    """
    Create a CMakeLists.txt for the CLion project from a template. Setup helper scripts and include hack for CLion.

    :param git_dir: Git directory in which packages are located
    :type git_dir: str
    :param ide_dir: Directory in which CLion project files should be generated
    :type ide_dir: str
    :param project: Name of the CLion project
    :type project: str
    :param packages: Dict of packages to include in the project
    :type packages: dict(str,catkin_pkg.Package)
    :param catkin_ws: Catkin workspace handle.
    :type catkin_ws: CatkinWorkspace
    """
    script_path = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    run_configs_internal_path = os.path.join(script_path, "run_configurations")
    project_settings_path = os.path.join(ide_dir, ".idea")
    code_style_path = os.path.join(project_settings_path, "codeStyles")
    clion_path = os.path.join(ide_dir, ".clion")
    run_configurations_path = os.path.join(project_settings_path, "runConfigurations")

    # Create directories
    utils.createDirectory(code_style_path, True)
    utils.createDirectory(clion_path, True)
    utils.createDirectory(run_configurations_path, True)

    # Copy code style settings
    code_style_config_src = os.path.join(script_path, "codeStyleConfig.xml")
    code_style_config_dest = os.path.join(code_style_path, 'codeStyleConfig.xml')
    shutil.copyfile(code_style_config_src, code_style_config_dest)
    project_setting_src = os.path.join(script_path, "Project.xml")
    project_setting_dest = os.path.join(code_style_path, 'Project.xml')
    shutil.copyfile(project_setting_src, project_setting_dest)

    # Set project root
    misc_setting_src = os.path.join(script_path, "misc.xml")
    misc_setting_dest = os.path.join(project_settings_path, 'misc.xml')
    shutil.copyfile(misc_setting_src, misc_setting_dest)

    # Add the header library
    header_library = os.path.join(clion_path, ".enable_include_folders.cpp")
    open(header_library, 'w+')

    # Copy project helper
    project_helper_src = os.path.join(script_path, "clion_macros.cmake")
    project_helper_dest = os.path.join(clion_path, "clion_macros.cmake")
    shutil.copyfile(project_helper_src, project_helper_dest)

    # Create CMakeLists
    package_paths = [os.path.relpath(os.path.dirname(
        package[1].filename), clion_path) for package in topological_order(git_dir) if package[1].name in packages]
    subs = {"project": project, "packages": package_paths,
            "catkin_devel_or_install_space": catkin_ws.develOrInstallSpace(),
            "ros_path": catkin_ws.extendPath(), "python_executable": getPythonExecutable(catkin_ws)}
    utils.updateFileFromTemplate(os.path.join(script_path, "CMakeLists.txt.em"),
                                 os.path.join(clion_path, "CMakeLists.txt"), subs)

    # Set project name
    utils.updateFileFromTemplate(os.path.join(script_path, "name.em"), os.path.join(project_settings_path, ".name"),
                                 {"project": project})

    # Create run configuration settings
    run_configuration_files = os.listdir(run_configs_internal_path)
    for run_configuration_file in run_configuration_files:
        source_file = os.path.join(run_configs_internal_path, run_configuration_file)
        if source_file.endswith(".em"):
            destination_file = os.path.splitext(os.path.join(run_configurations_path, run_configuration_file))[0]
            utils.updateFileFromTemplate(source_file, destination_file, subs)
        else:
            shutil.copy(source_file, run_configurations_path)


def getPythonExecutable(catkin_ws):
    """
    Create a CMakeLists.txt for the CLion project from a template. Setup helper scripts and include hack for CLion.

    :param catkin_ws: Catkin workspace handle.
    :type catkin_ws: CatkinWorkspace
    :return: Python executable
    :rtype: str
    """
    if "noetic" in catkin_ws.extendPath():
        return "python3"
    else:
        return "python2.7"


def createClangToolsSymlinks(git_dir):
    """
    Create symlinks for .clang-tidy and .clang-format in root directory of IDE project.

    :param git_dir: Git directory in which clang_tools is located
    :type git_dir: str
    :param ide_dir: Directory in which IDE project files should be generated
    :type ide_dir: str
    """
    clang_tools = utils.getPackagePath(git_dir, 'cmake_clang_tools')
    if clang_tools:
        path = os.path.join(git_dir, clang_tools[0])
        utils.updateSymlink(os.path.join(path, ".clang-tidy"), git_dir)
        utils.updateSymlink(os.path.join(path, ".clang-format"), git_dir)

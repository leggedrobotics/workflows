#!/usr/bin/python

# Data:   28.07.2017
# Author: Gabriel Hottiger


import sys
import argparse
import os
import re
import subprocess
from argparse import RawTextHelpFormatter

# Python code to remove duplicate elements
def remove_duplicates(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def create_script(project_path, project_name, catkin_ws_path, package_names, force):
    # Check if it exists already
    project_path = os.path.join(project_path, project_name)
    if not os.path.exists(project_path):
        print 'Creating directory ' + project_path + '.'
        os.makedirs(project_path)
    elif not force:
        print 'Directory ' + project_path + ' already exists. No action taken, aborting... '
        sys.exit()

    # Check if catkin_ws_path was set
    if catkin_ws_path is None:
        catkin_ws_path = subprocess.check_output(["rospack", "find", package_names[0]])
        catkin_ws_path = catkin_ws_path[:catkin_ws_path.rfind('/src/')]
    else:
        catkin_ws_path = os.path.abspath(catkin_ws_path)

    # Store current dir
    init_script_path = os.path.dirname(os.path.realpath(__file__))

    # Write the output file
    os.chdir(project_path)
    if not os.path.isdir('src'):
        os.makedirs('src')

    # Add the empty library hack
    include_hack = open("src/.include_hack.cpp", 'w+')

    # Add project header
    cmakelists = open("CMakeLists.txt", 'w+')
    cmakelists.write("cmake_minimum_required( VERSION 3.5 )\n")
    cmakelists.write("project( " + project_name + " )\n")

    # Allow duplicate targets
    cmakelists.write("\n## Allow duplicate targets\n")
    cmakelists.write("set_property(GLOBAL PROPERTY ALLOW_DUPLICATE_CUSTOM_TARGETS 1)\n")

    # Include the project helper script
    cmakelists.write("\n## Include our project helper utility\n")
    cmakelists.write("include(ProjectHelper.cmake)\n")

    # Add project initialization
    cmakelists.write("\n## Initialize project\n")
    cmakelists.write("project_initialize(" + os.path.join(catkin_ws_path, "devel") + ")\n")

    # Find all dependencies
    dependencies = []
    os.chdir(catkin_ws_path)
    for package_name in package_names:
        bashCommand = "catkin list --unformatted --recursive-dependencies"
        packageDeps = subprocess.check_output(bashCommand.split())
        packageFound = '\n' + package_name + '\n'
        packageDeps = packageDeps.split(packageFound, 1)[1]
        packageDeps = packageDeps.split('build_depend:\n', 1)[1]
        packageDeps = packageDeps.split('run_depend:', 1)[0]
        packageDeps = re.sub('- ', '', packageDeps)
        packageDeps = packageDeps.replace(" ", "")
        packageDeps = packageDeps.replace("build_depend:", "")
        packageDeps = packageDeps.replace("run_depend:", "")
        packageDeps = packageDeps.splitlines()
        dependencies.extend(packageDeps)
        dependencies.append(package_name)
    # Ensure to remove duplicate dependencies
    dependencies = remove_duplicates(dependencies)
    dependencies = [dep for dep in dependencies if dep is not '']
    print(dependencies)

    # Find and add each dependency package to the src/ directory
    cmakelists.write("\n## Packages\n")
    for dependency in dependencies:
        # Get package path
        os.chdir(catkin_ws_path)
        print("dependency = ", dependency)
        locateCommand = "catkin locate " + dependency
        path = subprocess.check_output(locateCommand.split())
        path = path.rstrip('\n')
        os.chdir(path)
        if os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
            repo_folder = os.popen('git rev-parse --show-toplevel').read().rstrip('\n')
            print 'adding package ' + dependency + ' from git repo: ' + repo_folder
        elif os.system('hg root 2> /dev/null > /dev/null') == 0:
            repo_folder = os.popen('hg root').read().rstrip('\n')
            print 'adding package ' + dependency + ' from hg repo: ' + repo_folder
        else:
            print 'Directory is not a repository. No action taken, aborting.. '
            sys.exit()
        # Get relative path for package xml
        path_split = re.split(os.sep, os.path.realpath(path))
        repo_folder_index = path_split.index(os.path.basename(repo_folder))  # Does not work if repos are in a folder with the same name
        relpath = path_split[repo_folder_index]
        for path_entry in path_split[(repo_folder_index + 1):]:
            relpath = os.path.join(relpath, path_entry)
        cmakelists.write("project_add_module( " + os.path.join("src", relpath) + " )\n");
        os.chdir(os.path.join(project_path, 'src'))
        if not os.path.islink(os.path.basename(repo_folder)):
            os.symlink(repo_folder, os.path.basename(repo_folder))

        # If cmake_clang_tools copy configs
        if dependency == "cmake_clang_tools":
            clang_format_file = os.path.join(project_path, "src", relpath, ".clang-format")
            clang_tidy_file = os.path.join(project_path, "src", relpath, ".clang-tidy")
            if os.path.isfile(clang_format_file) and not os.path.isfile(".clang-format"):
                os.symlink(clang_format_file, ".clang-format")
            if os.path.isfile(clang_tidy_file) and not os.path.isfile(".clang-tidy"):
                os.symlink(clang_tidy_file, ".clang-tidy")

    # Project suffix
    cmakelists.write("\n## THIS STEP IS NECESSARY, DO NOT REMOVE\n")
    cmakelists.write("project_finalize()\n")
    cmakelists.write("\n# EOF\n")

    # Symlink the ProjectHelpers.cmake (helper macros) to the new project dir
    if not os.path.isfile(project_path+"/ProjectHelper.cmake"):
        os.symlink(init_script_path+"/clion_project_template/ProjectHelper.cmake", project_path+"/ProjectHelper.cmake")


if __name__ == '__main__':
    # Create parser instance
    parser = argparse.ArgumentParser(description='init_clion.py\n'
                                                 '  Generates a CLion project for the toplevel packages \'package_names\'.\n'
						 '  The project is named \'project_name\' and stored in \'project_path\'.\n'
						 '  The packages have to be located in a catkin workspace at \'catkin_ws_path\'\n\n'
						 'Generated project folder structure:\n'
						 '  - project_name\n'
						 '    - src\n'
						 '      - repo_1 (symlink)\n'
						 '        - package_dependency_1a\n'
						 '        - package_dependency_1b\n'
						 '      - repo_2 (symlink)\n'
						 '        - package_dependency_2\n'
						 '      - .clang-format (symlink, if clang_tools is a dependency)\n'
						 '      - .clang-tidy (symlink, if clang_tools is a dependency)\n'
						 '    - CMakeLists.txt\n'
						 '    - ProjectHelper.cmake (symlink)\n',
						 formatter_class=RawTextHelpFormatter)
    # Define arguments
    parser.add_argument("package_names", nargs="+", help='Toplevel catkin packages to create CLion project for.')
    parser.add_argument("-c", "--project_path", help='Clion project directory path.', default=os.getcwd())
    parser.add_argument("-n", "--project_name", help='Clion project name.')
    parser.add_argument("-w", "--catkin_ws_path", help='Catkin workspace path.')
    parser.add_argument("-f", "--force", help='Force generation even if project already exists.', action='store_true')

    # Retrieve arguments
    args = parser.parse_args()
    # Check arguments
    if args.project_name is None:
        args.project_name = args.package_names[0]
    # Create the CMakeLists.txt for the CLion Project
    create_script(os.path.abspath(args.project_path), args.project_name, args.catkin_ws_path, args.package_names, args.force)

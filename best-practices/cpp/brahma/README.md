# Brahma

**Brahma** is a tool increasing the efficiency to develop catkin software packages. It is intended to be used in an environment where catkin packages are both available as pre-compiled Debian packages, as well as source code version controlled by git. Using the catkin workspace overlay functionality, it makes sure to minimize the amount of packages which are being built, effectively reducing the overall compile time during software development. Functionalities such as including downstream dependencies into the workspace make sure (build-)compatibility issues can be detected efficiently. Also, **brahma** can auto-configure the IDE environment.

## Quick Start

The quick start guide provides instruction on how to install and run the **brahma** workspace management tool. It is recommended to read the *Detailed description* section first to get an overview of the intended use and the underlying assumptions.

### Installation

Navigate to the **brahma** source directory in which the `setup.py` file is located.

To install the **brahma** execute:

```bash
pip3 install . --user
```

The same command can be used to update to a newer version of **brahma**.

The **Brahma** executable is installed in `~/.local/bin`. This directory has to be part of your `$PATH` environment variable in order for **brahma** to be found. To guarantee this add the following line to your `~/.bashrc` file.

```bash
[[ ":$PATH:" != *":/home/$USER/.local/bin:"* ]] && PATH="/home/$USER/.local/bin:${PATH}"
```

If you use **zsh**, changes that need to be done to your `~/.zshrc` are adding the line above and change your `PATH` by uncommenting the line
```bash
export PATH=$HOME/bin:/usr/local/bin:$PATH
```

#### Setup Default Workspace Configurations

First we need to create the default workspace configuration file located at `~/.config/brahma/default.yaml`.
```bash
brahma setup
```

**Brahma** will create this on the first run if you skipped this step. You can override the default configuration or add custom default configurations (e.g. `my_custom.yaml`) to the `~/.config/brahma` folder.


#### Add Bash Completion and Aliases

To enable bash completion create a `~/.bash_completion` file with the following content.

```bash
for bcfile in ~/.local/etc/bash_completion.d/* ; do
  . $bcfile
done
```

This script sources all bash completion files installed in `.local/etc/bash_completion.d`.

Add `source ~/.bash_completion` to your `~/.bashrc` file to make sure auto-complete is enabled.

After restarting your shell auto-completion and the following bash aliases should be available.

* `brahma_source`

  *Usage:* `brahma_source`

  *Example:* `brahma_source`

  *Functionality:* Sources the catkin workspace from anywhere within the brahma workspace.

* `brahma_git`

  *Usage:* `brahma_git $REPO_NAME command`

  *Example:* `brahma_git test_repo status`

  *Functionality:* Executes git commands for a given repository from anywhere within the brahma workspace.

* `brahma_catkin`

  *Usage:* `brahma_catkin command`

  *Example:* `brahma_catkin build --force-cmake`

  *Functionality:* Executes catkin commands from anywhere within the brahma workspace.

When using **zsh**  you need to run the following commands in order to be able to use the bash completion.
```
autoload bashcompinit
bashcompinit
source /path/to/your/bash_completion_file
```

### Usage

#### Creating a Workspace

To create a workspace located at `my_workspace` use:
```bash
brahma create my_workspace
```

By default the repositories listed in `default.yaml` are cloned. You can use custom configurations (e.g `my_custom.yaml`) using the `--config my_custom` option.
Check out the `example.yaml` in the package root for a detailed example.


##### Initializing a Workspace

During creation the workspace is initialized with the given configuration.

If you want to initialize or reset an existing workspace with the default configuration use:

```bash
brahma init my_workspace
```

#### Configuring a Workspace

To alter the default configuration of your workspace navigate into the workspace or one of its subfolders and run:

```bash
brahma config
```

The configuration can also be changed by altering the `settings.yaml` located in the `.brahma` folder in the workspace root.

#### Updating a workspace

The update script creates symbolic links to the relevant packages in your catkin workspace and creates the IDE configuration files. To trigger an update of the workspace navigate into the workspace or one of its subfolders and run:

```bash
brahma update
```

To update the *current branch* and the *base branch* with the latest changes from the remote use the `--pull` option. If you additionally want to merge the *base branch* into *current branch* use the `--pull-and-merge` option.

#### Sourcing a workspace
To source the catkin workspace from anywhere within the **brahma** workspace use:

```bash
brahma_source
```

Note that the workspace has to be built before it can be sourced. To build the catkin workspace from anywhere within the **brahma** workspace use:


```bash
brahma_catkin build
```

#### Cleaning a package
Cleaning single packages is a very useful functionality of *catkin_tools*.
Sadly it only work in combination with a devel space. 
Brahma adds a `brahma clean` command that allows to clean single packages with an install space.

To clean the packages `package_a` and `package_b` use the following command:

```bash
brahma clean --packages package_a package_b
```

### Logging

**Brahma** saves all the relevant information to the log file `brahma.log` stored in the `.brahma` folder in the workspace root.
Per default the console output and the log are identical. Using the `--quiet` option one can reduce the verbosity of the console output.

### Getting help

There is a top-level help available using `brahma --help`.

Every verb implements its own help available using `brahma verb --help`

## Detailed description

### Assumptions
The main assumption that **brahma** is:

> There is an existing catkin workspace that has all packages and corresponding dependencies built/installed. The version of the packages in this *base workspace* corresponds to a git branch (referred to as *base branch*).

The default *base workspace* is `/opt/ros/${ROS_VERSION}` and the *base branch* is the branch from which the installed debian packages were generated (default is nightly).

### Workflow
First you will have to install the *base workspace* from the PPA.

To develop a feature or fix:
1. Create a new brahma workspace.
2. Checkout a new git branch that branches off the *base branch*.
3. Frequently update the workspace using
   * `sudo apt update && sudo apt upgrade` to update the *base workspace*
   * `brahma update --pull-and-merge` to update the **brahma** workspace.


### Workspace management

#### Creation

**Brahma** assists you during the complete development workflow starting with the creation of your workspace. A **brahma** workspace can be created using the `brahma create my_workspace` command and has the following top-level folder structure.

```yaml
 -- my_workspace
    |-- catkin_ws
    |__ source   
```

During the creation of the workspace `git_repositories` present in the current configuration will be cloned into the source folder. The URL property of the `git_repositories` can either be:

* a URL of a remote repository (Brahma will clone the repository. An internet connection is required.),
* a path to a local bare repository (Brahma will clone the repository.), or
* a path to a local pre-cloned repository (Brahma will symlink the repository).

At the end of the creation the workspace is also initialized.

#### Initialization

Similar to the *catkin_tools*, **brahma** workspaces have to be initialized using the `brahma init my_workspace` command. This will run `catkin init` on the catkin workspace. Additionally it will generate the hidden folder `.brahma` in the workspace root. This folder is used to store configuration files of the workspace. Per default, the configuration is generated based on a default workspace configuration located in `~/.config/brahma/default.yaml`. You can create custom workspace configurations in that directory by creating a new yaml file or by modifying the `default.yaml`. Check out `example.yaml` as reference.

Note that once you initialized the workspace you no longer have to provide the workspace path to the **brahma** commands since this can be auto-deduced using the `.brahma` folder (as long as the commands are executed inside the brahma workspace).

#### Configuration

After successful initialization of the workspace you can always change the current configuration of the workspace using the `brahma config` command or by altering the `settings.yaml` located in the `.brahma` folder.

#### Reset

To reset the workspace configuration you can simply re-init the workspace using the `brahma init` command. Also when you move the workspace you have to re-init the workspace to update the `.brahma/paths.yaml` file.

#### Update

The following steps are executed on a workspace update:

* Update git repositories
* Update catkin workspace and clean outdated packages
* Update IDE project files

##### Update Git Repositories
In this step **brahma** makes sure the git repositories in the source folder are up to date.

1. Clone or symlink the repositories that are listed in the configuration but not present in the source folder
2. (optional) Pull repositories

   `brahma update --pull`
3. (optional) Merge *base branch* into *current branch*

    `brahma update --pull-and-merge`

##### Update Catkin Workspace

This step is used to symbolically link all 'relevant' packages into the catkin workspace.

**Resolve packages**

First a set of catkin packages `catkin_packages` is constructed. If the `complete_overlay` option is selected `catkin_packages` is set to all the packages that can be found in the source directory. If we make use of the overlay feature the set of packages is built up using the following procedure.

1. Resolve the `git diff` between the current repository state and the *base branch*
2. (optional: `include_upstream_dependencies`) Add all upstream dependencies of 1.
3. (optional: `include_downstream_dependencies`) Add downstream dependencies of 1.


**Filter packages**

The packages can additionally be filtered for packages that of interest (optional: `filter_packages`).
* For all `filter_packages` the upstream dependencies are collected, the resulting list of packages is used as a whitelist.
* If the `only_filter_downstream_packages` option is enabled then the previous step only applies to the packages deduced in step 3, otherwise all `catkin_packages` are whitelisted.

**Explicit packages**

After the filtering step the explicit packages are appended to list of packages (optional: `explicit_packages`).

**Missing packages**

At this point **brahma** checks whether all upstream dependencies of the remaining packages are installed in `/opt/ros/$ROS_VERSION`. If missing packages are detected and the option `include_missing_dependencies` is enabled in the configuration, those packages are additionally added to the list of packages.

**Symlink packages**

The final list of packages if symlinked into the source folder of the catkin workspace. If the option `complete_overlay` is enabled, then all the packages in the source folder are linked into the catkin workspace.

**Clean outdated packages**

Packages are cleaned in the following scenarios:
* If a package is newly added to the catkin workspace all the built downstream dependencies are cleaned, such that during the next compilation they build against the newly added package.
* If a built package is removed from the catkin workspace the package and all the built downstream dependencies are cleaned, such that during the next compilation they build against the installed package.
* If a package is built, but it is no longer part of the catkin workspace.

##### Update IDE Project Files

The update step of **brahma** also creates IDE configuration scripts. At the moment only the CLion IDE is supported, for which a `CMakeLists.txt` will be generated. The list of packages that is added to the top-level `CMakeLists.txt` as subprojects, are .

Moreover, the `cmake_clang_tools` configuration files are symbolically linked if present.

##### Final Structure

The final workspace has the following structure:
```
_
|-- catkin_ws
|   |-- src
|       |-- package1
|       |-- package2
|       |__ ...
|
|-- source
|   |-- .clion
|   |   |-- CMakeLists.txt
|   |   |__ ...
|   |-- .idea
|   |   |__ ...
|   |-- .clang-format
|   |-- .clang-tidy
|   |-- repo1
|   |-- repo2
|   |-- repo3
|   |__ ...
|__ .brahma       
    |-- paths.yaml
    |__ settings.yaml
```

### Gathering Information About The Workspace

The `brahma info` command can be used to gather information (s.a. paths or source file location) about the **brahma** workspace.

### Known Limitations  
 * Every package can only exist once in all the repositories

   However, as a workaround one can place CATKIN_IGNORE files in duplicated catkin packages.
 * Debian packages must be in-sync with the *base branch*

## Documentation

### Dependencies

Install sphinx with:
```bash
pip3 install sphinx
```

### Generate Documentation
Build the documentation with:
```bash
cd docs
make html
```

Then the documentation is available at `brahma/docs/build/html/brahma.html`.

### Update Documentation

Generate `.rst` files with:
```bash
cd docs
sphinx-apidoc -f -e -o source/ ../brahma/
```

## Testing

### Install Test Dependencies

Install the `testing_infrastructure` python package.

```
pip3 install <repo_path>/infrastructure/testing_infrastructure --user
```
Use the `-e` option to get a editable install. 
Changes to the `testing_infrastrucutre` package will be available without re-installation.


### Run Tests

Execute the `run_tests` executable.

This will run all tests in the `test` directory with pytest.
It will also generate a coverage report located at `test/coverage_report/index.html`.

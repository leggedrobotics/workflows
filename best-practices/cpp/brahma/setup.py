#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'empy',
    'gitpython',
    'catkin_pkg',
    'catkin_tools',
    'termcolor',
    'PyYAML',
]


def get_data_files():
    data_files = []

    # Bash completion
    bash_comp_dest = 'etc/bash_completion.d'
    data_files.append((bash_comp_dest,
                       ['bash/brahma-completion.bash']))
    data_files.append((bash_comp_dest,
                       ['bash/brahma-aliases.bash']))
    return data_files


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="brahma",
    version="1.1.5",
    packages=find_packages(),
    package_data={'brahma': ['ide/*.em', 'ide/*.cmake', 'ide/*.xml', 'ide/run_configurations/*.xml',
                             'ide/run_configurations/*.xml.em']},
    entry_points={
        'console_scripts': [
            'brahma = brahma.main:brahma_main',
        ]},
    author="Gabriel Hottiger",
    author_email="ghottiger@anybotics.com",
    url="",
    keywords=['catkin', 'ROS'],
    classifiers=[
        'Programming Language :: Python',
    ],
    description="Workspace management script for ANYmal Research.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Proprietary',
    data_files=get_data_files(),
    install_requires=install_requires,
    python_requires='>=3.6',
)

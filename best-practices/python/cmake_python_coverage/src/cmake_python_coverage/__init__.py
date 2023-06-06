# coding=utf-8

from argparse import ArgumentParser
from distutils.version import LooseVersion

import os

import coverage
import pytest

import rospy


def get_output_file(argv):
    for arg in argv:
        if arg.startswith('--gtest_output'):
            return arg.split('=xml:')[1]

    raise RuntimeError('No output file has been passed')


def get_additional_args(argv):
    args = []
    for arg in argv[1:]:
        if arg.startswith('__') or arg.startswith('--gtest_output'):
            continue
        args.append(arg)
    return args


def create_cache_dir_args(version, output_file):
    # disable cache for Pytest < 3.2
    if LooseVersion("3.5.0") > LooseVersion(version):
        cache_dir_arg = '-p no:cacheprovider'
    else:
        root_dir = os.path.dirname(output_file)
        cache_dir_arg = '--rootdir={}'.format(root_dir)
    return cache_dir_arg.split(' ')


def run_pytest(argv):
    output_file = get_output_file(argv)
    additional_args = get_additional_args(argv)
    test_module = rospy.get_param('test_module')
    module_path = os.path.realpath(test_module)
    cache_dir_args = create_cache_dir_args(pytest.__version__, output_file)

    return pytest.main(
        [module_path, '--junitxml={}'.format(output_file)]
        + cache_dir_args
        + additional_args
    )


def run_pytest_coverage(argv):
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("--test", type=str, help="Path where the ROS tests are located.", required=True)
    parser.add_argument("--module", type=str, help="Python module to test (mostly equal to the package name)", required=True)
    parser.add_argument("--coverage_file", type=str, help="File to store coverage data.", required=True)

    args, other_args = parser.parse_known_args()

    # Set the test_module parameter used by ros_pytest
    rospy.set_param('test_module', args.test)

    # Run coverage
    cov = coverage.Coverage(source=[args.module], data_file=args.coverage_file)
    # cov.load() # Used to append to existing (Not required)
    cov.start()
    exit_code = run_pytest(other_args)
    cov.stop()
    cov.save()
    return exit_code

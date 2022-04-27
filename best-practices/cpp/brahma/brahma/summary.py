#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

from termcolor import colored
import brahma.log as log


def entry(key, value):
    """
    Prints a key-value pair in an aligned way

    :param key: Key printed on the left side
    :type key: str
    :param value: Value printed on the right side
    :type value: str
    """
    log.logger.info(colored("{:<31}".format(key), 'cyan') + colored("    {}".format(value), 'yellow'))

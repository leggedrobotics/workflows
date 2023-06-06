#!/usr/bin/python3

# Author:       Gabriel Hottiger
# Affiliation:  ANYbotics

import sys
import logging
from logging.handlers import RotatingFileHandler

from termcolor import colored

logger = logging.getLogger("brahma")


def setupLogger(quiet, loggerFilePath, loggerFileName):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = logging.handlers.RotatingFileHandler(
        "{0}/{1}.log".format(loggerFilePath, loggerFileName), maxBytes=1000000, backupCount=5)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    if quiet:
        consoleHandler.setLevel(logging.INFO)
    else:
        consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)


def error(*args):
    """
    Prints and error message and exits the process

    :param `*args`: The message to be printed
    """
    sys.exit(colored("Error: ", 'red', attrs=['bold']) + colored(*args, 'red'))


def warn(*args, **kwargs):
    """
    Prints an warning message

    :param `*args`: The message to be printed
    :param `*kwargs`: Additional arguments for the print function
    """
    logger.warn(colored(*args, 'yellow'), **kwargs)


def status(*status, **kwargs):
    """
    Prints a status message

    :param `*status`: The message to be printed
    :param `*kwargs`: Additional arguments for the print function
    """
    logger.info(colored('--> ', 'green') + colored(*status, 'green'), **kwargs)


def prefixStatus(prefix, *status, **kwargs):
    """
    Prints an information message with a prefix

    :param `prefix`: Prefix of the message
    :param `*status`: The message to be printed
    :param `*kwargs`: Additional arguments for the print function
    """
    logger.info(colored(prefix + ':\n', 'magenta') + colored('--> ', 'blue') + colored(*status, 'blue'), **kwargs)


def info(*args, **kwargs):
    """
    Prints an information message

    :param `*args`: The message to be printed
    :param `*kwargs`: Additional arguments for the print function
    """
    logger.debug(colored(*args, 'magenta'), **kwargs)


def title(*args, **kwargs):
    """
    Prints a title

    :param `*args`: The title to be printed
    :param `*kwargs`: Additional arguments for the print function
    """
    logger.info(colored(*args, 'cyan', attrs=['bold']), **kwargs)


def packages(packages, **kwargs):
    """
    Prints the package list message

    :param `packages`: List of package names
    :param `*args`: The message to be printed
    :param `*kwargs`: Additional arguments for the print function
    """
    logger.debug(colored("[{}]".format(', '.join(sorted(packages, key=lambda x: x.lower()))), 'blue'), **kwargs)

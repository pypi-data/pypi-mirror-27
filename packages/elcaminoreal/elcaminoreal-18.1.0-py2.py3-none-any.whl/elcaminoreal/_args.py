"""
An experiment in a better way to build argument parsers.
"""
import argparse


def argparser(*add_arguments):
    """
    Generate a function that parses arguments.
    """
    ret = argparse.ArgumentParser()
    for (args, kwargs) in add_arguments:
        ret.add_argument(*args, **kwargs)
    return ret.parse_args


def argument(*args, **kwargs):
    """
    Represents an argument
    """
    return args, kwargs

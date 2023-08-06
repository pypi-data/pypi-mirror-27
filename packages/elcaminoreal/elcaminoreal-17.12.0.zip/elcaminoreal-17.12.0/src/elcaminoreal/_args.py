"""
An experiment in a better way to build argument parsers.
"""
import argparse

import attr


def argparser(*things):
    """
    Generate a function that parses arguments.
    """
    ret = argparse.ArgumentParser()
    for thing in things:
        thing.add_to(ret)
    return ret.parse_args


# pylint: disable=invalid-name
@attr.s(frozen=True)
class argument(object):

    """
    An argument to the command
    """

    name = attr.ib()
    required = attr.ib(default=False)

    def add_to(self, parser):
        """
        Add myself parser
        """
        kwargs = {}
        if self.required:
            kwargs['required'] = True
        parser.add_argument(self.name, **kwargs)
# pylint: enable=invalid-name

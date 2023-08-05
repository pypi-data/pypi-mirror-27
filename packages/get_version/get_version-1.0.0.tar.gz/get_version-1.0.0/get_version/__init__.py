"""Provides the get_version function."""

from pkg_resources import get_distribution


def get_version(name):
    """Get the version of a particular package. Typical usage is:
    __version__ = get_version(__package__)
    Code modified from:
    https://stackoverflow.com/questions/20180543/how-to-check-version-of-python-modules
    """
    return get_distribution(name).version

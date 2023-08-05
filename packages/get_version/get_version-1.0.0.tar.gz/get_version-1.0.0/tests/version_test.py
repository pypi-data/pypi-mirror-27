from pytest import __version__
from get_version import get_version


def test_version():
    assert get_version('pytest') == __version__

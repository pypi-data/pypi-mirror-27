# get_version
Never store another version string.

## Usage
```
from get_version import get_version
__version__ = get_version(__package__)
```

The get_version module prevents you from having to maintain version numbers in your code. As most of the time the package will have been installed via pip you can simply extract the version using get-version, which internally uses pkg_resources.

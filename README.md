# polypy

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/polypy/master.svg)](https://circleci.com/gh/nschloe/polypy/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/polypy.svg)](https://codecov.io/gh/nschloe/polypy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi Version](https://img.shields.io/pypi/v/polypy.svg)](https://pypi.org/project/polypy)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/polypy.svg?logo=github&label=Stars)](https://github.com/nschloe/polypy)

Some description.

Run
```
find . -type f -print0 | xargs -0 sed -i 's/polypy/your-project-name/g'
```
to customize.

### Installation

polypy is [available from the Python Package
Index](https://pypi.org/project/polypy/), so simply type
```
pip install -U polypy
```
to install or upgrade.

### Testing

To run the polypy unit tests, check out this repository and type
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    make publish
    ```

### License

polypy is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).

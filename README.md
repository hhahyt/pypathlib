# pypathlib

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/pypathlib/master.svg)](https://circleci.com/gh/nschloe/pypathlib/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pypathlib.svg)](https://codecov.io/gh/nschloe/pypathlib)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi Version](https://img.shields.io/pypi/v/pypathlib.svg)](https://pypi.org/project/pypathlib)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pypathlib.svg?logo=github&label=Stars)](https://github.com/nschloe/pypathlib)

Lightweight package for working with 2D polygons.

```python
import pypathlib

# Create polygon
poly = pypathlib.Polygon([[0, 0], [0, 1], [1, 1], [1, 0]])

# Get the squared distance of some points to the polygon
poly.squared_distance([[0.5, 0.5], [0.1, 2.4]])

# Get the _signed_ squared distance of some points to the polygon
# (negative if inside the polygon)
poly.signed_squared_distance([[0.5, 0.5], [0.1, 2.4]])

# Check if the polygon contains the points
# (with a tolerance; set negative if you want to exclude the boundary)
poly.contains_points([[0.5, 0.5], [0.1, 2.4]], tol=1.0e-12)
```

pypathlib is fully vectorized, so it's pretty fast. (Not quite as fast as
[`mathplotlib.path.contains_points`](https://matplotlib.org/api/path_api.html#matplotlib.path.Path.contains_points)
though.)


### Relevant publications

 * [S.W. Sloan, _A point-in-polygon program_. Adv. Eng. Software, Vol 7, No. 1, pp.
   45-47, 1985, 10.1016/0141-1195(85)90094-4](https://doi.org/10.1016/0141-1195(85)90094-4).


### Installation

pypathlib is [available from the Python Package
Index](https://pypi.org/project/pypathlib/), so simply type
```
pip install -U pypathlib
```
to install or upgrade.

### Testing

To run the pypathlib unit tests, check out this repository and type
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

pypathlib is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).

# -*- coding: utf-8 -*-
#
import numpy
import pypathlib


def test_squared_distance():
    poly = pypathlib.Path([[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]])

    dist = poly.squared_distance(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    ref = numpy.array([0.01, 0.16, 1.0 / 104.0, 0.01, 0.02, 0.0])
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


if __name__ == "__main__":
    test_squared_distance()

# -*- coding: utf-8 -*-
#
import numpy
import polypy


def test_show():
    poly = numpy.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.1, 1.1],
        [0.1, 1.0],
    ])
    polypy.show(poly)
    return


def test_area():
    poly = polypy.Polygon([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.1, 1.1],
        [0.1, 1.0],
    ])

    ref = 1.045
    assert abs(poly.area - ref) < 1.0e-12 * ref
    return


if __name__ == "__main__":
    test_area()

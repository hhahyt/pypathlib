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


if __name__ == "__main__":
    test_show()

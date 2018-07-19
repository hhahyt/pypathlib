# -*- coding: utf-8 -*-
#
from matplotlib import path
import numpy
import polypy
import perfplot


def test_speed(n=3):
    poly_pts = [[0, 0], [0, 1], [1, 1], [1, 0]]
    poly0 = path.Path(poly_pts)
    poly1 = polypy.Polygon(poly_pts)

    def _mpl_poly(pts):
        return poly0.contains_points(pts)

    def _polypy_contains_points(pts):
        return poly1.contains_points(pts)

    numpy.random.seed(0)

    perfplot.show(
        setup=lambda n: numpy.random.rand(n, 2),
        kernels=[_mpl_poly, _polypy_contains_points],
        n_range=[2 ** k for k in range(n)],
        labels=["matplotlib.path.contains_points", "polypy.contains_points"],
        logx=True,
        logy=True,
        xlabel="num points",
    )
    return


def benchmark():
    poly_pts = [[0, 0], [0, 1], [1, 1], [1, 0]]
    poly1 = polypy.Polygon(poly_pts)
    pts = numpy.random.rand(5000000, 2)
    poly1.contains_points(pts)
    return


if __name__ == "__main__":
    # test_speed(20)
    benchmark()

# -*- coding: utf-8 -*-
#
import numpy
import polypy


def test_show():
    poly = numpy.array([[0.0, 0.0], [1.0, 0.0], [1.1, 1.1], [0.1, 1.0]])
    polypy.show(poly)
    return


def test_convex():
    poly = polypy.Polygon([[0.0, 0.0], [1.0, 0.0], [1.1, 1.1], [0.1, 1.0]])

    ref = 1.045
    assert abs(poly.area - ref) < 1.0e-12 * ref
    assert poly.positive_orientation
    assert all(poly.is_convex_node)
    return


def test_orientation():
    poly = polypy.Polygon([[0.1, 1.0], [1.1, 1.1], [1.0, 0.0], [0.0, 0.0]])

    ref = 1.045
    assert abs(poly.area - ref) < 1.0e-12 * ref
    assert not poly.positive_orientation
    assert all(poly.is_convex_node)
    return


def test_concave():
    poly = polypy.Polygon([[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.1, 1.1], [0.1, 1.0]])

    ref = 0.965
    assert abs(poly.area - ref) < 1.0e-12 * ref
    assert poly.positive_orientation
    assert numpy.array_equal(poly.is_convex_node, [True, True, False, True, True])
    return


def test_concave_counterclock():
    poly = polypy.Polygon([[0.1, 1.0], [1.1, 1.1], [0.9, 0.5], [1.0, 0.0], [0.0, 0.0]])

    ref = 0.965
    assert abs(poly.area - ref) < 1.0e-12 * ref
    assert not poly.positive_orientation
    assert numpy.array_equal(poly.is_convex_node, [True, True, False, True, True])
    return


def test_distance():
    poly = polypy.Polygon([[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]])

    dist = poly.squared_distance(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    ref = numpy.array([0.01, 0.16, 1.0 / 104.0, 0.01, 0.02, 0.0])
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


def test_inside():
    poly = polypy.Polygon([[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]])

    is_inside = poly.is_inside(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    assert numpy.array_equal(is_inside, [True, True, False, False, False, True])
    return


if __name__ == "__main__":
    test_inside()

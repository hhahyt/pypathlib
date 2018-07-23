# -*- coding: utf-8 -*-
#
import numpy
import pypathlib


def test_show():
    path = pypathlib.ClosedPath([[0.0, 0.0], [1.0, 0.0], [1.1, 1.1], [0.1, 1.0]])
    path.show()
    return


def test_convex():
    path = pypathlib.ClosedPath([[0.0, 0.0], [1.0, 0.0], [1.1, 1.1], [0.1, 1.0]])

    ref = 1.045
    assert abs(path.area - ref) < 1.0e-12 * ref
    assert path.positive_orientation
    assert all(path.is_convex_node)
    return


def test_orientation():
    path = pypathlib.ClosedPath([[0.1, 1.0], [1.1, 1.1], [1.0, 0.0], [0.0, 0.0]])

    ref = 1.045
    assert abs(path.area - ref) < 1.0e-12 * ref
    assert not path.positive_orientation
    assert all(path.is_convex_node)
    return


def test_concave():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.1, 1.1], [0.1, 1.0]]
    )

    ref = 0.965
    assert abs(path.area - ref) < 1.0e-12 * ref
    assert path.positive_orientation
    assert numpy.array_equal(path.is_convex_node, [True, True, False, True, True])
    return


def test_concave_counterclock():
    path = pypathlib.ClosedPath(
        [[0.1, 1.0], [1.1, 1.1], [0.9, 0.5], [1.0, 0.0], [0.0, 0.0]]
    )

    ref = 0.965
    assert abs(path.area - ref) < 1.0e-12 * ref
    assert not path.positive_orientation
    assert numpy.array_equal(path.is_convex_node, [True, True, False, True, True])
    return


def test_squared_distance():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]]
    )

    dist = path.squared_distance(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    ref = numpy.array([0.01, 0.16, 1.0 / 104.0, 0.01, 0.02, 0.0])
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


def test_distance():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]]
    )

    dist = path.distance(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    ref = numpy.array([0.1, 0.4, numpy.sqrt(1.0 / 104.0), 0.1, numpy.sqrt(2) / 10, 0.0])
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


def test_signed_distance():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]]
    )

    dist = path.signed_distance(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    print(dist)
    ref = numpy.array(
        [-0.1, -0.4, numpy.sqrt(1.0 / 104.0), 0.1, numpy.sqrt(2) / 10, 0.0]
    )
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


def test_inside():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]]
    )

    contains_points = path.contains_points(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    assert numpy.array_equal(contains_points, [True, True, False, False, False, True])
    return


def test_closest_points():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]]
    )

    closest_points = path.closest_points(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )

    ref = numpy.array(
        [
            [0.2, 0.0],
            [0.9, 0.5],
            [9.0384615384615385e-01, 5.1923076923076927e-01],
            [0.0, 1.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ]
    )
    assert numpy.all(numpy.abs(closest_points - ref) < 1.0e-12)
    return


def test_signed_squared_distance():
    path = pypathlib.ClosedPath(
        [[0.0, 0.0], [1.0, 0.0], [0.9, 0.5], [1.0, 1.0], [0.0, 1.0]]
    )

    dist = path.signed_squared_distance(
        [[0.2, 0.1], [0.5, 0.5], [1.0, 0.5], [0.0, 1.1], [-0.1, 1.1], [1.0, 1.0]]
    )
    ref = numpy.array([-0.01, -0.16, 1.0 / 104.0, 0.01, 0.02, 0.0])
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


def test_sharp_angle():
    path = pypathlib.ClosedPath(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 0.45],
            [0.6, 0.5],
            [1.0, 0.55],
            [1.0, 1.0],
            [0.0, 1.0],
        ]
    )

    contains_points = path.contains_points([[0.5, 0.4], [0.5, 0.6]])
    assert numpy.all(contains_points)

    dist = path.signed_squared_distance([[0.5, 0.4], [0.5, 0.6]])
    ref = numpy.array([-0.02, -0.02])
    assert numpy.all(numpy.abs(dist - ref) < 1.0e-12)
    return


# def test_two_points():
#     path = pypathlib.ClosedPath([[-0.5, 1.0], [+0.5, 1.0]])
#     contains_points = path.contains_points([[0.0, 0.0], [0.0, 2.0]])
#     assert numpy.array_equal(contains_points, [False, False])
#     return


if __name__ == "__main__":
    test_sharp_angle()

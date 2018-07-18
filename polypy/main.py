# -*- coding: utf-8 -*-
#
import numpy

from .helpers import shoelace


class Polygon(object):
    def __init__(self, points):
        self.points = numpy.array(points)
        assert self.points.shape[1] == 2

        self.edges = numpy.roll(points, -1, axis=0) - points
        self.e_dot_e = numpy.einsum("ij,ij->i", self.edges, self.edges)

        self.area = 0.5 * shoelace(self.points)
        self.positive_orientation = self.area > 0
        if self.area < 0:
            self.area = -self.area

        tri = numpy.array(
            [
                numpy.roll(self.points, +1, axis=0),
                self.points,
                numpy.roll(self.points, -1, axis=0),
            ]
        )
        self.is_convex_node = numpy.equal(shoelace(tri) > 0, self.positive_orientation)
        return

    def _all_distances(self, x):
        x = numpy.array(x).T
        assert x.shape[0] == 2

        # Find closest point for each side segment
        # <https://stackoverflow.com/q/51397389/353337>
        diff = x.T[:, None, :] - self.points[None, :, :]
        diff_dot_edge = numpy.einsum("ijk,jk->ij", diff, self.edges)
        t = diff_dot_edge / self.e_dot_e

        # The squared distance from the point x to the line defined by the points x0, x1
        # is
        #
        # (<x1-x0, x1-x0> <x-x0, x-x0> - <x-x0, x1-x0>**2) / <x1-x0, x1-x0>
        #
        dist2_points = numpy.einsum("ijk,ijk->ij", diff, diff)
        dist2_sides = (self.e_dot_e * dist2_points - diff_dot_edge ** 2) / self.e_dot_e

        # Index of the closest points and sides
        ip0 = numpy.argmin(dist2_points, axis=1)
        is0 = numpy.argmin(dist2_sides, axis=1)

        # Get the squared distance to the polygon. By default equals the distance to the
        # line, unless t < 0 (then the squared distance to x0), unless t > 1 (then the
        # squared distance to x1).
        dist2_polygon = dist2_sides.copy()
        dist2_polygon[t < 0.0] = dist2_points[t < 0.0]
        dist2_polygon[t > 1.0] = numpy.roll(dist2_points, -1, axis=1)[t > 1.0]

        r = numpy.arange(x.shape[1])
        is_closer_to_point = dist2_points[r, ip0] < dist2_sides[r, is0]

        idx = numpy.empty(is_closer_to_point.shape, dtype=int)
        idx[is_closer_to_point] = ip0[is_closer_to_point]
        idx[~is_closer_to_point] = is0[~is_closer_to_point]

        return t, dist2_polygon, is_closer_to_point, idx

    def squared_distance(self, x):
        """Get the squared distance of all points x to the polygon `poly`.
        """
        x = numpy.array(x)
        assert x.shape[1] == 2
        _, dist2_polygon, _, _ = self._all_distances(x)
        return numpy.min(dist2_polygon, axis=1)

    def is_inside(self, x):
        x = numpy.array(x)
        assert x.shape[1] == 2
        _, dist2_polygon, _, _ = self._all_distances(x)

        idx = numpy.argmin(dist2_polygon, axis=1)

        points = self.points
        next_points = numpy.roll(self.points, -1, axis=0)
        tri = numpy.array([x, points[idx], next_points[idx]])
        eps = 1.0e-15
        is_inside = (shoelace(tri) > -eps) == self.positive_orientation

        return is_inside

    def closest_points(self, x):
        """Get the closest points on the polygon.
        """
        x = numpy.array(x)
        assert x.shape[1] == 2
        t, dist2_polygon, _, _ = self._all_distances(x)

        idx = numpy.argmin(dist2_polygon, axis=1)

        t[t < 0.0] = 0.0
        t[t > 1.0] = 1.0

        pts0 = self.points[idx]
        pts1 = numpy.roll(self.points, -1, axis=0)[idx]
        r = numpy.arange(t.shape[0])
        t0 = t[r, idx]
        closest_points = (pts0.T * (1 - t0)).T + (pts1.T * t0).T
        return closest_points

    def plot(self):
        import matplotlib.pyplot as plt

        x = numpy.concatenate([self.points[:, 0], [self.points[0, 0]]])
        y = numpy.concatenate([self.points[:, 1], [self.points[0, 1]]])
        plt.plot(x, y, "-")
        return

    def show(self, *args, **kwargs):
        import matplotlib.pyplot as plt

        self.plot(*args, **kwargs)
        plt.show()
        return


def plot(points):
    Polygon(points).plot()
    return


def show(points):
    Polygon(points).show()
    return

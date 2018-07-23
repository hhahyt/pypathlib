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

        assert numpy.all(self.e_dot_e > 1.0e-12), \
            "Edge of 0 length are not permitted (edge lengths: {})".format(numpy.sqrt(self.e_dot_e))

        self.area = 0.5 * shoelace(self.points)
        self.positive_orientation = self.area > 0
        if self.area < 0:
            self.area = -self.area

        self._is_convex_node = None
        return

    def _all_distances(self, x):
        x = numpy.array(x)
        assert x.shape[1] == 2

        # Find closest point for each side segment
        # <https://stackoverflow.com/q/51397389/353337>
        diff = x[:, None, :] - self.points[None, :, :]
        diff_dot_edge = numpy.einsum("ijk,jk->ij", diff, self.edges)
        t = diff_dot_edge / self.e_dot_e

        # The squared distance from the point x to the line defined by the points x0, x1
        # is
        #
        # (<x1-x0, x1-x0> <x-x0, x-x0> - <x-x0, x1-x0>**2) / <x1-x0, x1-x0>
        #
        # <https://math.stackexchange.com/q/2856409/36678>
        dist2_points = numpy.einsum("ijk,ijk->ij", diff, diff)
        dist2_sides = (self.e_dot_e * dist2_points - diff_dot_edge ** 2) / self.e_dot_e

        # Get the squared distance to the polygon. By default equals the distance to the
        # line, unless t < 0 (then the squared distance to x0), unless t > 1 (then the
        # squared distance to x1).
        t0 = t < 0.0
        t1 = t > 1.0
        t[t0] = 0.0
        t[t1] = 1.0
        dist2_sides[t0] = dist2_points[t0]
        dist2_sides[t1] = numpy.roll(dist2_points, -1, axis=1)[t1]

        idx = numpy.argmin(dist2_sides, axis=1)
        dist2_sides = dist2_sides[numpy.arange(idx.shape[0]), idx]

        return t, dist2_sides, idx

    def squared_distance(self, x):
        """Get the squared distance of all points x to the polygon `poly`.
        """
        x = numpy.array(x)
        assert x.shape[1] == 2
        _, dist2_sides, _ = self._all_distances(x)
        return dist2_sides

    def _contains_points(self, t, x, idx):
        r = numpy.arange(idx.shape[0])

        contains_points = numpy.zeros(x.shape[0], dtype=bool)

        pts0 = self.points
        pts1 = numpy.roll(self.points, -1, axis=0)

        # If the point is closest to a polygon edge, check which which side of the edge
        # it is on.
        is_closest_to_side = (0.0 < t[r, idx]) & (t[r, idx] < 1.0)
        tri = numpy.array(
            [
                x[is_closest_to_side],
                pts0[idx[is_closest_to_side]],
                pts1[idx[is_closest_to_side]],
            ]
        )
        contains_points[is_closest_to_side] = (
            shoelace(tri) > 0.0
        ) == self.positive_orientation

        # If the point is closest to a polygon node, check if the node is convex or
        # concave.
        is_closest_to_pt0 = t[r, idx] <= 0.0
        contains_points[is_closest_to_pt0] = ~self.is_convex_node[
            idx[is_closest_to_pt0]
        ]

        is_closest_to_pt1 = 1.0 <= t[r, idx]
        n = self.points.shape[0]
        contains_points[is_closest_to_pt1] = ~self.is_convex_node[
            (idx[is_closest_to_pt1] + 1) % n
        ]

        return contains_points

    def contains_points(self, x, tol=1.0e-15):
        return self.signed_squared_distance(x) < tol

    def signed_squared_distance(self, x):
        """Negative inside the polgon.
        """
        x = numpy.array(x)
        assert x.shape[1] == 2
        t, dist2, idx = self._all_distances(x)

        # Due to round-off error, the squared distances will sometimes be negative in
        # the order of machine precision. This gives errors when computing the root.
        # Don't sqrt for now and keep an eye on
        # <https://math.stackexchange.com/q/2856409/36678>.
        # dist = numpy.sqrt(dist2)

        contains_points = self._contains_points(t, x, idx)
        dist2[contains_points] *= -1
        return dist2

    def closest_points(self, x):
        """Get the closest points on the polygon.
        """
        x = numpy.array(x)
        assert x.shape[1] == 2
        t, _, idx = self._all_distances(x)

        pts0 = self.points[idx]
        pts1 = numpy.roll(self.points, -1, axis=0)[idx]
        r = numpy.arange(t.shape[0])
        t0 = t[r, idx]
        closest_points = (pts0.T * (1 - t0)).T + (pts1.T * t0).T
        return closest_points

    @property
    def is_convex_node(self):
        if self._is_convex_node is None:
            tri = numpy.array(
                [
                    numpy.roll(self.points, +1, axis=0),
                    self.points,
                    numpy.roll(self.points, -1, axis=0),
                ]
            )
            self._is_convex_node = numpy.equal(
                shoelace(tri) > 0, self.positive_orientation
            )
        return self._is_convex_node

    def plot(self, color="#1f77b4"):
        import matplotlib.pyplot as plt

        x = numpy.concatenate([self.points[:, 0], [self.points[0, 0]]])
        y = numpy.concatenate([self.points[:, 1], [self.points[0, 1]]])
        plt.plot(x, y, "-", color=color)

        plt.axis("square")
        return

    def show(self, *args, **kwargs):
        import matplotlib.pyplot as plt

        self.plot(*args, **kwargs)
        plt.show()
        return


def show(points):
    Polygon(points).show()
    return

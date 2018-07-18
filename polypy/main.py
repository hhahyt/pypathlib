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
        diff_dot_diff = numpy.einsum("ijk,ijk->ij", diff, diff)
        dist2_lines = (self.e_dot_e * diff_dot_diff - diff_dot_edge ** 2) / self.e_dot_e

        return t, diff_dot_diff, dist2_lines

    def squared_distance(self, x):
        """Get the squared distance of all points x to the polygon `poly`.
        """
        assert x.shape[1] == 2
        t, dist2_points, dist2_lines = self._all_distances(x)

        # Get the squared distance to the polygon. By default equals the distance to the
        # line, unless t < 0 (then the squared distance to x0), unless t > 1 (then the
        # squared distance to x1).
        dist2_polygon = dist2_lines.copy()
        dist2_polygon[t < 0.0] = dist2_points[t < 0.0]
        dist2_polygon[t > 1.0] = numpy.roll(dist2_points, -1, axis=1)[t > 1.0]
        dist2_polygon = numpy.min(dist2_polygon, axis=1)

        return dist2_polygon

    def is_inside(self, x):
        x = numpy.array(x)
        assert x.shape[1] == 2
        t, dist2_points, dist2_lines = self._all_distances(x)

        is_close_to_node0 = t < 0.0
        is_close_to_node1 = t > 1.0
        is_close_to_side = ~(is_close_to_node0 | is_close_to_node1)

        dist2_polygon = dist2_lines.copy()
        dist2_polygon[is_close_to_node0] = dist2_points[is_close_to_node0]
        dist2_polygon[is_close_to_node1] = numpy.roll(dist2_points, -1, axis=1)[
            is_close_to_node1
        ]
        idx = numpy.argmin(dist2_polygon, axis=1)

        is_inside = numpy.ones(x.shape[0], dtype=bool)

        # if the left node is closest to the point and it is a convex node, the point is
        # outside
        r = numpy.arange(idx.shape[0])
        node0_out = numpy.logical_and(
            is_close_to_node0[r, idx], self.is_convex_node[idx]
        )
        is_inside[node0_out] = False
        # Same for outs on the right side
        node1_out = numpy.logical_and(
            is_close_to_node1[r, idx], numpy.roll(self.is_convex_node, -1)[idx]
        )
        is_inside[node1_out] = False

        # if the point is closest to a side, check the orientation
        ic = is_close_to_side[r, idx]
        tri = numpy.array([
            x[ic],
            self.points[idx[ic]],
            self.points[(idx[ic] + 1) % self.points.shape[0]]
        ])
        eps = 1.0e-15
        is_outside = (shoelace(tri) > -eps) != self.positive_orientation

        ic0 = numpy.where(ic)[0]
        is_inside[ic0[is_outside]] = False

        return is_inside

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

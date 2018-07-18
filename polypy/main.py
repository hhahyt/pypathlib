# -*- coding: utf-8 -*-
#
import numpy


def plot(poly):
    import matplotlib.pyplot as plt
    x = numpy.concatenate([poly[:, 0], [poly[0, 0]]])
    y = numpy.concatenate([poly[:, 1], [poly[0, 1]]])
    plt.plot(x, y, "-")
    return


def show(*args, **kwargs):
    import matplotlib.pyplot as plt
    plot(*args, **kwargs)
    plt.show()
    return

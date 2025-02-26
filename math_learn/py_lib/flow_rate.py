import matplotlib.pyplot as plt
import numpy as np


def plot_function(f, tmin, tmax, tlabel=None, xlabel=None, axes=False, **kwargs):
    ts = np.linspace(tmin, tmax, 1000)
    if tlabel:
        plt.xlabel(tlabel, fontsize=18)
    if xlabel:
        plt.ylabel(xlabel, fontsize=18)
    plt.plot(ts, [f(t) for t in ts], **kwargs)
    if axes:
        total_t = tmax - tmin
        plt.plot([tmin - total_t / 10, tmax + total_t / 10], [0, 0], c='k', linewidth=1)
        plt.xlim(tmin - total_t / 10, tmax + total_t / 10)
        xmin, xmax = plt.ylim()
        plt.plot([0, 0], [xmin, xmax], c='k', linewidth=1)
        plt.ylim(xmin, xmax)


def plot_volume(f, tmin, tmax, axes=False, **kwargs):
    plot_function(f, tmin, tmax, tlabel="time (hr)", xlabel="volume (bbl)", axes=axes, **kwargs)


def plot_flow_rate(f, tmin, tmax, axes=False, **kwargs):
    plot_function(f, tmin, tmax, tlabel="time (hr)", xlabel="flow rate (bbl/hr)", axes=axes, **kwargs)


def volume(t):
    return (t - 4) ** 3 / 64 + 3.3


def flow_rate(t):
    return 3 * (t - 4) ** 2 / 64


def secant_line(f, x1, x2):
    def line(x):
        return f(x1) + (x - x1) * (f(x2) - f(x1)) / (x2 - x1)

    return line


def plot_secant(f, x1, x2, color='k'):
    line = secant_line(f, x1, x2)
    plot_function(line, x1, x2, c=color)
    plt.scatter([x1, x2], [f(x1), f(x2)], c=color)


def plot_points(points, color='k'):
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    plt.scatter(x_list, y_list, c=color)

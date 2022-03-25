from typing import Iterable, Tuple
import time
from bisect_scanner.util import produce_gradual
import itertools as it
import numpy as np
import matplotlib.pyplot as plt


STEPS = 10000


def axes(balances):
    x_axis, y_axis = [*zip(*balances)]
    x_start, x_end = x_axis[0], x_axis[-1]
    xdiff = x_end - x_start
    if xdiff:
        x_axis = [round(((x - x_start) / xdiff) * STEPS) for x in x_axis]
    return x_axis, [*y_axis]


def ticks(balances, n_ticks=5):
    ticks = [round(STEPS/n_ticks) * x for x in range(n_ticks)]
    x_start, x_end = balances[0][0], balances[-1][0]
    xdiff = x_end - x_start
    labels = [round((tick / STEPS) * xdiff) + x_start for tick in ticks]
    return ticks, labels


def step_fn(x_axis, y_axis):
    ls_y = np.zeros(STEPS)
    prev = 0
    for x, y in zip(x_axis[1:], y_axis):
        x_ = (x - x_axis[0])
        ls_y[prev:x_] = y
        prev = x_
    return ls_y


def plot(balances: Iterable[Tuple[int, float]], block=True, show=True, zoom=False):
    x_axis, y_axis = axes(balances)
    ls_y = step_fn(x_axis, y_axis)
    ls_x = np.linspace(0, STEPS, STEPS)
    plt.cla()
    plt.xticks(*ticks(balances))
    plt.plot(ls_x, ls_y)
    if zoom:
        mng = plt.get_current_fig_manager()
        mng.resize(1500, 700)
    if show:
        plt.show(block=block)
        plt.pause(1)


def plot_gradual(balances: Iterable[Tuple[int, float]], wait_after=0):
    for balances_ in produce_gradual(balances):
        plot(balances_, block=False)
        plt.pause(1)
        plt.cla()
    time.sleep(wait_after)


def with_plot(balances: Iterable[Tuple[int, float]], end_block=None):
    balances1, balances2 = it.tee(balances)
    producer = produce_gradual(balances1, end_block)
    plt.ion()
    for balances_, balance in zip(producer, balances2):
        yield balance
        show = len(balances_) > 0
        plot(balances_, block=False, show=show, zoom=True)

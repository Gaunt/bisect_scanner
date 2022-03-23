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


def plot(balances: Iterable[Tuple[int, float]], block=True):
    x_axis, y_axis = axes(balances)
    ls_y = step_fn(x_axis, y_axis)
    ls_x = np.linspace(0, STEPS, STEPS)
    plt.xticks(*ticks(balances))
    plt.plot(ls_x, ls_y)
    plt.show(block=block)
    return plt


def plot_gradual(balances: Iterable[Tuple[int, float]]):
    for balances_ in produce_gradual(balances):
        plt = plot(balances_, block=False)
        plt.pause(0.1)
        plt.cla()
    time.sleep(5)


def with_plot(balances: Iterable[Tuple[int, float]], end_block=None):
    balances1, balances2 = it.tee(balances)
    producer = produce_gradual(balances1, end_block)
    for balances_, balance in zip(producer, balances2):
        yield balance
        plt = plot(balances_, block=False)
        plt.pause(0.01)
        plt.cla()

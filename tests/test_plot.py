from bisect_scanner.plot import axes, step_fn, plot
from bisect_scanner.util import slowed_down, produce_gradual
import time
import pytest


BALANCES = [
    (0, 0.0),
    (11503731, 0.005),
    (12103372, 0.015),
    (12107610, 0.009),
    (12425773, 0.0),
    (14412861, 0.0),
]


def test_axes():
    x_axis, y_axis = axes(BALANCES)
    assert x_axis == [0, 7982, 8398, 8401, 8621, 10000]
    assert y_axis == [0.0, 0.005, 0.015, 0.009, 0.0, 0.0]


def test_step_fn():
    x_axis, y_axis = axes(BALANCES)
    linsp = step_fn(x_axis, y_axis)
    assert set(linsp) == {0.0, 0.015, 0.009, 0.005}


@pytest.mark.skip()
def test_plot():
    plot(BALANCES)


@pytest.mark.skip()
def test_plot_gradual():
    for balances in produce_gradual(BALANCES):
        plt = plot(balances, block=False)
        plt.pause(0.1)
        plt.cla()
    # plot(balances)
    time.sleep(5)

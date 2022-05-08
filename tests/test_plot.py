import bisect_scanner.plot as plot  # axes, step_fn, plot, with_plot, plot_gradual
from bisect_scanner.util import slowed_down, produce_gradual
import time
import pytest
from unittest.mock import MagicMock

BALANCES = [
    (0, 0.0),
    (11503731, 0.005),
    (12103372, 0.015),
    (12107610, 0.009),
    (12425773, 0.0),
    (14412861, 0.0),
]


plot.plt.show = MagicMock


def test_axes():
    x_axis, y_axis = plot.axes(BALANCES)
    assert x_axis == [0, 7982, 8398, 8401, 8621, 10000]
    assert y_axis == [0.0, 0.005, 0.015, 0.009, 0.0, 0.0]


def test_step_fn():
    x_axis, y_axis = plot.axes(BALANCES)
    linsp = plot.step_fn(x_axis, y_axis)
    assert set(linsp) == {0.0, 0.015, 0.009, 0.005}


@pytest.mark.plot
def test_plot():
    plot.plot(BALANCES)


@pytest.mark.plot
def test_plot_gradual():
    plot.plot_gradual(slowed_down(BALANCES, delay=0))

    
@pytest.mark.plot
def test_with_plot():
    balances = [*plot.with_plot(slowed_down(BALANCES, delay=0))]
    assert balances == [
        (0, 0.0),
        (11503731, 0.005),
        (12103372, 0.015),
        (12107610, 0.009),
        (12425773, 0.0),
        (14412861, 0.0),
    ]

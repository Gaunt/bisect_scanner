import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run_network", action="store_true", help="run tests requiring network connection"
    )
    parser.addoption(
        "--run_plot", action="store_true", help="run plotting tests"
    )


def pytest_collection_modifyitems(config, items):
    skip_network = False
    if not config.getoption("--run_network"):
        skip_network = pytest.mark.skip(reason="need --run_network option to run")
        for item in items:
            if "network" in item.keywords:
                item.add_marker(skip_network)

    skip_plot = False
    if not config.getoption("--run_plot"):
        skip_plot = pytest.mark.skip(reason="need --run_plot option to run")
        for item in items:
            if "plot" in item.keywords:
                item.add_marker(skip_plot)


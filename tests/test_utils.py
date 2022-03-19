from bisect_scanner.util import slowed_down, produce_gradual


BALANCES = [
    (0, 0.0),
    (11503731, 0.005),
    (12103372, 0.015),
    (12107610, 0.009),
    (12425773, 0.0),
    (14412861, 0.0),
]


def test_slowed_down():
    assert [*slowed_down(BALANCES, 0)] == BALANCES


def test_gradual():
    gradual = [*produce_gradual(BALANCES, 0)]
    assert gradual == [
        [(0, 0.0), (14412861, 0.0)],
        [(0, 0.0), (11503731, 0.005), (14412861, 0.0)],
        [(0, 0.0), (11503731, 0.005), (12103372, 0.015), (14412861, 0.0)],
        [
            (0, 0.0),
            (11503731, 0.005),
            (12103372, 0.015),
            (12107610, 0.009),
            (14412861, 0.0),
        ],
        [
            (0, 0.0),
            (11503731, 0.005),
            (12103372, 0.015),
            (12107610, 0.009),
            (12425773, 0.0),
            (14412861, 0.0),
        ],
    ]

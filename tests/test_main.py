import bisect_scanner.__main__ as main
from textwrap import dedent


def test_main(capfd):
    main.main('a', scanner='fake')
    out, err = capfd.readouterr()
    expected_out = dedent('''\
    block,balance
    0,0
    1001,2000
    200001,1
    200002,4000
    200101,2
    ''')
    assert out.replace('\r\n', '\n') == expected_out


def test_parse_args():
    args = main.parse_args(['--account=a'])

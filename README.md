# bisect_scanner

Scan for balance history

## Usage

```python
>>> from bisect_scanner import PolygonScanner
>>> scanner = PolygonScanner(account)
>>> scanner.balance_history()
 [
        (0, 0),
        (0, 0),
        (1, 1000),
        (5, 1001.5),
        (1000, 1003),
        (1001, 2000),
]
```

## Authors

`bisect_scanner` was written by `Karel Novak <novakk5@gmail.com>`_.

bisect_scanner
================

Scan for balance history

Usage
-----------------

>>> from bisect_scanner import W3Scanner
>>> W3_URL = '...' # w3 archive node url
>>> account = '0x790370ff5045bCeCc2161f0913302FCCC7Ee256d'
>>> scanner = W3Scanner(W3_URL)
>>> [*eth.balance_history('0x790370ff5045bCeCc2161f0913302FCCC7Ee256d')] 
[(0, 0.0),
 (11503731, 0.005),
 (12103372, 0.015),
 (12107610, 0.009),
 (12425773, 0.0)]


Authors
-------------------------------

*bisect_scanner* was written by Karel Novak.

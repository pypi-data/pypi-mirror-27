sqlextension
============
This module makes some SQL commands available for use with python-sql.

Install
=======
pip install mds-sqlextension

Available SQL commands
======================

- AnyInArray (any)
- ArrayAgg (array_agg)
- Ascii (ascii)
- Concat2 (concat)
- FuzzyEqal (%)
- Lower (lower)
- Replace (replace)
- RPad (rpad)
- SplitPart (split_part)
- StringAgg (string_agg)

To make FuzzyEqual work, call *CREATE EXTENSION pg_trgm;* in PostgreSQL.

Requires
========
- python-sql

Changes
=======

*0.1.4 - 12/14/2017*

- bugfix: import-syntax in python3
- added docstrings for help

*0.1.3 - 07/14/2017*

- added 'split_part'

*0.1.2 - 06/09/2017*

- import optimized

*0.1.1 - 06/09/2017*

- first public version



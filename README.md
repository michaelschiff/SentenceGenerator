SentenceGenerator
=================

make english

WordSmasher_v2.py is the current main version

construct a sentence generator:
```SentenceGenerator("romeo_and_juliet.txt", 3)```
Uses "romeo_and_juliet.txt" as the source text, and a lookback window of size 3.  Currently, a lookback window of size N will create a probability matrix for each n-tuple of size 1..N

generate text:
```x.generate_sentence(2, 250)```
uses the 2-arity probability matrix, and generates a phrase of length=250

Run:
```python WordSmasher_v2.py```

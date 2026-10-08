# big-integer-nth-root

Computes the integer floor of the kth root of an arbitrarily large integer using an integer-only Newton iteration.

```python
from big_integer_nth_root import nth_root

assert nth_root(125, 3) == 5
assert nth_root(124, 3) == 4
assert nth_root(12345678901234567890 ** 7, 7) == 12345678901234567890
```

## Why

`int(n ** (1 / k))` goes through floating point and stops being meaningful once `n` has more than about 15–16 significant digits: the float rounds, the cast truncates, and you get an answer that is off by one (or worse, off by many). This library exists to give a correct floor for inputs of any size, which matters when you are, for example, checking whether a big number is a perfect power.

The trade-off is speed versus correctness: the iteration here is pure integer arithmetic, so it never loses precision, but for very large inputs and large `k` the `pow(x, k-1)` step in each Newton step is not cheap. It is the right call when you need the answer to be right, not when you need it to be fast.

## Edge cases

- `n` must be non-negative and `k` must be a positive `int`. Negative `n` raises `ValueError`; `k < 1` raises `ValueError`.
- `bool` is explicitly rejected for both arguments. `bool` is a subclass of `int` in Python, so without this check `nth_root(16, True)` would silently mean `nth_root(16, 1)` and return `16`, which is almost certainly not what a caller intended.
- The result is the floor. `nth_root(124, 3)` returns `4`, not `5`, because `4**3 = 64 <= 124 < 125 = 5**3`.

## Exports

- `nth_root(n, k)` — returns `floor(n ** (1/k))` as an `int`.
- `floor_nth_root(n, k)` — alias of `nth_root`, for callers who want the "floor" in the name.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

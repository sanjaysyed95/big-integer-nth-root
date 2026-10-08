"""Floor of the kth root of a non-negative integer via Newton iteration.

The built-in ``pow(n, 1/k)`` path is a floating-point computation and loses
precision past a few dozen digits. For arbitrarily large integers we instead
run Newton's method entirely in the integer domain so no precision is lost.
"""


def _initial_guess(n: int, k: int) -> int:
    """A cheap-ish starting point for Newton's method.

    We use ``int(n ** (1.0 / k))`` when ``n`` is small enough that the float
    is exact-ish, and fall back to a bit-length estimate otherwise. The
    estimate only needs to be >= the true root and not absurdly large; Newton
    converges quadratically from any overestimate, so a rough upper bound is
    fine and keeps us out of floating-point territory entirely for big inputs.
    """
    if n < (1 << 53):
        # Below 2**53 floats are exact integers, so the float root is a safe
        # starting overestimate (we clamp up by one in case rounding lands low).
        g = int(n ** (1.0 / k))
        return g + 1
    # bit-length upper bound: if n < 2**b then n**(1/k) < 2**(ceil(b/k)).
    b = n.bit_length()
    return 1 << ((b + k - 1) // k)


def nth_root(n: int, k: int) -> int:
    """Return the floor of the kth root of ``n``: ``floor(n ** (1/k))``.

    Requirements:
        - ``n`` is a non-negative ``int``.
        - ``k`` is an ``int`` >= 1.

    Raises:
        TypeError: if either argument is not an ``int``.
        ValueError: if ``n`` < 0 or ``k`` < 1.
        ZeroDivisionError: if ``k`` == 0 (caught by the ``k < 1`` check first,
            but documented for completeness).

    The iteration is the classic integer Newton step for ``x**k = n``:
        x' = ((k-1)*x + n // x**(k-1)) // k
    which is monotonically decreasing as long as we start above the true root,
    and never undershoots. We stop when the value stabilises.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an int")
    if k < 1:
        raise ValueError("k must be >= 1")
    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return 0
    if k == 1:
        return n
    if n == 1:
        return 1

    x = _initial_guess(n, k)
    km1 = k - 1
    # Newton iteration. Because we start from an overestimate, the sequence is
    # non-increasing and integer, so it must converge. We loop until the value
    # stops decreasing; the stable value is the floor of the root.
    while True:
        # x**(k-1) is the expensive part; recompute each step for simplicity.
        y = (km1 * x + n // pow(x, km1)) // k
        if y >= x:
            return x
        x = y


# Alias chosen so callers who prefer the explicit "floor" framing can use it.
floor_nth_root = nth_root

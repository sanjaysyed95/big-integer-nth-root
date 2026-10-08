"""Integer nth root of arbitrarily large integers.

Public surface:
    nth_root(n, k) -> int
    floor_nth_root(n, k) -> int  (alias of nth_root)
"""

from .core import nth_root, floor_nth_root

__all__ = ["nth_root", "floor_nth_root"]

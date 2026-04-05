"""
irrational_map.py

Lookup table mapping decimal approximations (as output by iso) to their
exact symbolic forms in each output mode.

Format: IRRATIONAL_MAP[decimal_string] = {
    'display': human-readable form,
    'code':    sympy-compatible Python expression,
    'latex':   LaTeX math expression,
    'nb':      Mathematica expression,
}

Add entries here as new values are encountered in practice.
Matching is done on 3-decimal-place string representation of the coefficient.

To use: before output formatting, scan polynomial strings for decimal numbers
and replace using this map. Numbers not found in the map are left as-is.
"""

import math

def _entry(n, m, denom=False):
    """Helper to build a map entry for n*sqrt(m) or n/sqrt(m)."""
    if denom:
        display = f"1/\u221a{m}" if n == 1 else f"{n}/\u221a{m}"
        code    = f"1/sp.sqrt({m})" if n == 1 else f"{n}/sp.sqrt({m})"
        latex   = f"1/\\sqrt{{{m}}}" if n == 1 else f"{n}/\\sqrt{{{m}}}"
        nb      = f"1/Sqrt[{m}]" if n == 1 else f"{n}/Sqrt[{m}]"
    else:
        display = f"\u221a{m}" if n == 1 else f"{n}\u221a{m}"
        code    = f"sp.sqrt({m})" if n == 1 else f"{n}*sp.sqrt({m})"
        latex   = f"\\sqrt{{{m}}}" if n == 1 else f"{n}\\sqrt{{{m}}}"
        nb      = f"Sqrt[{m}]" if n == 1 else f"{n}*Sqrt[{m}]"
    return {"display": display, "code": code, "latex": latex, "nb": nb}


# Auto-generate entries for n*sqrt(m) and n/sqrt(m)
# for small integers n in [1,12] and m in [2,3,5,6,7,10,11,13,15]
IRRATIONAL_MAP = {}

_sqrts = [2, 3, 5, 6, 7, 10, 11, 13, 15]

for m in _sqrts:
    s = math.sqrt(m)
    for n in range(1, 13):
        # n*sqrt(m)
        key = f"{n * s:.3f}"
        if key not in IRRATIONAL_MAP:
            IRRATIONAL_MAP[key] = _entry(n, m, denom=False)
        # n/sqrt(m)
        key2 = f"{n / s:.3f}"
        if key2 not in IRRATIONAL_MAP:
            IRRATIONAL_MAP[key2] = _entry(n, m, denom=True)

# Manual overrides and additional entries can be added below.
# These take precedence if added after the auto-generation block.
# Example:
# IRRATIONAL_MAP["1.732"] = {
#     "display": "√3", "code": "sp.sqrt(3)",
#     "latex": r"\sqrt{3}", "nb": "Sqrt[3]",
# }

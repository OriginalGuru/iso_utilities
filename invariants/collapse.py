"""
collapse.py
Collapses individual invariants into a single free energy polynomial
with named coefficients, and checks for duplicates.
"""

from typing import Dict, List, Tuple
import re


def _normalize_polynomial(polynomial: str) -> str:
    """
    Normalize a polynomial string for duplicate detection.
    Strips whitespace and sorts terms alphabetically so that
    'A + B' and 'B + A' are treated as equal.
    """
    # split on + and - separators
    terms = re.split(r'\s+\+\s+', polynomial.strip())
    # strip leading/trailing whitespace from each term
    terms = [t.strip() for t in terms]
    # sort for canonical form
    terms = sorted(terms)
    return ' + '.join(terms)


def build_collapsed(
    invariants: List[dict],
    coeff_style: str = "c",
) -> Tuple[List[dict], List[Tuple[int, int]]]:
    """
    Build collapsed free energy from invariant list.

    Checks for duplicate invariants (after normalization) and warns.

    Args:
        invariants: substituted + filtered invariant list
        coeff_style: prefix for coefficient names

    Returns:
        (collapsed, duplicates) where:
          collapsed: list of dicts with 'degree', 'polynomial', 'coeff'
          duplicates: list of (i, j) index pairs that are identical after normalization
    """
    normalized = [_normalize_polynomial(inv["polynomial"]) for inv in invariants]

    # detect duplicates
    duplicates = []
    seen = {}
    for i, norm in enumerate(normalized):
        if norm in seen:
            duplicates.append((seen[norm], i))
        else:
            seen[norm] = i

    if duplicates:
        print(f"  WARNING: {len(duplicates)} duplicate invariant(s) detected:")
        for i, j in duplicates:
            print(f"    [{i+1}] and [{j+1}] are identical after normalization")

    collapsed = []
    for i, inv in enumerate(invariants):
        collapsed.append({
            "degree": inv["degree"],
            "polynomial": inv["polynomial"],
            "coeff": f"{coeff_style}{i+1}",
        })

    return collapsed, duplicates

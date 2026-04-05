"""
output_nb.py
Mathematica notebook (.nb) output for invariant polynomials.

Converts parenthesised substituted polynomials to Mathematica expressions:
  - )^N(  ->  )^N*(   (adjacent terms with exponents)
  - )(    ->  )*(      (adjacent degree-1 terms)
  - ^ is already correct for Mathematica
"""

import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path


def _fmt(polynomial: str) -> str:
    """Convert to Mathematica expression."""
    result = re.sub(r'\)(\^\d+)?\(', lambda m: ')' + (m.group(1) or '') + '*(', polynomial)
    return result


def _esc(s: str) -> str:
    """Escape for Mathematica string literals."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def write_nb(
    outpath: Path,
    parent: int,
    irreps: List[str],
    degree: Tuple[int, int],
    var_map: Dict[str, dict],
    invariants: List[dict],
    collapsed: Optional[List[dict]] = None,
    coeff_style: str = "c",
) -> None:
    deg_lo, deg_hi = degree
    deg_str = str(deg_lo) if deg_lo == deg_hi else f"{deg_lo}-{deg_hi}"
    all_vars = [info["code"] for info in var_map.values()]

    cells = []

    title = (f"Invariant Polynomials\\nSpace group: {parent}\\n"
             f"Irreps: {_esc(', '.join(irreps))}\\nDegree: {deg_str}")
    cells.append(f'Cell[TextData[{{"{title}"}}], "Title"]')

    # variable declarations — just list them, Mathematica treats them as symbols
    var_list = ", ".join(all_vars)
    cells.append(f'Cell[BoxData["{_esc("{" + var_list + "}")}"], "Input"]')

    inv_items = []
    for inv in invariants:
        inv_items.append(f"  {_fmt(inv['polynomial'])}  (* deg {inv['degree']} *)")
    inv_block = "invariants = {\n" + ",\n".join(inv_items) + "\n};"
    cells.append(f'Cell[BoxData["{_esc(inv_block)}"], "Input"]')

    if collapsed:
        coeff_names = [f"{coeff_style}{i+1}" for i in range(len(collapsed))]
        coeff_list = ", ".join(coeff_names)
        cells.append(f'Cell[BoxData["{_esc("{" + coeff_list + "}")}"], "Input"]')

        f_terms = []
        for i, inv in enumerate(collapsed):
            f_terms.append(f"  {coeff_style}{i+1} * ({_fmt(inv['polynomial'])})")
        f_block = "F = (\n" + " +\n".join(f_terms) + "\n);"
        cells.append(f'Cell[BoxData["{_esc(f_block)}"], "Input"]')

    nb_content = (
        "(* Content-type: application/vnd.wolfram.mathematica *)\n\n"
        "Notebook[{\n"
        + ",\n\n".join(cells)
        + "\n}, WindowSize->{1200, 800}]\n"
    )

    outpath.write_text(nb_content)
    print(f"  Written: {outpath}")

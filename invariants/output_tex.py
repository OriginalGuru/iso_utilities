"""
output_tex.py
LaTeX output for invariant polynomials.

Converts parenthesised substituted polynomials to LaTeX math expressions:
  - ^N       ->  ^{N}       (proper LaTeX exponents)
  - )^{N}(   ->  )^{N}\,(   (thin space between adjacent exponentiated terms)
  - )(        ->  )\,(       (thin space between adjacent degree-1 terms)
  - strip remaining ( and )
  - escape - and + inside variable names: GM2- -> GM2{-}, GM6+ -> GM6{+}
  - handle numeric coefficient before (: 2( stays as 2 after paren strip
"""

import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path


def _fmt(polynomial: str) -> str:
    """Convert to LaTeX math expression."""
    # ^N -> ^{N}
    result = re.sub(r'\^(\d+)', r'^{\1}', polynomial)
    # insert \, between adjacent tokens: )^{N}( and )(
    result = re.sub(r'\)((\^\{\d+\})?)\(', lambda m: ')' + m.group(1) + r'\,(', result)
    # strip parentheses
    result = result.replace('(', '').replace(')', '')
    # spaces around term separators - only match + preceded by space (term boundary)
    result = re.sub(r'\s+\+\s*', ' + ', result)
    result = re.sub(r'\s+-\s*(?=\d)', ' - ', result)
    # then escape +/- inside variable names
    result = re.sub(r'(?<=[A-Za-z0-9])-(?=[A-Za-z_])', '{-}', result)
    result = re.sub(r'(?<=[A-Za-z0-9])\+(?=[A-Za-z_])', '{+}', result)
    return result


def _tex_irrep(label: str) -> str:
    """Escape irrep label for LaTeX texttt."""
    return label.replace('-', r'\textminus{}').replace('+', r'\textplus{}')


def _tex_varname(name: str) -> str:
    """Escape variable display name for LaTeX texttt."""
    return (name.replace('_', r'\_')
                .replace('-', r'\textminus{}')
                .replace('+', r'\textplus{}'))


def write_tex(
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
    deg_str = str(deg_lo) if deg_lo == deg_hi else f"{deg_lo}--{deg_hi}"
    irreps_tex = ", ".join(f"\\texttt{{{_tex_irrep(r)}}}" for r in irreps)

    lines = []
    lines.append(r'\documentclass{article}')
    lines.append(r'\usepackage{amsmath}')
    lines.append(r'\usepackage{booktabs}')
    lines.append(r'\usepackage{textcomp}')
    lines.append(r'\begin{document}')
    lines.append('')
    lines.append(r'\section*{Invariant Polynomials}')
    lines.append('')
    lines.append(r'\begin{tabular}{ll}')
    lines.append(r'\toprule')
    lines.append(f'Space group & {parent} \\\\')
    lines.append(f'Irreps & {irreps_tex} \\\\')
    lines.append(f'Degree & {deg_str} \\\\')
    lines.append(f'Total invariants & {len(invariants)} \\\\')
    lines.append(r'\bottomrule')
    lines.append(r'\end{tabular}')
    lines.append('')

    lines.append(r'\subsection*{Variable Map}')
    lines.append('')
    lines.append(r'\begin{tabular}{lll}')
    lines.append(r'\toprule')
    lines.append(r'iso name & display name & magnetic \\')
    lines.append(r'\midrule')
    for iso_name, info in var_map.items():
        mag = "yes" if info["magnetic"] else "no"
        lines.append(
            f'\\texttt{{{iso_name}}} & '
            f'\\texttt{{{_tex_varname(info["display"])}}} & {mag} \\\\'
        )
    lines.append(r'\bottomrule')
    lines.append(r'\end{tabular}')
    lines.append('')

    lines.append(r'\subsection*{Invariants}')
    lines.append('')
    degrees_seen = sorted(set(inv["degree"] for inv in invariants))
    idx = 1
    for deg in degrees_seen:
        deg_invs = [inv for inv in invariants if inv["degree"] == deg]
        lines.append(f'\\subsubsection*{{Degree {deg}}}')
        lines.append('')
        lines.append(r'\begin{align*}')
        for inv in deg_invs:
            lines.append(f'I_{{{idx}}} &= {_fmt(inv["polynomial"])} \\\\')
            idx += 1
        lines.append(r'\end{align*}')
        lines.append('')

    if collapsed:
        lines.append(r'\subsection*{Free Energy}')
        lines.append('')
        lines.append(r'\begin{align*}')
        lines.append(r'F &=')
        for i, inv in enumerate(collapsed):
            end = r' \\' if i < len(collapsed) - 1 else ''
            lines.append(
                f'  &\\quad {coeff_style}_{{{i+1}}} '
                f'\\left({_fmt(inv["polynomial"])}\\right){end}'
            )
        lines.append(r'\end{align*}')
        lines.append('')

    lines.append(r'\end{document}')

    outpath.write_text("\n".join(lines))
    print(f"  Written: {outpath}")

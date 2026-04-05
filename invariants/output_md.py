"""
output_md.py
Human-readable Markdown output for invariant polynomials.
Strips parentheses from substituted polynomials for clean display.
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path


def _fmt(polynomial: str) -> str:
    """Strip parentheses — display mode needs no explicit multiply separator."""
    return polynomial.replace('(', '').replace(')', '')


def write_md(
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

    lines = []
    lines.append("# Invariant Polynomials")
    lines.append("")
    lines.append(f"**Space group:** {parent}  ")
    lines.append(f"**Irreps:** {', '.join(irreps)}  ")
    lines.append(f"**Degree:** {deg_str}  ")
    lines.append(f"**Total invariants:** {len(invariants)}  ")
    lines.append("")

    lines.append("## Variable Map")
    lines.append("")
    lines.append("| iso name | display name | magnetic |")
    lines.append("|----------|--------------|----------|")
    for iso_name, info in var_map.items():
        mag = "yes" if info["magnetic"] else "no"
        lines.append(f"| `{iso_name}` | `{info['display']}` | {mag} |")
    lines.append("")

    lines.append("## Invariants")
    lines.append("")
    degrees_seen = sorted(set(inv["degree"] for inv in invariants))
    idx = 1
    for deg in degrees_seen:
        deg_invs = [inv for inv in invariants if inv["degree"] == deg]
        lines.append(f"### Degree {deg}")
        lines.append("")
        for inv in deg_invs:
            lines.append(f"{idx}. `{_fmt(inv['polynomial'])}`")
            idx += 1
        lines.append("")

    if collapsed:
        lines.append("## Collapsed Free Energy")
        lines.append("")
        f_terms = " + ".join(
            f"{coeff_style}{i+1} * ({_fmt(inv['polynomial'])})"
            for i, inv in enumerate(collapsed)
        )
        lines.append(f"F = {f_terms}")
        lines.append("")
        lines.append("### Coefficients")
        lines.append("")
        for i, inv in enumerate(collapsed):
            lines.append(f"- `{coeff_style}{i+1}`: deg {inv['degree']}, `{_fmt(inv['polynomial'])}`")
        lines.append("")

    outpath.write_text("\n".join(lines))
    print(f"  Written: {outpath}")

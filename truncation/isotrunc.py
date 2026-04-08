#!/usr/bin/env python3
"""
isotrunc.py
Truncates invariant polynomials from isoinv.py or isocond.py output by applying
per-group power limits to the dynamic variables.

For each truncation group VAR1,VAR2,...:N, any monomial where the combined power
of the listed variables exceeds N is dropped. A monomial is dropped if it violates
ANY group's limit. An invariant is dropped entirely if all its monomials are dropped.
Surviving invariants are re-indexed and F is rebuilt.

Usage:
    python isotrunc.py \
        --indir PATH \
        --infile invariants_collapsed.py \
        --truncate Ex,Ey,Qx,Qy:2 Mx,My:2 epsilon:4 \
        [--label NAME] \
        [--formats md py nb tex]

The --indir should point to the directory containing --infile.
Output files are written back into the same directory.
"""

import argparse
import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

try:
    import sympy as sp
except ImportError:
    print("Error: sympy is required. Install with: pip install sympy", file=sys.stderr)
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(
        description="Truncate invariant polynomials by per-group power limits."
    )
    p.add_argument("--indir", required=True,
                   help="Directory containing the input .py file")
    p.add_argument("--infile", required=True,
                   help="Input .py file (from isoinv.py or isocond.py)")
    p.add_argument("--truncate", nargs="+", required=True,
                   help=("Truncation rules. Format: VAR1,VAR2,...:N "
                         "e.g. Ex,Ey,Qx,Qy:2 Mx,My:2 epsilon:4 "
                         "A monomial is dropped if it violates ANY rule. "
                         "Variables can appear in multiple rules."))
    p.add_argument("--label", default=None,
                   help="Custom output filename suffix (default: 'trunc')")
    p.add_argument("--formats", nargs="+",
                   choices=["md", "py", "nb", "tex"],
                   default=["md", "py", "nb", "tex"],
                   help="Output formats to generate (default: all)")
    return p.parse_args()


def parse_truncations(truncate_args: List[str]) -> List[Tuple[List[str], int]]:
    """
    Parse --truncate arguments into (variable_list, max_power) pairs.
    e.g. ['Ex,Ey,Qx,Qy:2', 'Mx,My:2'] -> [(['Ex','Ey','Qx','Qy'], 2), (['Mx','My'], 2)]
    """
    result = []
    for arg in truncate_args:
        if ":" not in arg:
            print(f"Error: --truncate entries must be VAR1,VAR2,...:N. Got: {arg}",
                  file=sys.stderr)
            sys.exit(1)
        vars_str, n_str = arg.rsplit(":", 1)
        try:
            n = int(n_str)
        except ValueError:
            print(f"Error: power limit must be an integer. Got: {n_str}", file=sys.stderr)
            sys.exit(1)
        variables = [v.strip() for v in vars_str.split(",")]
        result.append((variables, n))
    return result


def load_py(indir: Path, infile: str) -> dict:
    """Load a .py file from isoinv.py or isocond.py and exec it."""
    py_path = indir / infile
    if not py_path.exists():
        print(f"Error: {py_path} not found.", file=sys.stderr)
        sys.exit(1)
    namespace = {}
    exec(compile(py_path.read_text(), str(py_path), "exec"), namespace)
    return namespace


def monomial_group_power(monomial: sp.Expr, variables: List[sp.Symbol]) -> int:
    """Return the total power of the given variables in a monomial."""
    total = 0
    for var in variables:
        total += sp.Poly(monomial, var).degree() if monomial.has(var) else 0
    return total


def truncate_invariants(
    invariants: List[dict],
    truncations: List[Tuple[List[str], int]],
    namespace: dict,
    coeff_style: str = "c",
) -> List[dict]:
    """
    Apply truncation rules to a list of invariant dicts.
    Each invariant dict has 'polynomial' (sympy expr), 'coefficient', 'degree', 'index'.

    For each invariant, split into monomials and drop those violating any rule.
    Drop the invariant entirely if no monomials survive.
    Re-index survivors.
    """
    # resolve variable names to sympy symbols
    resolved = []
    for var_names, max_power in truncations:
        syms = []
        for name in var_names:
            if name in namespace and isinstance(namespace[name], sp.Symbol):
                syms.append(namespace[name])
            else:
                # try to find it as a sympy symbol
                syms.append(sp.Symbol(name))
        resolved.append((syms, max_power))

    result = []
    for inv in invariants:
        poly = inv['polynomial']

        # split polynomial into additive terms
        terms = sp.Add.make_args(poly)

        surviving = []
        for term in terms:
            keep = True
            for syms, max_power in resolved:
                group_power = sum(
                    int(term.as_powers_dict().get(s, 0)) for s in syms
                )
                if group_power > max_power:
                    keep = False
                    break
            if keep:
                surviving.append(term)

        if surviving:
            new_poly = sp.Add(*surviving) if len(surviving) > 1 else surviving[0]
            new_inv = dict(inv)
            new_inv['polynomial'] = new_poly
            result.append(new_inv)

    # re-index
    for i, inv in enumerate(result, 1):
        inv['index'] = i
        inv['coeff_name'] = f"{coeff_style}{i}"

    return result


def make_output_stem(infile: str, label: Optional[str]) -> str:
    """Build output stem from input filename and label."""
    stem = Path(infile).stem  # strip .py
    suffix = label if label else "trunc"
    return f"{stem}_{suffix}"


def write_md(outpath, indir, infile, truncations, invariants, namespace):
    """Write markdown output."""
    trunc_str = ", ".join(
        f"`{','.join(vars_)}` ≤ {n}" for vars_, n in truncations
    )

    lines = [
        "# Truncated Invariant Polynomials\n",
        f"**Source:** `{indir / infile}`  ",
        f"**Truncation rules:** {trunc_str}  ",
        f"**Surviving invariants:** {len(invariants)}",
        "",
        "## Invariants",
        "",
    ]

    by_degree = defaultdict(list)
    for inv in invariants:
        by_degree[inv['degree']].append(inv)

    for deg in sorted(by_degree.keys()):
        lines.append(f"### Degree {deg}")
        lines.append("")
        for inv in by_degree[deg]:
            poly_str = str(inv['polynomial']).replace('**', '^').replace('*', '')
            lines.append(f"{inv['index']}. `{poly_str}`")
        lines.append("")

    lines += ["## Free Energy", ""]
    terms = " + ".join(
        f"{inv['coeff_name']} * ({str(inv['polynomial']).replace('**','^').replace('*','')})"
        for inv in invariants
    )
    lines.append(f"F = {terms}")
    lines.append("")

    lines += ["## Coefficients", ""]
    for inv in invariants:
        lines.append(f"- `{inv['coeff_name']}` = `{inv['coefficient']}`")

    outpath.write_text("\n".join(lines) + "\n")
    print(f"  Written: {outpath}")


def write_py(outpath, indir, infile, truncations, invariants, namespace):
    """Write sympy-compatible Python output."""
    trunc_str = ", ".join(f"{','.join(v)}:{n}" for v, n in truncations)

    # collect symbol names from namespace
    all_sym_names = sorted([
        k for k, v in namespace.items()
        if isinstance(v, sp.Symbol) and not k.startswith('__')
    ], key=lambda x: (len(x), x))
    coeff_names = [inv['coeff_name'] for inv in invariants]

    lines = [
        '"""',
        f'Truncated invariant polynomials',
        f'Source: {indir / infile}',
        f'Truncation: {trunc_str}',
        f'Generated by isotrunc',
        '"""',
        '',
        'import sympy as sp',
        '',
        '# Symbol declarations',
        f'{", ".join(all_sym_names)} = sp.symbols("{" ".join(all_sym_names)}")',
        '',
        '# Coefficients',
    ]
    for inv in invariants:
        lines.append(f"{inv['coeff_name']} = {inv['coefficient']}")

    lines += ['', '# Invariants', 'invariants = [']
    for inv in invariants:
        lines.append(f"    {sp.pycode(inv['polynomial'])},  # deg {inv['degree']}")
    lines += [']', '', '# Free energy', 'F = (']
    for i, inv in enumerate(invariants):
        sep = ' +' if i < len(invariants) - 1 else ''
        lines.append(f"    {inv['coeff_name']} * ({sp.pycode(inv['polynomial'])}){sep}")
    lines += [')', '']

    outpath.write_text("\n".join(lines) + "\n")
    print(f"  Written: {outpath}")


def write_nb(outpath, indir, infile, truncations, invariants, namespace):
    """Write Mathematica notebook output."""
    trunc_str = ", ".join(f"{','.join(v)}:{n}" for v, n in truncations)

    all_sym_names = sorted([
        k for k, v in namespace.items()
        if isinstance(v, sp.Symbol) and not k.startswith('__')
    ], key=lambda x: (len(x), x))

    def to_nb(expr):
        return sp.mathematica_code(expr)

    lines = [
        '(* Content-type: application/vnd.wolfram.mathematica *)',
        '',
        'Notebook[{',
        f'Cell[TextData[{{"Truncated Invariant Polynomials\\nSource: {indir / infile}\\nTruncation: {trunc_str}"}}], "Title"],',
        '',
        f'Cell[BoxData["{{{", ".join(all_sym_names)}}}"], "Input"],',
        '',
        'Cell[BoxData["',
    ]
    for inv in invariants:
        lines.append(f'{inv["coeff_name"]} = {to_nb(inv["coefficient"])}')
    lines += ['"], "Input"],', '']
    lines += ['Cell[BoxData["invariants = {']
    for inv in invariants:
        lines.append(f'  {to_nb(inv["polynomial"])},  (* deg {inv["degree"]} *)')
    lines += ['};"], "Input"],', '']
    lines += ['Cell[BoxData["F = (']
    for i, inv in enumerate(invariants):
        sep = ' +' if i < len(invariants) - 1 else ''
        lines.append(f'  {inv["coeff_name"]} * ({to_nb(inv["polynomial"])}){sep}')
    lines += [');"], "Input"]', '', '}, WindowSize->{1200, 800}]']

    outpath.write_text('\n'.join(lines) + '\n')
    print(f"  Written: {outpath}")


def write_tex(outpath, indir, infile, truncations, invariants, namespace):
    """Write LaTeX output."""
    from collections import defaultdict as ddict

    trunc_str = ", ".join(
        f"${''.join(sp.latex(sp.Symbol(v)) + '+' for v in vars_)[:-1]} \\leq {n}$"
        for vars_, n in truncations
    )

    lines = [
        r'\documentclass{article}',
        r'\usepackage{amsmath}',
        r'\usepackage{booktabs}',
        r'\begin{document}',
        '',
        r'\section*{Truncated Invariant Polynomials}',
        '',
        r'\begin{tabular}{ll}',
        r'\toprule',
        f'Source & \\texttt{{{indir / infile}}} \\\\',
        f'Truncation & {trunc_str} \\\\',
        f'Surviving invariants & {len(invariants)} \\\\',
        r'\bottomrule',
        r'\end{tabular}',
        '',
        r'\subsection*{Invariants}',
        '',
        r'\begin{align*}',
    ]

    by_degree = ddict(list)
    for inv in invariants:
        by_degree[inv['degree']].append(inv)

    for deg in sorted(by_degree.keys()):
        for inv in by_degree[deg]:
            lines.append(f'I_{{{inv["index"]}}} &= {sp.latex(inv["polynomial"])} \\\\')

    lines += [r'\end{align*}', '']
    lines += [
        r'\subsection*{Free Energy}',
        '',
        r'\begin{align*}',
        r'F &= \\',
    ]
    for i, inv in enumerate(invariants):
        sep = r' \\' if i < len(invariants) - 1 else ''
        coeff_latex = sp.latex(sp.Symbol(inv['coeff_name']))
        lines.append(f'&\\quad {coeff_latex} \\left({sp.latex(inv["polynomial"])}\\right){sep}')
    lines += [r'\end{align*}', '']

    lines += [r'\subsection*{Coefficients}', '', r'\begin{align*}']
    for inv in invariants:
        coeff_latex = sp.latex(sp.Symbol(inv['coeff_name']))
        lines.append(f'{coeff_latex} &= {sp.latex(inv["coefficient"])} \\\\')
    lines += [r'\end{align*}', '', r'\end{document}']

    outpath.write_text('\n'.join(lines) + '\n')
    print(f"  Written: {outpath}")


def main():
    args = parse_args()
    indir = Path(args.indir)
    truncations = parse_truncations(args.truncate)

    if not indir.exists():
        print(f"Error: --indir '{indir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {indir / args.infile}...")
    namespace = load_py(indir, args.infile)

    if 'invariants' not in namespace or 'F' not in namespace:
        print("Error: 'invariants' and 'F' must be present in the input file.",
              file=sys.stderr)
        sys.exit(1)

    # build invariant dicts from the loaded namespace
    raw_invariants = namespace['invariants']

    # detect coeff style from namespace
    coeff_names = sorted([
        k for k in namespace if re.match(r'^[a-zA-Z]+\d+$', k)
        and isinstance(namespace[k], sp.Symbol)
    ], key=lambda x: (len(x), x))
    coeff_style = re.match(r'^([a-zA-Z]+)', coeff_names[0]).group(1) if coeff_names else 'c'

    # reconstruct invariant dicts
    inv_dicts = []
    for i, poly in enumerate(raw_invariants, 1):
        coeff_name = f"{coeff_style}{i}"
        coeff = namespace.get(coeff_name, sp.Symbol(coeff_name))
        # degree = total degree in all free symbols except coefficients and statics
        deg = sp.Poly(poly, *poly.free_symbols).total_degree() if poly.free_symbols else 0
        inv_dicts.append({
            'index': i,
            'degree': deg,
            'polynomial': poly,
            'coefficient': coeff,
            'coeff_name': coeff_name,
        })

    print(f"Loaded {len(inv_dicts)} invariant(s).")
    print(f"Applying truncation rules:")
    for vars_, n in truncations:
        print(f"  {{{', '.join(vars_)}}} combined power <= {n}")

    truncated = truncate_invariants(inv_dicts, truncations, namespace, coeff_style)
    n_removed = len(inv_dicts) - len(truncated)
    print(f"  {len(truncated)} invariant(s) survive ({n_removed} removed).")

    stem = make_output_stem(args.infile, args.label)
    print(f"\nWriting output to {indir}/")

    writers = {
        "md": write_md,
        "py": write_py,
        "nb": write_nb,
        "tex": write_tex,
    }

    for fmt in args.formats:
        writers[fmt](
            outpath=indir / f"{stem}.{fmt}",
            indir=indir,
            infile=args.infile,
            truncations=truncations,
            invariants=truncated,
            namespace=namespace,
        )

    print("\nDone.")


if __name__ == "__main__":
    main()

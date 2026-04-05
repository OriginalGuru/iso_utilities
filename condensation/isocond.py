#!/usr/bin/env python3
"""
isocond.py
Condenses one or more order parameters in a collapsed free energy polynomial
produced by isoinv.py.

For each condensed variable P, substitutes P -> P0 + dP, expands, and
regroups terms by shared coefficient to identify new effective invariants.
The new coefficients (beta_i) are expressed symbolically in terms of the
original coefficients (alpha_i / c_i) and the static values (P0).

Usage:
    python isocond.py --indir PATH --condense Pz:Pz0 [Mz:Mz0 ...] [--formats md py nb tex]

The --indir should point to an isoinv.py output directory containing
invariants_collapsed.py. Output files are written back into the same directory.
"""

import argparse
import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

try:
    import sympy as sp
except ImportError:
    print("Error: sympy is required. Install with: pip install sympy", file=sys.stderr)
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(
        description="Condense order parameters in an isoinv.py collapsed free energy."
    )
    p.add_argument("--indir", required=True,
                   help="isoinv.py output directory containing invariants_collapsed.py")
    p.add_argument("--condense", nargs="+", required=True,
                   help="Variables to condense. Format: VAR:VAR0 e.g. Pz:Pz0 or Pz:Pz0 Mz:Mz0")
    p.add_argument("--formats", nargs="+",
                   choices=["md", "py", "nb", "tex"],
                   default=["md", "py", "nb", "tex"],
                   help="Output formats to generate (default: all)")
    p.add_argument("--max-degree", type=int, default=None,
                   help="Truncate output to invariants with total dynamic degree <= this value. "
                        "Applied after condensation so renormalized coefficients are exact.")
    p.add_argument("--linear-static", action="store_true",
                   help="Linearize each coefficient in the static (condensed) variables, "
                        "keeping only zeroth and first order terms. Useful when condensed "
                        "OP values are small. Invariants whose coefficients vanish at this "
                        "order are dropped.")
    return p.parse_args()


def parse_condense(condense_args: List[str]) -> List[Tuple[str, str]]:
    """Parse --condense arguments into (var_name, static_name) pairs."""
    result = []
    for arg in condense_args:
        if ":" not in arg:
            print(f"Error: --condense entries must be VAR:VAR0. Got: {arg}", file=sys.stderr)
            sys.exit(1)
        var, static = arg.split(":", 1)
        result.append((var.strip(), static.strip()))
    return result


def load_collapsed_py(indir: Path) -> dict:
    """
    Load invariants_collapsed.py from the indir and exec it to get
    the sympy namespace including F, invariants, and all symbols.
    Returns the namespace dict.
    """
    py_path = indir / "invariants_collapsed.py"
    if not py_path.exists():
        print(f"Error: {py_path} not found.", file=sys.stderr)
        sys.exit(1)

    namespace = {}
    exec(compile(py_path.read_text(), str(py_path), "exec"), namespace)
    return namespace


def condense(
    F: sp.Expr,
    condensations: List[Tuple[str, str]],
    namespace: dict,
) -> Tuple[sp.Expr, List[sp.Symbol], List[sp.Symbol], dict]:
    """
    Perform the condensation substitutions on F.

    For each (var_name, static_name) pair:
      - Declare static_name and d{var_name} as new symbols
      - Substitute var_name -> static_name + d{var_name} in F
      - Expand

    Returns:
        F_cond:        expanded condensed free energy
        dynamic_vars:  list of sympy symbols for dynamic variables
        static_syms:   list of new static symbols (P0 values)
        dvar_map:      dict mapping original var name -> (static_sym, delta_sym)
    """
    F_cond = F
    dvar_map = {}
    static_syms = []
    delta_syms = []

    for var_name, static_name in condensations:
        if var_name not in namespace:
            print(f"Error: variable '{var_name}' not found in collapsed polynomial.",
                  file=sys.stderr)
            sys.exit(1)
        orig_sym = namespace[var_name]
        static_sym = sp.Symbol(static_name)
        delta_sym = sp.Symbol(f"d{var_name}")
        F_cond = F_cond.subs(orig_sym, static_sym + delta_sym)
        dvar_map[var_name] = (static_sym, delta_sym)
        static_syms.append(static_sym)
        delta_syms.append(delta_sym)

    F_cond = sp.expand(F_cond)

    # dynamic variables: all original order parameter symbols except condensed ones,
    # plus the delta symbols
    condensed_names = {v for v, _ in condensations}
    orig_vars = [v for k, v in namespace.items()
                 if isinstance(v, sp.Symbol)
                 and not k.startswith('_')
                 and not k.startswith('alpha')
                 and not k.startswith('c')
                 and k not in condensed_names
                 and k not in {s.name for s in static_syms}
                 and k not in {s.name for s in delta_syms}
                 and k in str(F)]

    dynamic_vars = delta_syms + orig_vars
    return F_cond, dynamic_vars, static_syms, dvar_map


def group_invariants(
    F_cond: sp.Expr,
    dynamic_vars: List[sp.Symbol],
    coeff_style: str = "beta",
) -> List[dict]:
    """
    Group monomials in dynamic_vars by shared coefficient to identify
    new effective invariants. Returns list of dicts:
        {
            'index': int,
            'degree': int,
            'polynomial': sympy expr (sum of monomials),
            'coefficient': sympy expr (the shared coefficient),
            'coeff_name': str (e.g. 'beta1'),
        }
    """
    try:
        p = sp.Poly(F_cond, *dynamic_vars)
    except sp.PolynomialError as e:
        print(f"Error building polynomial: {e}", file=sys.stderr)
        sys.exit(1)

    # Group monomials by their primitive base coefficient.
    # sp.primitive(coeff) returns (rational_content, primitive_part) such that
    # coeff = rational_content * primitive_part.
    # Monomials with the same primitive_part belong to the same invariant.
    coeff_to_terms = defaultdict(list)
    for monom, coeff in zip(p.monoms(), p.coeffs()):
        _, primitive = sp.primitive(coeff)
        key = str(sp.factor(primitive))
        coeff_to_terms[key].append((monom, coeff))

    # sort by (degree, coeff_key) for stable ordering
    def sort_key(item):
        terms = item[1]
        deg = sum(terms[0][0])
        return (deg, item[0])

    invariants = []
    for i, (coeff_key, terms) in enumerate(
        sorted(coeff_to_terms.items(), key=sort_key), 1
    ):
        coeff = sp.factor(terms[0][1])
        deg = sum(terms[0][0])

        # reconstruct polynomial expression
        poly_expr = sp.Integer(0)
        for monom, c in terms:
            term = sp.Integer(1)
            for var, exp in zip(dynamic_vars, monom):
                term *= var ** exp
            prefactor = sp.simplify(c / coeff)
            poly_expr += prefactor * term

        invariants.append({
            'index': i,
            'degree': deg,
            'polynomial': poly_expr,
            'coefficient': coeff,
            'coeff_name': f"{coeff_style}{i}",
        })

    return invariants


def make_output_stem(condensations: List[Tuple[str, str]]) -> str:
    """Build output filename stem from condensed variable names."""
    parts = [v for v, _ in condensations]
    return "invariants_condensed_" + "_".join(parts)


def write_md(
    outpath: Path,
    indir: Path,
    condensations: List[Tuple[str, str]],
    static_syms: List[sp.Symbol],
    dynamic_vars: List[sp.Symbol],
    invariants: List[dict],
    original_invariants: list,
    original_coeffs: list,
):
    """Write markdown output."""
    cond_str = ", ".join(f"{v} → {s}+d{v}" for v, s in condensations)
    lines = [
        "# Condensed Invariant Polynomials\n",
        f"**Source:** `{indir}`  ",
        f"**Condensation:** {cond_str}  ",
        f"**Static variables:** {', '.join(f'`{s}`' for s in static_syms)}  ",
        f"**Dynamic variables:** {', '.join(f'`{v}`' for v in dynamic_vars)}  ",
        f"**New invariants:** {len(invariants)}",
        "",
        "## New Invariants",
        "",
    ]

    # group by degree
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

    lines += [
        "## Collapsed Condensed Free Energy",
        "",
    ]
    terms = " + ".join(
        f"{inv['coeff_name']} * ({str(inv['polynomial']).replace('**','^').replace('*','')})"
        for inv in invariants
    )
    lines.append(f"F = {terms}")
    lines.append("")

    lines += [
        "## Coefficient Mapping",
        "",
        "New coefficients expressed in terms of original coefficients and static values:",
        "",
    ]
    for inv in invariants:
        lines.append(f"- `{inv['coeff_name']}` = `{inv['coefficient']}`")

    outpath.write_text("\n".join(lines) + "\n")
    print(f"  Written: {outpath}")


def write_py(
    outpath: Path,
    indir: Path,
    condensations: List[Tuple[str, str]],
    static_syms: List[sp.Symbol],
    dynamic_vars: List[sp.Symbol],
    invariants: List[dict],
    namespace: dict,
):
    """Write sympy-compatible Python output."""
    cond_str = ", ".join(f"{v} -> {s}+d{v}" for v, s in condensations)

    # collect all symbol names needed
    static_names = [s.name for s in static_syms]
    dynamic_names = [v.name for v in dynamic_vars]
    coeff_names = [inv['coeff_name'] for inv in invariants]

    # original coeff symbols from namespace
    orig_coeff_names = sorted([
        k for k, v in namespace.items()
        if isinstance(v, sp.Symbol) and (k.startswith('alpha') or k.startswith('c'))
        and not k.startswith('__')
    ], key=lambda x: (len(x), x))

    lines = [
        f'"""',
        f'Condensed invariant polynomials',
        f'Source: {indir}',
        f'Condensation: {cond_str}',
        f'Generated by isocond',
        f'"""',
        '',
        'import sympy as sp',
        '',
        '# Original coefficient symbols',
        f'{", ".join(orig_coeff_names)} = sp.symbols("{" ".join(orig_coeff_names)}")',
        '',
        '# Static (condensed) variable symbols',
        f'{", ".join(static_names)} = sp.symbols("{" ".join(static_names)}")',
        '',
        '# Dynamic variable symbols',
        f'{", ".join(dynamic_names)} = sp.symbols("{" ".join(dynamic_names)}")',
        '',
        '# New effective coefficients',
    ]

    for inv in invariants:
        lines.append(f"{inv['coeff_name']} = {inv['coefficient']}")

    lines += [
        '',
        '# New invariants',
        'invariants = [',
    ]
    for inv in invariants:
        poly_str = sp.pycode(inv['polynomial'])
        lines.append(f"    {poly_str},  # deg {inv['degree']}")
    lines += [
        ']',
        '',
        '# Condensed free energy',
        'F = (',
    ]
    for i, inv in enumerate(invariants):
        sep = ' +' if i < len(invariants) - 1 else ''
        lines.append(f"    {inv['coeff_name']} * ({sp.pycode(inv['polynomial'])}){sep}")
    lines += [')', '']

    outpath.write_text("\n".join(lines) + "\n")
    print(f"  Written: {outpath}")


def write_nb(
    outpath,
    indir,
    condensations,
    static_syms,
    dynamic_vars,
    invariants,
    namespace,
):
    """Write Mathematica notebook output."""
    cond_str = ", ".join(f"{v} -> {s}+d{v}" for v, s in condensations)

    orig_coeff_names = sorted([
        k for k, v in namespace.items()
        if isinstance(v, sp.Symbol) and (k.startswith('alpha') or k.startswith('c'))
        and not k.startswith('__')
    ], key=lambda x: (len(x), x))

    static_names = [s.name for s in static_syms]
    dynamic_names = [v.name for v in dynamic_vars]

    def to_nb(expr):
        return sp.mathematica_code(expr)

    lines = [
        '(* Content-type: application/vnd.wolfram.mathematica *)',
        '',
        'Notebook[{',
        f'Cell[TextData[{{"Condensed Invariant Polynomials\\nSource: {indir}\\nCondensation: {cond_str}"}}], "Title"],',
        '',
        f'Cell[BoxData["{{{", ".join(dynamic_names + static_names)}}}"], "Input"],',
        '',
        'Cell[BoxData["',
    ]
    coeff_lines = []
    for inv in invariants:
        coeff_lines.append(f'{inv["coeff_name"]} = {to_nb(inv["coefficient"])}')
    lines.append('\n'.join(coeff_lines))
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


def write_tex(
    outpath,
    indir,
    condensations,
    static_syms,
    dynamic_vars,
    invariants,
    namespace,
):
    """Write LaTeX output."""
    from collections import defaultdict as ddict

    cond_str = ", ".join(
        f"${sp.latex(sp.Symbol(v))} \\to {sp.latex(sp.Symbol(s))} + {sp.latex(sp.Symbol('d'+v))}$"
        for v, s in condensations
    )
    static_latex = ", ".join(f"${sp.latex(s)}$" for s in static_syms)
    dynamic_latex = ", ".join(f"${sp.latex(v)}$" for v in dynamic_vars)

    orig_coeff_names = sorted([
        k for k, v in namespace.items()
        if isinstance(v, sp.Symbol) and (k.startswith('alpha') or k.startswith('c'))
        and not k.startswith('__')
    ], key=lambda x: (len(x), x))

    lines = [
        r'\documentclass{article}',
        r'\usepackage{amsmath}',
        r'\usepackage{booktabs}',
        r'\begin{document}',
        '',
        r'\section*{Condensed Invariant Polynomials}',
        '',
        r'\begin{tabular}{ll}',
        r'\toprule',
        f'Source & \\texttt{{{indir}}} \\\\',
        f'Condensation & {cond_str} \\\\',
        f'Static variables & {static_latex} \\\\',
        f'Dynamic variables & {dynamic_latex} \\\\',
        f'New invariants & {len(invariants)} \\\\',
        r'\bottomrule',
        r'\end{tabular}',
        '',
        r'\subsection*{New Invariants}',
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
        r'\subsection*{Condensed Free Energy}',
        '',
        r'\begin{align*}',
        r'F &= \\',
    ]
    for i, inv in enumerate(invariants):
        sep = r' \\' if i < len(invariants) - 1 else ''
        coeff_latex = sp.latex(sp.Symbol(inv['coeff_name']))
        lines.append(f'&\\quad {coeff_latex} \\left({sp.latex(inv["polynomial"])}\\right){sep}')
    lines += [r'\end{align*}', '']

    lines += [
        r'\subsection*{Coefficient Mapping}',
        '',
        r'\begin{align*}',
    ]
    for inv in invariants:
        coeff_latex = sp.latex(sp.Symbol(inv['coeff_name']))
        lines.append(f'{coeff_latex} &= {sp.latex(inv["coefficient"])} \\\\')
    lines += [r'\end{align*}', '', r'\end{document}']

    outpath.write_text('\n'.join(lines) + '\n')
    print(f"  Written: {outpath}")

def main():
    args = parse_args()
    condensations = parse_condense(args.condense)
    indir = Path(args.indir)

    if not indir.exists():
        print(f"Error: --indir '{indir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {indir / 'invariants_collapsed.py'}...")
    namespace = load_collapsed_py(indir)

    if 'F' not in namespace:
        print("Error: 'F' not found in collapsed polynomial file.", file=sys.stderr)
        sys.exit(1)

    F = namespace['F']

    # get coeff_style from existing coefficient names
    coeff_names = [k for k in namespace if re.match(r'^[a-zA-Z]+\d+$', k)
                   and isinstance(namespace[k], sp.Symbol)]
    coeff_style = re.match(r'^([a-zA-Z]+)', coeff_names[0]).group(1) if coeff_names else 'c'
    # use beta for new coefficients
    new_coeff_style = "beta"

    print(f"Condensing: {', '.join(f'{v} → {s}+d{v}' for v, s in condensations)}")
    F_cond, dynamic_vars, static_syms, dvar_map = condense(F, condensations, namespace)

    print(f"Grouping new invariants...")
    invariants = group_invariants(F_cond, dynamic_vars, coeff_style=new_coeff_style)
    print(f"  Found {len(invariants)} new invariant group(s).")

    if args.max_degree is not None:
        n_before = len(invariants)
        invariants = [inv for inv in invariants if inv['degree'] <= args.max_degree]
        # re-index after truncation
        for i, inv in enumerate(invariants, 1):
            inv['index'] = i
            inv['coeff_name'] = f"{new_coeff_style}{i}"
        print(f"  Truncated to degree <= {args.max_degree}: {len(invariants)} invariant(s) "
              f"({n_before - len(invariants)} removed).")

    if args.linear_static:
        n_before = len(invariants)
        linearized = []
        for inv in invariants:
            # expand coefficient to first order in each static symbol
            coeff = inv['coefficient']
            for sym in static_syms:
                # zeroth + first order: f(0) + f'(0)*sym
                c0 = coeff.subs(sym, 0)
                c1 = sp.diff(coeff, sym).subs(sym, 0)
                coeff = c0 + c1 * sym
            coeff = sp.expand(coeff)
            if coeff != 0:
                inv = dict(inv)
                inv['coefficient'] = coeff
                linearized.append(inv)
        # re-index
        for i, inv in enumerate(linearized, 1):
            inv['index'] = i
            inv['coeff_name'] = f"{new_coeff_style}{i}"
        invariants = linearized
        print(f"  Linearized in static variables: {len(invariants)} invariant(s) "
              f"({n_before - len(invariants)} removed).")

    # build output filename stem
    stem = make_output_stem(condensations)
    if args.max_degree is not None:
        stem += f"_deg{args.max_degree}"
    if args.linear_static:
        stem += "_linear"
    print(f"\nWriting output to {indir}/")

    if "md" in args.formats:
        write_md(
            outpath=indir / f"{stem}.md",
            indir=indir,
            condensations=condensations,
            static_syms=static_syms,
            dynamic_vars=dynamic_vars,
            invariants=invariants,
            original_invariants=namespace.get('invariants', []),
            original_coeffs=coeff_names,
        )

    if "py" in args.formats:
        write_py(
            outpath=indir / f"{stem}.py",
            indir=indir,
            condensations=condensations,
            static_syms=static_syms,
            dynamic_vars=dynamic_vars,
            invariants=invariants,
            namespace=namespace,
        )

    if "nb" in args.formats:
        write_nb(
            outpath=indir / f"{stem}.nb",
            indir=indir,
            condensations=condensations,
            static_syms=static_syms,
            dynamic_vars=dynamic_vars,
            invariants=invariants,
            namespace=namespace,
        )

    if "tex" in args.formats:
        write_tex(
            outpath=indir / f"{stem}.tex",
            indir=indir,
            condensations=condensations,
            static_syms=static_syms,
            dynamic_vars=dynamic_vars,
            invariants=invariants,
            namespace=namespace,
        )

    print("\nDone.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
isoinv.py
Wrapper around the ISOTROPY software to produce invariant polynomials
with physically meaningful variable names, TRS filtering, and multiple output formats.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from runner import get_irrep_dimension, get_invariants
from parser import (
    build_variable_map,
    substitute_invariants,
    apply_trs_filter,
    _strip_magnetic,
)
from collapse import build_collapsed
from output_md import write_md
from output_py import write_py
from output_nb import write_nb
from output_tex import write_tex


def parse_args():
    p = argparse.ArgumentParser(
        description="Generate invariant polynomials using ISOTROPY with physical variable names."
    )
    p.add_argument("--parent", type=int, required=True,
                   help="Parent space group number")
    p.add_argument("--irreps", nargs="+", required=True,
                   help=(
                       "Irrep labels, optionally with variable name overrides. "
                       "Format: IRREP or IRREP:name1,name2,... "
                       "Prefix 'm' denotes magnetic irrep. "
                       "Examples: GM2- GM6-:Px,Py mA1:Mx GM4-:Ex,Ey,Ez GM4-:Px,Py,Pz"
                   ))
    p.add_argument("--degree", type=int, nargs="+", required=True,
                   help="Degree or degree range. One value: exact. Two values: min max.")
    p.add_argument("--iso-exec", default="iso",
                   help="Path to iso executable (default: 'iso', assumed on PATH)")
    p.add_argument("--formats", nargs="+",
                   choices=["md", "py", "nb", "tex"],
                   default=["md", "py", "nb", "tex"],
                   help="Output formats to generate (default: all)")
    p.add_argument("--collapse", action="store_true",
                   help="Also produce collapsed single-polynomial output with named coefficients")
    p.add_argument("--coeff-style", default="c",
                   help="Coefficient prefix for collapsed polynomial (default: 'c' -> c1, c2, ...)")
    p.add_argument("--outdir", default=None,
                   help="Output directory (default: sg{N}__{irreps}__{deg}/)")
    p.add_argument("--debug", action="store_true",
                   help="Save iso.log from each iso call into the output directory")
    p.add_argument("--debug-only", action="store_true",
                   help="Save iso.log files but skip all output file writing")
    return p.parse_args()


def parse_irreps(irrep_args: List[str]) -> Tuple[List[str], Optional[Dict[str, List[str]]]]:
    """
    Parse --irreps arguments which may contain optional name overrides.

    Each argument is either:
      - 'GM2-'           -> irrep label only, use default naming
      - 'GM6-:Px,Py'     -> irrep label with name overrides

    For duplicate irrep labels, names are assigned positionally:
      'GM4-:Ex,Ey,Ez GM4-:Px,Py,Pz' -> GM4-[1] gets Ex,Ey,Ez; GM4-[2] gets Px,Py,Pz

    Returns:
        (irreps, user_names) where irreps is a plain list of labels (no colons)
        and user_names is a dict mapping positional keys to name lists,
        or None if no overrides were given.
    """
    irreps = []
    raw_names = {}  # label -> list of name lists in order of appearance
    has_any_names = False

    for arg in irrep_args:
        if ":" in arg:
            label, names_str = arg.split(":", 1)
            names = names_str.split(",")
            has_any_names = True
        else:
            label = arg
            names = None

        irreps.append(label)

        if label not in raw_names:
            raw_names[label] = []
        raw_names[label].append(names)

    if not has_any_names:
        return irreps, None

    # build positional user_names dict
    # track occurrence index per label
    occurrence: Dict[str, int] = {}
    user_names: Dict[str, List[str]] = {}

    for arg in irrep_args:
        if ":" in arg:
            label, names_str = arg.split(":", 1)
        else:
            label = arg

        occurrence[label] = occurrence.get(label, 0) + 1
        idx = occurrence[label]

        # check if this label appears more than once total
        total = len(raw_names[label])
        if total > 1:
            key = f"{label}[{idx}]"
        else:
            key = label

        if ":" in arg:
            user_names[key] = arg.split(":", 1)[1].split(",")

    return irreps, user_names if user_names else None


def parse_degree(degree_args: List[int]) -> Tuple[int, int]:
    if len(degree_args) == 1:
        return (degree_args[0], degree_args[0])
    elif len(degree_args) == 2:
        return (degree_args[0], degree_args[1])
    else:
        print("Error: --degree takes one or two integers.", file=sys.stderr)
        sys.exit(1)


def make_stem(parent: int, irreps: List[str], degree: Tuple[int, int]) -> str:
    def sanitize(label: str) -> str:
        return label.replace("+", "p").replace("-", "m")
    irrep_str = "_".join(sanitize(r) for r in irreps)
    deg_lo, deg_hi = degree
    deg_str = f"deg{deg_lo}" if deg_lo == deg_hi else f"deg{deg_lo}-{deg_hi}"
    return f"sg{parent}__{irrep_str}__{deg_str}"


def main():
    args = parse_args()
    degree = parse_degree(args.degree)
    irreps, user_names = parse_irreps(args.irreps)

    # --- Set up output directory early (needed for debug paths) ---
    stem = make_stem(args.parent, irreps, degree)
    outdir = Path(args.outdir) if args.outdir else Path(stem)
    outdir.mkdir(parents=True, exist_ok=True)

    # --- Step 1: dimension queries ---
    stripped_irreps = []
    seen = {}
    for irrep in irreps:
        _, stripped = _strip_magnetic(irrep)
        if stripped not in seen:
            seen[stripped] = True
            stripped_irreps.append(stripped)

    print(f"Querying dimensions for {len(stripped_irreps)} irrep(s)...")
    dimensions = {}
    for irrep in stripped_irreps:
        debug_path = outdir / f"debug_dim_{irrep}.log" if args.debug else None
        dim = get_irrep_dimension(
            args.parent, irrep, iso_exec=args.iso_exec, debug_path=debug_path
        )
        dimensions[irrep] = dim
        print(f"  {irrep}: dimension {dim}")
        if args.debug:
            print(f"    (iso.log saved to {debug_path})")

    # --- Step 2: variable map ---
    var_map = build_variable_map(irreps, dimensions, user_names)
    print("\nVariable map (iso name -> display name):")
    for iso_name, info in var_map.items():
        mag_tag = " [magnetic]" if info["magnetic"] else ""
        print(f"  {iso_name} -> {info['display']}{mag_tag}")

    # --- Step 3: invariants ---
    stripped_for_iso = [_strip_magnetic(r)[1] for r in irreps]
    print(f"\nQuerying invariants (degree {degree[0]}-{degree[1]})...")
    debug_path = outdir / "debug_invariants.log" if args.debug else None
    raw_invariants = get_invariants(
        args.parent, stripped_for_iso, degree,
        iso_exec=args.iso_exec, debug_path=debug_path
    )
    print(f"  Found {len(raw_invariants)} invariant(s) before TRS filtering.")
    if args.debug:
        print(f"  (iso.log saved to {debug_path})")

    # --- Step 4: substitute (display mode for md/tex, code mode for py/nb) ---
    substituted_display = substitute_invariants(raw_invariants, var_map, mode="display")
    substituted_code = substitute_invariants(raw_invariants, var_map, mode="code")

    # --- Step 5: TRS filtering ---
    has_magnetic = any(v["magnetic"] for v in var_map.values())
    if has_magnetic:
        filtered_display = apply_trs_filter(substituted_display, var_map, mode="display")
        filtered_code = apply_trs_filter(substituted_code, var_map, mode="code")
        n_removed = len(substituted_display) - len(filtered_display)
        print(f"  TRS filtering removed {n_removed} invariant(s). {len(filtered_display)} remain.")
    else:
        filtered_display = substituted_display
        filtered_code = substituted_code
        print("  No magnetic irreps -- TRS filtering skipped.")

    # --- Step 6: optional collapse ---
    collapsed_display = None
    collapsed_code = None
    if args.collapse:
        print("\nBuilding collapsed free energy...")
        collapsed_display, dupes = build_collapsed(filtered_display, args.coeff_style)
        collapsed_code, _ = build_collapsed(filtered_code, args.coeff_style)
        if not dupes:
            print(f"  No duplicates detected. {len(collapsed_display)} terms.")

    # --- Step 7: output ---
    print(f"\nWriting output to {outdir}/")

    writers = {
        "md":  (write_md,  filtered_display, collapsed_display, ".md"),
        "py":  (write_py,  filtered_code,    collapsed_code,    ".py"),
        "nb":  (write_nb,  filtered_code,    collapsed_code,    ".nb"),
        "tex": (write_tex, filtered_display, collapsed_display, ".tex"),
    }

    file_stem = "invariants_collapsed" if args.collapse else "invariants"
    if not args.debug_only:
        for fmt in args.formats:
            writer_fn, invariants, collapsed, ext = writers[fmt]
            outpath = outdir / (file_stem + ext)
            writer_fn(
                outpath=outpath,
                parent=args.parent,
                irreps=irreps,
                degree=degree,
                var_map=var_map,
                invariants=invariants,
                collapsed=collapsed,
                coeff_style=args.coeff_style,
            )
    else:
        print("  --debug-only set -- skipping output file writing.")

    print("\nDone.")


if __name__ == "__main__":
    main()

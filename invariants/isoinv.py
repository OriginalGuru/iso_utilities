#!/usr/bin/env python3
"""
isoinv.py
Wrapper around the ISOTROPY software to produce invariant polynomials
with physically meaningful variable names, TRS filtering, and multiple output formats.

Testing entry point: runs iso calls, prints parsed + substituted invariants to stdout.
Full output module to follow once core is verified.
"""

import argparse
import sys
from runner import get_irrep_dimension, get_invariants
from parser import (
    build_variable_map,
    substitute_invariants,
    apply_trs_filter,
    _strip_magnetic,
)


def parse_args():
    p = argparse.ArgumentParser(
        description="Generate invariant polynomials using ISOTROPY with physical variable names."
    )
    p.add_argument("--parent", type=int, required=True, help="Parent space group number")
    p.add_argument(
        "--irreps", nargs="+", required=True,
        help="Irrep labels (e.g. GM2- mGM6- A1). Prefix 'm' denotes magnetic irrep."
    )
    p.add_argument(
        "--degree", type=int, nargs="+", required=True,
        help="Degree or degree range. One value: exact degree. Two values: min max."
    )
    p.add_argument(
        "--names", nargs="*", default=None,
        help=(
            "Optional variable name overrides. Format: IRREP:name1,name2,...  "
            "e.g. GM6-:Px,Py GM2-:Pz"
        )
    )
    p.add_argument(
        "--iso-exec", default="iso",
        help="Path to iso executable (default: 'iso', assumed on PATH)"
    )
    p.add_argument(
        "--formats", nargs="+",
        choices=["md", "py", "nb", "tex"],
        default=["md", "py", "nb", "tex"],
        help="Output formats to generate (default: all)"
    )
    p.add_argument(
        "--collapse", action="store_true",
        help="Also produce collapsed single-polynomial output with named coefficients"
    )
    p.add_argument(
        "--coeff-style", default="c",
        help="Coefficient prefix for collapsed polynomial (default: 'c' → c1, c2, ...)"
    )
    p.add_argument(
        "--outdir", default=None,
        help="Output directory (default: sg{N}__{irreps}__{deg}/)"
    )
    return p.parse_args()


def parse_degree(degree_args: list[int]) -> tuple[int, int]:
    if len(degree_args) == 1:
        return (degree_args[0], degree_args[0])
    elif len(degree_args) == 2:
        return (degree_args[0], degree_args[1])
    else:
        print("Error: --degree takes one or two integers.", file=sys.stderr)
        sys.exit(1)


def parse_user_names(names_args: list[str] | None) -> dict[str, list[str]] | None:
    if not names_args:
        return None
    result = {}
    for item in names_args:
        if ":" not in item:
            print(f"Error: --names entries must be in format IRREP:name1,name2,...  Got: {item}",
                  file=sys.stderr)
            sys.exit(1)
        irrep, names_str = item.split(":", 1)
        result[irrep] = names_str.split(",")
    return result


def make_outdir_name(parent: int, irreps: list[str], degree: tuple[int, int]) -> str:
    def sanitize(label: str) -> str:
        return label.replace("+", "p").replace("-", "m")
    irrep_str = "_".join(sanitize(r) for r in irreps)
    deg_lo, deg_hi = degree
    deg_str = f"deg{deg_lo}" if deg_lo == deg_hi else f"deg{deg_lo}-{deg_hi}"
    return f"sg{parent}__{irrep_str}__{deg_str}"


def make_filename_stem(parent: int, irreps: list[str], degree: tuple[int, int]) -> str:
    return make_outdir_name(parent, irreps, degree)


def main():
    args = parse_args()
    degree = parse_degree(args.degree)
    user_names = parse_user_names(args.names)

    # --- Step 1: get dimension for each unique stripped irrep ---
    stripped_irreps = []
    seen = {}
    for irrep in args.irreps:
        _, stripped = _strip_magnetic(irrep)
        if stripped not in seen:
            seen[stripped] = True
            stripped_irreps.append(stripped)

    print(f"Querying dimensions for {len(stripped_irreps)} irrep(s)...")
    dimensions = {}
    for irrep in stripped_irreps:
        dim = get_irrep_dimension(args.parent, irrep, iso_exec=args.iso_exec)
        dimensions[irrep] = dim
        print(f"  {irrep}: dimension {dim}")

    # --- Step 2: build variable map ---
    var_map = build_variable_map(args.irreps, dimensions, user_names)
    print("\nVariable map (iso name → display name):")
    for iso_name, info in var_map.items():
        mag_tag = " [magnetic]" if info["magnetic"] else ""
        print(f"  {iso_name} → {info['display']}{mag_tag}")

    # --- Step 3: get invariants ---
    stripped_for_iso = [_strip_magnetic(r)[1] for r in args.irreps]
    print(f"\nQuerying invariants (degree {degree[0]}–{degree[1]})...")
    raw_invariants = get_invariants(
        args.parent, stripped_for_iso, degree, iso_exec=args.iso_exec
    )
    print(f"  Found {len(raw_invariants)} invariant(s) before TRS filtering.")

    # --- Step 4: substitute variable names (display mode for now) ---
    substituted = substitute_invariants(raw_invariants, var_map, mode="display")

    # --- Step 5: TRS filtering ---
    has_magnetic = any(v["magnetic"] for v in var_map.values())
    if has_magnetic:
        filtered = apply_trs_filter(substituted, var_map, mode="display")
        n_removed = len(substituted) - len(filtered)
        print(f"  TRS filtering removed {n_removed} invariant(s). {len(filtered)} remain.")
    else:
        filtered = substituted
        print("  No magnetic irreps — TRS filtering skipped.")

    # --- Print results to stdout ---
    print("\n--- Invariants (display mode) ---")
    for i, inv in enumerate(filtered, 1):
        print(f"  [{i}] deg {inv['degree']}: {inv['polynomial']}")


if __name__ == "__main__":
    main()

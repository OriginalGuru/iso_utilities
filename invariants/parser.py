"""
parser.py
Builds variable name maps from irrep labels and dimensions,
applies substitution to raw iso polynomials, and handles TRS filtering.

Substitution wraps each variable token in parentheses: n1 -> (GM2m_a).
This makes implicit multiplication explicit and unambiguous for all output
modes — adjacency between tokens always appears as )( or )^N( which each
output module converts to its appropriate separator.
"""

import re
from typing import Dict, List, Optional, Set, Tuple


def _index_labels(n: int) -> List[str]:
    """Generate component labels: a, b, c, ..., z, aa, ab, ..."""
    labels = []
    i = 0
    while len(labels) < n:
        q, r = divmod(i, 26)
        label = ("" if q == 0 else chr(ord("a") + q - 1)) + chr(ord("a") + r)
        labels.append(label)
        i += 1
    return labels


def _strip_magnetic(irrep: str) -> Tuple[bool, str]:
    """Return (is_magnetic, stripped_label)."""
    if irrep.startswith("m"):
        return True, irrep[1:]
    return False, irrep


def _sanitize_for_code(label: str) -> str:
    """Replace + and - with p and m for use in Python/Mathematica variable names."""
    return label.replace("+", "p").replace("-", "m")


def build_variable_map(
    irreps: List[str],
    dimensions: Dict[str, int],
    user_names: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, dict]:
    """
    Build variable map from iso generic names (n1, n2, ...) to physical names.

    Args:
        irreps: list of irrep labels as given by user (may have 'm' prefix)
        dimensions: dict mapping stripped irrep label -> dimension (from runner)
        user_names: optional dict mapping irrep label -> list of component names
                    e.g. {'GM6-': ['Px', 'Py']}
                    For duplicate irrep labels, use positional keys like
                    'GM4-[1]', 'GM4-[2]' to target specific occurrences.

    Returns:
        dict mapping iso name (e.g. 'n1') -> {
            'display': 'GM6-_a',   # for human-readable / LaTeX output
            'code':    'GM6m_a',   # for Python / Mathematica output
            'irrep':   'GM6-',     # stripped irrep label
            'magnetic': bool,      # whether this irrep had 'm' prefix
            'component': 'a',      # component label
        }
    """
    # count occurrences of each irrep label to detect duplicates
    irrep_counts: Dict[str, int] = {}
    for irrep in irreps:
        irrep_counts[irrep] = irrep_counts.get(irrep, 0) + 1
    duplicated = {label for label, count in irrep_counts.items() if count > 1}

    # track which occurrence of each label we are on
    irrep_occurrence: Dict[str, int] = {}

    var_map = {}
    counter = 1

    for irrep in irreps:
        is_mag, stripped = _strip_magnetic(irrep)
        dim = dimensions[stripped]
        component_labels = _index_labels(dim)

        # track occurrence index for this label
        irrep_occurrence[irrep] = irrep_occurrence.get(irrep, 0) + 1
        occurrence = irrep_occurrence[irrep]

        # build the base label used for default naming:
        # if duplicated, append [N] to distinguish occurrences
        if irrep in duplicated:
            base_label = f"{irrep}[{occurrence}]"
            base_code = f"{_sanitize_for_code(irrep)}{occurrence}"
        else:
            base_label = irrep
            base_code = _sanitize_for_code(irrep)

        # check for user overrides: try positional key first, then plain label
        positional_key = f"{irrep}[{occurrence}]"
        if user_names and positional_key in user_names:
            overrides = user_names[positional_key]
            if len(overrides) != dim:
                raise ValueError(
                    f"User supplied {len(overrides)} names for {positional_key} "
                    f"but its dimension is {dim}"
                )
            names_display = overrides
            names_code = [_sanitize_for_code(n) for n in overrides]
        elif user_names and irrep in user_names and irrep not in duplicated:
            overrides = user_names[irrep]
            if len(overrides) != dim:
                raise ValueError(
                    f"User supplied {len(overrides)} names for {irrep} "
                    f"but its dimension is {dim}"
                )
            names_display = overrides
            names_code = [_sanitize_for_code(n) for n in overrides]
        else:
            names_display = [f"{base_label}_{c}" for c in component_labels[:dim]]
            names_code = [f"{base_code}_{c}" for c in component_labels[:dim]]

        for comp_label, name_display, name_code in zip(
            component_labels[:dim], names_display, names_code
        ):
            iso_name = f"n{counter}"
            var_map[iso_name] = {
                "display": name_display,
                "code": name_code,
                "irrep": stripped,
                "magnetic": is_mag,
                "component": comp_label,
            }
            counter += 1

    return var_map


def _substitute_polynomial(polynomial: str, var_map: Dict[str, dict], mode: str) -> str:
    """
    Replace iso generic variable names (n1, n2, ...) with parenthesised physical names.

    Each token nN is replaced with (name), e.g. n1 -> (GM2m_a).
    This makes implicit multiplication explicit: adjacent tokens always appear
    as )( or )^N( which output modules convert to their appropriate separator.

    Single-pass substitution sorted longest-first so n10 matches before n1.
    """
    sorted_keys = sorted(var_map.keys(), key=lambda k: -len(k))
    alts = '|'.join(re.escape(k) for k in sorted_keys)
    pattern = re.compile(
        r'(?<=\d)(' + alts + r')|(?<![a-zA-Z])(' + alts + r')'
    )

    def replacer(match):
        token = match.group(1) or match.group(2)
        return '(' + var_map[token][mode] + ')'

    return pattern.sub(replacer, polynomial)


def substitute_invariants(
    invariants: List[dict],
    var_map: Dict[str, dict],
    mode: str,
) -> List[dict]:
    """
    Apply variable substitution to a list of invariant dicts.
    Returns new list with 'polynomial' replaced (tokens wrapped in parentheses).
    mode: 'display' or 'code'
    """
    result = []
    for inv in invariants:
        result.append({
            "degree": inv["degree"],
            "polynomial": _substitute_polynomial(inv["polynomial"], var_map, mode),
        })
    return result


def _get_magnetic_names(var_map: Dict[str, dict], mode: str) -> Set[str]:
    """Return set of variable names (in given mode) that belong to magnetic irreps."""
    return {v[mode] for v in var_map.values() if v["magnetic"]}


def _monomial_magnetic_power(monomial: str, magnetic_names: Set[str]) -> int:
    """
    Compute total power of magnetic variables in a single monomial term.
    Searches the parenthesised form directly: each variable token appears
    as (name) optionally followed by ^N, avoiding false matches from
    adjacent variable names that share leading characters.
    """
    total = 0
    for name in magnetic_names:
        escaped = re.escape(name)
        for match in re.finditer(
            r'\(' + escaped + r'\)(?:\^(\d+))?', monomial
        ):
            exp = int(match.group(1)) if match.group(1) else 1
            total += exp
    return total


def _polynomial_magnetic_power(polynomial: str, magnetic_names: Set[str]) -> int:
    """
    Return total magnetic variable power for a polynomial line.
    Raises if monomials within a line have mixed parity (should not happen).
    """
    # In parenthesised form, term separators are whitespace followed by a sign then
    # an opening paren or digit. Variable names like GM4- never have space before -/+.
    terms = re.split(r'\s+(?=[+-]\(|[+-]\d)', polynomial)
    powers = [_monomial_magnetic_power(t, magnetic_names) for t in terms]
    if len(set(p % 2 for p in powers)) > 1:
        import warnings
        warnings.warn(
            f"Mixed magnetic parity in polynomial (check TRS logic): {polynomial}\n"
            f"Powers: {powers}"
        )
    return powers[0] if powers else 0


def apply_trs_filter(
    invariants: List[dict],
    var_map: Dict[str, dict],
    mode: str,
) -> List[dict]:
    """
    Filter invariants keeping only those where total magnetic variable power is even.
    Operates on already-substituted invariants.
    mode: 'display' or 'code' — must match the mode used in substitute_invariants.
    """
    magnetic_names = _get_magnetic_names(var_map, mode)
    if not magnetic_names:
        return invariants

    filtered = []
    for inv in invariants:
        power = _polynomial_magnetic_power(inv["polynomial"], magnetic_names)
        if power % 2 == 0:
            filtered.append(inv)
    return filtered

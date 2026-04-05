"""
runner.py
Handles all subprocess calls to the iso executable and parses iso.log output.
Each call runs in its own temporary directory to avoid iso.log collisions.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path


ISO_EXEC_DEFAULT = "iso"


def _run_iso(input_str: str, iso_exec: str = ISO_EXEC_DEFAULT) -> str:
    """
    Run iso with the given input string, return the contents of iso.log.
    Raises RuntimeError if iso fails or iso.log is not produced.
    """
    tmpdir = tempfile.mkdtemp(prefix="isoinv_")
    try:
        input_file = Path(tmpdir) / "input.iso"
        input_file.write_text(input_str)

        result = subprocess.run(
            [iso_exec],
            stdin=open(input_file),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=tmpdir,
        )

        log_path = Path(tmpdir) / "iso.log"
        if not log_path.exists():
            raise RuntimeError(
                f"iso.log not produced. stderr: {result.stderr.decode()}"
            )

        return log_path.read_text()

    finally:
        shutil.rmtree(tmpdir)


def _build_dim_input(parent: int, irrep: str) -> str:
    """Build iso input string for a single-irrep dimension query."""
    return (
        f"VALUE PARENT {parent}\n"
        f"VALUE IRREP {irrep}\n"
        f"SHOW DIMENSION\n"
        f"PAGE NOBREAK\n"
        f"SCREEN 340\n"
        f"DISPLAY IRREP\n"
        f"QUIT\n"
    )


def _build_invariants_input(parent: int, irreps: list[str], degree: tuple[int, int]) -> str:
    """Build iso input string for the invariants query."""
    irrep_str = " ".join(irreps)
    deg_lo, deg_hi = degree
    if deg_lo == deg_hi:
        deg_str = str(deg_lo)
    else:
        deg_str = f"{deg_lo} {deg_hi}"
    return (
        f"VALUE PARENT {parent}\n"
        f"VALUE IRREP {irrep_str}\n"
        f"PAGE NOBREAK\n"
        f"SCREEN 340\n"
        f"VALUE DEGREE {deg_str}\n"
        f"DISPLAY INVARIANT\n"
        f"QUIT\n"
    )


def _parse_dimension(log: str) -> int:
    """
    Parse dimension integer from iso.log of a DISPLAY IRREP call.
    Looks for 'Dim' header line and reads the next non-empty line as an integer.
    """
    lines = log.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "Dim":
            # next non-empty line is the integer
            for j in range(i + 1, len(lines)):
                val = lines[j].strip()
                if val:
                    return int(val)
    raise ValueError(f"Could not parse dimension from iso.log:\n{log}")


def _parse_invariants(log: str) -> list[dict]:
    """
    Parse invariant polynomial lines from iso.log of a DISPLAY INVARIANT call.
    Returns a list of dicts: [{'degree': int, 'polynomial': str}, ...]
    Skips all 'Deg Invariants' header lines (may appear multiple times).
    Stops at '*QUIT'.
    """
    lines = log.splitlines()

    # find start: line after '*DISPLAY INVARIANT'
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "*DISPLAY INVARIANT":
            start = i + 1
            break
    if start is None:
        raise ValueError("Could not find '*DISPLAY INVARIANT' in iso.log")

    invariants = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped == "*QUIT":
            break
        if stripped == "Deg Invariants" or stripped == "":
            continue
        # data lines: "4   n1^4" or "3   n1n2n6 -n1n3n5"
        parts = stripped.split(None, 1)
        if len(parts) == 2:
            try:
                degree = int(parts[0])
                polynomial = parts[1].strip()
                invariants.append({"degree": degree, "polynomial": polynomial})
            except ValueError:
                # not a data line, skip
                continue

    return invariants


def get_irrep_dimension(
    parent: int, irrep: str, iso_exec: str = ISO_EXEC_DEFAULT
) -> int:
    """
    Query iso for the dimension of a single irrep.
    irrep should already have any 'm' prefix stripped.
    """
    input_str = _build_dim_input(parent, irrep)
    log = _run_iso(input_str, iso_exec)
    return _parse_dimension(log)


def get_invariants(
    parent: int,
    irreps: list[str],
    degree: tuple[int, int],
    iso_exec: str = ISO_EXEC_DEFAULT,
) -> list[dict]:
    """
    Query iso for invariant polynomials.
    irreps should already have any 'm' prefixes stripped.
    Returns list of {'degree': int, 'polynomial': str}.
    """
    input_str = _build_invariants_input(parent, irreps, degree)
    log = _run_iso(input_str, iso_exec)
    return _parse_invariants(log)

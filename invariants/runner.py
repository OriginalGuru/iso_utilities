"""
runner.py
Handles all subprocess calls to the iso executable and parses iso.log output.
Each call runs in its own temporary directory to avoid iso.log collisions.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional, Tuple


ISO_EXEC_DEFAULT = "iso"


def _run_iso(
    input_str: str,
    iso_exec: str = ISO_EXEC_DEFAULT,
    debug_path: Optional[Path] = None,
) -> str:
    """
    Run iso with the given input string, return the contents of iso.log.
    If debug_path is provided, iso.log is copied there before the temp dir
    is cleaned up.
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

        log_text = log_path.read_text()

        if debug_path is not None:
            debug_path.parent.mkdir(parents=True, exist_ok=True)
            debug_path.write_text(log_text)

        return log_text

    finally:
        shutil.rmtree(tmpdir)


def _build_dim_input(parent: int, irrep: str) -> str:
    """Build iso input string for a single-irrep dimension query."""
    return (
        f"VALUE PARENT {parent}\n"
        f"VALUE IRREP {irrep}\n"
        f"SHOW DIMENSION\n"
        f"PAGE NOBREAK\n"
        f"SCREEN 1000\n"
        f"DISPLAY IRREP\n"
        f"QUIT\n"
    )


def _build_invariants_input(parent: int, irreps: List[str], degree: Tuple[int, int]) -> str:
    """Build iso input string for the invariants query."""
    irrep_str = " ".join(irreps)
    deg_lo, deg_hi = degree
    deg_str = str(deg_lo) if deg_lo == deg_hi else f"{deg_lo} {deg_hi}"
    return (
        f"VALUE PARENT {parent}\n"
        f"VALUE IRREP {irrep_str}\n"
        f"PAGE NOBREAK\n"
        f"SCREEN 1000\n"
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
            for j in range(i + 1, len(lines)):
                val = lines[j].strip()
                if val:
                    return int(val)
    raise ValueError(f"Could not parse dimension from iso.log:\n{log}")


def _parse_invariants(log: str) -> List[dict]:
    """
    Parse invariant polynomial lines from iso.log of a DISPLAY INVARIANT call.
    Returns a list of dicts: [{'degree': int, 'polynomial': str}, ...]
    Skips all 'Deg Invariants' header lines (may appear multiple times).
    Stops at '*QUIT'.
    """
    lines = log.splitlines()

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
        parts = stripped.split(None, 1)
        if len(parts) == 2:
            try:
                degree = int(parts[0])
                polynomial = parts[1].strip()
                invariants.append({"degree": degree, "polynomial": polynomial})
            except ValueError:
                continue

    return invariants


def get_irrep_dimension(
    parent: int,
    irrep: str,
    iso_exec: str = ISO_EXEC_DEFAULT,
    debug_path: Optional[Path] = None,
) -> int:
    """
    Query iso for the dimension of a single irrep.
    irrep should already have any 'm' prefix stripped.
    If debug_path is provided, iso.log is saved there.
    """
    input_str = _build_dim_input(parent, irrep)
    log = _run_iso(input_str, iso_exec, debug_path=debug_path)
    return _parse_dimension(log)


def get_invariants(
    parent: int,
    irreps: List[str],
    degree: Tuple[int, int],
    iso_exec: str = ISO_EXEC_DEFAULT,
    debug_path: Optional[Path] = None,
) -> List[dict]:
    """
    Query iso for invariant polynomials.
    irreps should already have any 'm' prefixes stripped.
    Returns list of {'degree': int, 'polynomial': str}.
    If debug_path is provided, iso.log is saved there.
    """
    input_str = _build_invariants_input(parent, irreps, degree)
    log = _run_iso(input_str, iso_exec, debug_path=debug_path)
    return _parse_invariants(log)

# invariants

Generates invariant polynomials using ISOTROPY with physically meaningful variable names,
optional time-reversal symmetry (TRS) filtering, and multiple output formats.

## Requirements

- Python 3.11+
- ISOTROPY (`iso` executable on PATH or passed via `--iso-exec`)
- Python dependencies: `pip install -r requirements.txt`

## Usage

```bash
# Basic
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 4

# Degree range
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 3 6

# With magnetic irreps (m prefix triggers TRS filtering)
python isoinv.py --parent 194 --irreps GM2- mGM6- GM2+ mGM6+ A1 --degree 4

# With user-defined variable name overrides
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 4 \
    --names GM2-:Pz GM6-:Px,Py GM2+:Mz GM6+:Mx,My A1:phi

# Collapsed single-polynomial output with named coefficients
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 4 \
    --collapse --coeff-style alpha

# Select output formats (default: all)
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 4 \
    --formats md py

# Custom output directory
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 4 \
    --outdir my_output

# Custom iso executable path
python isoinv.py --parent 194 --irreps GM2- GM6- GM2+ GM6+ A1 --degree 4 \
    --iso-exec /path/to/iso
```

## Output

By default, output files are written to `sg{N}__{irreps}__{deg}/`, e.g.:

```
sg194__GM2m_GM6m_GM2p_GM6p_A1__deg4/
├── sg194__GM2m_GM6m_GM2p_GM6p_A1__deg4.md
├── sg194__GM2m_GM6m_GM2p_GM6p_A1__deg4.py
├── sg194__GM2m_GM6m_GM2p_GM6p_A1__deg4.nb
└── sg194__GM2m_GM6m_GM2p_GM6p_A1__deg4.tex
```

## Variable naming

By default, variables are named `{irrep}_{component}` where component is `a, b, c, ...`
assigned in order of the irrep's dimension. For example, `GM6-` with dimension 2 becomes
`GM6-_a` and `GM6-_b`.

In code output modes (Python, Mathematica), `+` and `-` in irrep labels are replaced
with `p` and `m` respectively to produce valid identifiers.

## Time-reversal symmetry

Irreps prefixed with `m` (e.g. `mGM6-`) are treated as magnetic. TRS filtering removes
any invariant where the total power across all magnetic variables is odd.

## Examples

See `examples/barium_hexaferrite/` for a worked example with space group 194.

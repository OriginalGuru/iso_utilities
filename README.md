# iso_utilities

A collection of Python tools for working with the [ISOTROPY](https://iso.byu.edu/isolinux.php) software suite.

## Tools

### invariants — `isoinv.py`

Generates invariant polynomials from ISOTROPY with physically meaningful variable names,
time-reversal symmetry (TRS) filtering, and multiple output formats.

```bash
python invariants/isoinv.py \
    --parent 194 \
    --irreps GM2-:Pz GM6-:Px,Py GM2+:Mz GM6+:Mx,My A1:A1a,A1b \
    --degree 4 \
    --collapse --coeff-style alpha \
    --formats md py nb tex
```

Key features:
- Variable name overrides inline with irrep labels (`IRREP:name1,name2,...`)
- Magnetic irrep prefix (`mGM5-`) with automatic TRS filtering
- Duplicate irrep handling (`GM4- GM4-` → `GM4-[1]`, `GM4-[2]`)
- Collapsed free energy with named coefficients
- Output formats: Markdown, SymPy/Python, Mathematica notebook, LaTeX
- Debug mode (`--debug`, `--debug-only`) saves raw `iso.log` files

See `invariants/README.md` for full usage.

### condensation — `isocond.py`

Takes the collapsed free energy output from `isoinv.py` and performs order parameter
condensation: substitutes `P → P0 + δP`, expands, and regroups terms into new effective
invariants with renormalized coefficients expressed in terms of the original coefficients
and the static condensed value `P0`.

```bash
python condensation/isocond.py \
    --indir sg194__GM2m_GM6m_GM2p_GM6p_A1__deg4 \
    --condense Pz:Pz0 \
    --formats md py
```

Key features:
- Single or multiple simultaneous condensations (`--condense Pz:Pz0 Mz:Mz0`)
- Coefficients remain fully symbolic in the static values (`P0`, `Mz0`)
- Truncation to a maximum dynamic degree after condensation (`--max-degree 2`)
- Linearization in the static variables for small-OP approximation (`--linear-static`)
- Flags can be combined: `--max-degree 2 --linear-static`

Output files are written into the same directory as the input, with filenames encoding
the condensed variables and any approximations applied, e.g.
`invariants_condensed_Pz_deg2_linear.md`.

## Repository Structure

```
iso_utilities/
├── README.md
├── invariants/          # isoinv.py and supporting modules
│   ├── isoinv.py
│   ├── runner.py
│   ├── parser.py
│   ├── collapse.py
│   ├── output_md.py
│   ├── output_py.py
│   ├── output_nb.py
│   ├── output_tex.py
│   ├── irrational_map.py
│   └── README.md
├── condensation/        # isocond.py
│   ├── isocond.py
│   └── README.md
└── examples/            # worked examples using the tools in sequence
    ├── barium_hexaferrite/
    └── cubic_perovskite/
```

## Typical Workflow

```bash
cd examples/barium_hexaferrite

# Step 1: generate invariant polynomials
python ../../invariants/isoinv.py \
    --parent 194 \
    --irreps GM1+:ε GM2-:P GM6-:Qx,Qy mGM2+:Mz mGM6+:Mx,My \
    --degree 1 6 --collapse --coeff-style alpha

# Step 2: condense order parameters
python ../../condensation/isocond.py \
    --indir sg194__GM1p_GM2m_GM6m_mGM2p_mGM6p__deg1-6 \
    --condense P:P0 Mz:Mz0

# Step 3: simplified model (degree 2 in dynamic variables, linearized in P0, Mz0)
python ../../condensation/isocond.py \
    --indir sg194__GM1p_GM2m_GM6m_mGM2p_mGM6p__deg1-6 \
    --condense P:P0 Mz:Mz0 --max-degree 2 --linear-static
```

## Requirements

- Python 3.9+
- `sympy` (for `isocond.py`)
- [ISOTROPY](https://iso.byu.edu/isolinux.php) — the `iso` executable must be on your
  PATH or its location passed via `--iso-exec`

Each tool directory also has its own `requirements.txt`.

# Condensed Invariant Polynomials

**Source:** `output_test`  
**Condensation:** Pz → Pz0+dPz  
**Static variables:** `Pz0`  
**Dynamic variables:** `dPz`, `Qx`, `Qy`, `Mz`  
**New invariants:** 14

## New Invariants

### Degree 0

1. `1`

### Degree 1

2. `dPz`

### Degree 2

3. `dPz^2`
4. `Qx^2 + Qy^2`
5. `Mz^2`

### Degree 3

6. `dPz^3`
7. `Qx^2dPz + Qy^2dPz`
8. `Mz^2dPz`

### Degree 4

9. `dPz^4`
10. `Qx^2dPz^2 + Qy^2dPz^2`
11. `Mz^2dPz^2`
12. `Qx^4 + 2Qx^2Qy^2 + Qy^4`
13. `Mz^2Qx^2 + Mz^2Qy^2`
14. `Mz^4`

## Collapsed Condensed Free Energy

F = beta1 * (1) + beta2 * (dPz) + beta3 * (dPz^2) + beta4 * (Qx^2 + Qy^2) + beta5 * (Mz^2) + beta6 * (dPz^3) + beta7 * (Qx^2dPz + Qy^2dPz) + beta8 * (Mz^2dPz) + beta9 * (dPz^4) + beta10 * (Qx^2dPz^2 + Qy^2dPz^2) + beta11 * (Mz^2dPz^2) + beta12 * (Qx^4 + 2Qx^2Qy^2 + Qy^4) + beta13 * (Mz^2Qx^2 + Mz^2Qy^2) + beta14 * (Mz^4)

## Coefficient Mapping

New coefficients expressed in terms of original coefficients and static values:

- `beta1` = `Pz0**2*(Pz0**2*c4 + c1)`
- `beta2` = `2*Pz0*(2*Pz0**2*c4 + c1)`
- `beta3` = `6*Pz0**2*c4 + c1`
- `beta4` = `Pz0**2*c5 + c2`
- `beta5` = `Pz0**2*c6 + c3`
- `beta6` = `4*Pz0*c4`
- `beta7` = `2*Pz0*c5`
- `beta8` = `2*Pz0*c6`
- `beta9` = `c4`
- `beta10` = `c5`
- `beta11` = `c6`
- `beta12` = `c7`
- `beta13` = `c8`
- `beta14` = `c9`

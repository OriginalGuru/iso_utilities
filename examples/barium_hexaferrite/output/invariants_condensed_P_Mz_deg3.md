# Condensed Invariant Polynomials

**Source:** `output`  
**Condensation:** P → P0+dP, Mz → Mz0+dMz  
**Static variables:** `P0`, `Mz0`  
**Dynamic variables:** `dP`, `dMz`, `ε`, `Qx`, `Qy`, `Mx`, `My`  
**New invariants:** 32

## New Invariants

### Degree 0

1. `1`

### Degree 1

2. `dMz`
3. `ε`
4. `dP`

### Degree 2

5. `dMz^2`
6. `dMzε`
7. `ε^2`
8. `dP^2`
9. `Qx^2 + Qy^2`
10. `Mx^2 + My^2`
11. `dMzdP`
12. `MxQx + MyQy`
13. `dPε`

### Degree 3

14. `dMz^2ε`
15. `dMzε^2`
16. `dMzdP^2`
17. `Qx^2dMz + Qy^2dMz`
18. `Mx^2dMz + My^2dMz`
19. `dMz^3`
20. `MxQxdP + MyQydP`
21. `ε^3`
22. `dP^2ε`
23. `Qx^2ε + Qy^2ε`
24. `Mx^2ε + My^2ε`
25. `dMzdPε`
26. `MxQxε + MyQyε`
27. `MxQxdMz + MyQydMz`
28. `dMz^2dP`
29. `dPε^2`
30. `dP^3`
31. `Qx^2dP + Qy^2dP`
32. `Mx^2dP + My^2dP`

## Collapsed Condensed Free Energy

F = beta1 * (1) + beta2 * (dMz) + beta3 * (ε) + beta4 * (dP) + beta5 * (dMz^2) + beta6 * (dMzε) + beta7 * (ε^2) + beta8 * (dP^2) + beta9 * (Qx^2 + Qy^2) + beta10 * (Mx^2 + My^2) + beta11 * (dMzdP) + beta12 * (MxQx + MyQy) + beta13 * (dPε) + beta14 * (dMz^2ε) + beta15 * (dMzε^2) + beta16 * (dMzdP^2) + beta17 * (Qx^2dMz + Qy^2dMz) + beta18 * (Mx^2dMz + My^2dMz) + beta19 * (dMz^3) + beta20 * (MxQxdP + MyQydP) + beta21 * (ε^3) + beta22 * (dP^2ε) + beta23 * (Qx^2ε + Qy^2ε) + beta24 * (Mx^2ε + My^2ε) + beta25 * (dMzdPε) + beta26 * (MxQxε + MyQyε) + beta27 * (MxQxdMz + MyQydMz) + beta28 * (dMz^2dP) + beta29 * (dPε^2) + beta30 * (dP^3) + beta31 * (Qx^2dP + Qy^2dP) + beta32 * (Mx^2dP + My^2dP)

## Coefficient Mapping

New coefficients expressed in terms of original coefficients and static values:

- `beta1` = `Mz0**6*alpha90 + Mz0**4*P0**2*alpha72 + Mz0**4*alpha26 + Mz0**2*P0**4*alpha65 + Mz0**2*P0**2*alpha19 + Mz0**2*alpha5 + P0**6*alpha63 + P0**4*alpha17 + P0**2*alpha3`
- `beta2` = `2*Mz0*(3*Mz0**4*alpha90 + 2*Mz0**2*P0**2*alpha72 + 2*Mz0**2*alpha26 + P0**4*alpha65 + P0**2*alpha19 + alpha5)`
- `beta3` = `Mz0**4*alpha43 + Mz0**2*P0**2*alpha36 + Mz0**2*alpha10 + P0**4*alpha34 + P0**2*alpha8 + alpha1`
- `beta4` = `2*P0*(Mz0**4*alpha72 + 2*Mz0**2*P0**2*alpha65 + Mz0**2*alpha19 + 3*P0**4*alpha63 + 2*P0**2*alpha17 + alpha3)`
- `beta5` = `15*Mz0**4*alpha90 + 6*Mz0**2*P0**2*alpha72 + 6*Mz0**2*alpha26 + P0**4*alpha65 + P0**2*alpha19 + alpha5`
- `beta6` = `2*Mz0*(2*Mz0**2*alpha43 + P0**2*alpha36 + alpha10)`
- `beta7` = `Mz0**4*alpha60 + Mz0**2*P0**2*alpha53 + Mz0**2*alpha15 + P0**4*alpha51 + P0**2*alpha13 + alpha2`
- `beta8` = `Mz0**4*alpha72 + 6*Mz0**2*P0**2*alpha65 + Mz0**2*alpha19 + 15*P0**4*alpha63 + 6*P0**2*alpha17 + alpha3`
- `beta9` = `Mz0**4*alpha84 + Mz0**2*P0**2*alpha69 + Mz0**2*alpha23 + P0**4*alpha64 + P0**2*alpha18 + alpha4`
- `beta10` = `Mz0**4*alpha91 + Mz0**2*P0**2*alpha73 + Mz0**2*alpha27 + P0**4*alpha66 + P0**2*alpha20 + alpha6`
- `beta11` = `4*Mz0*P0*(2*Mz0**2*alpha72 + 2*P0**2*alpha65 + alpha19)`
- `beta12` = `Mz0*P0*(Mz0**2*alpha76 + P0**2*alpha67 + alpha21)`
- `beta13` = `2*P0*(Mz0**2*alpha36 + 2*P0**2*alpha34 + alpha8)`
- `beta14` = `6*Mz0**2*alpha43 + P0**2*alpha36 + alpha10`
- `beta15` = `2*Mz0*(2*Mz0**2*alpha60 + P0**2*alpha53 + alpha15)`
- `beta16` = `2*Mz0*(2*Mz0**2*alpha72 + 6*P0**2*alpha65 + alpha19)`
- `beta17` = `2*Mz0*(2*Mz0**2*alpha84 + P0**2*alpha69 + alpha23)`
- `beta18` = `2*Mz0*(2*Mz0**2*alpha91 + P0**2*alpha73 + alpha27)`
- `beta19` = `4*Mz0*(5*Mz0**2*alpha90 + P0**2*alpha72 + alpha26)`
- `beta20` = `Mz0*(Mz0**2*alpha76 + 3*P0**2*alpha67 + alpha21)`
- `beta21` = `Mz0**2*alpha32 + P0**2*alpha30 + alpha7`
- `beta22` = `Mz0**2*alpha36 + 6*P0**2*alpha34 + alpha8`
- `beta23` = `Mz0**2*alpha40 + P0**2*alpha35 + alpha9`
- `beta24` = `Mz0**2*alpha44 + P0**2*alpha37 + alpha11`
- `beta25` = `4*Mz0*P0*alpha36`
- `beta26` = `Mz0*P0*alpha38`
- `beta27` = `P0*(3*Mz0**2*alpha76 + P0**2*alpha67 + alpha21)`
- `beta28` = `2*P0*(6*Mz0**2*alpha72 + 2*P0**2*alpha65 + alpha19)`
- `beta29` = `2*P0*(Mz0**2*alpha53 + 2*P0**2*alpha51 + alpha13)`
- `beta30` = `4*P0*(Mz0**2*alpha65 + 5*P0**2*alpha63 + alpha17)`
- `beta31` = `2*P0*(Mz0**2*alpha69 + 2*P0**2*alpha64 + alpha18)`
- `beta32` = `2*P0*(Mz0**2*alpha73 + 2*P0**2*alpha66 + alpha20)`

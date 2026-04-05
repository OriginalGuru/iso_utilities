# Condensed Invariant Polynomials

**Source:** `output`  
**Condensation:** P → P0+dP, Mz → Mz0+dMz  
**Static variables:** `P0`, `Mz0`  
**Dynamic variables:** `dP`, `dMz`, `ε`, `Qx`, `Qy`, `Mx`, `My`  
**New invariants:** 31

## New Invariants

### Degree 1

1. `dMz`
2. `ε`
3. `dP`

### Degree 2

4. `dMz^2`
5. `dMzε`
6. `ε^2`
7. `dP^2`
8. `Qx^2 + Qy^2`
9. `Mx^2 + My^2`
10. `dMzdP`
11. `MxQx + MyQy`
12. `dPε`

### Degree 3

13. `dMz^2ε`
14. `dMzε^2`
15. `dMzdP^2`
16. `Qx^2dMz + Qy^2dMz`
17. `Mx^2dMz + My^2dMz`
18. `dMz^3`
19. `MxQxdP + MyQydP`
20. `ε^3`
21. `dP^2ε`
22. `Qx^2ε + Qy^2ε`
23. `Mx^2ε + My^2ε`
24. `dMzdPε`
25. `MxQxε + MyQyε`
26. `MxQxdMz + MyQydMz`
27. `dMz^2dP`
28. `dPε^2`
29. `dP^3`
30. `Qx^2dP + Qy^2dP`
31. `Mx^2dP + My^2dP`

## Collapsed Condensed Free Energy

F = beta1 * (dMz) + beta2 * (ε) + beta3 * (dP) + beta4 * (dMz^2) + beta5 * (dMzε) + beta6 * (ε^2) + beta7 * (dP^2) + beta8 * (Qx^2 + Qy^2) + beta9 * (Mx^2 + My^2) + beta10 * (dMzdP) + beta11 * (MxQx + MyQy) + beta12 * (dPε) + beta13 * (dMz^2ε) + beta14 * (dMzε^2) + beta15 * (dMzdP^2) + beta16 * (Qx^2dMz + Qy^2dMz) + beta17 * (Mx^2dMz + My^2dMz) + beta18 * (dMz^3) + beta19 * (MxQxdP + MyQydP) + beta20 * (ε^3) + beta21 * (dP^2ε) + beta22 * (Qx^2ε + Qy^2ε) + beta23 * (Mx^2ε + My^2ε) + beta24 * (dMzdPε) + beta25 * (MxQxε + MyQyε) + beta26 * (MxQxdMz + MyQydMz) + beta27 * (dMz^2dP) + beta28 * (dPε^2) + beta29 * (dP^3) + beta30 * (Qx^2dP + Qy^2dP) + beta31 * (Mx^2dP + My^2dP)

## Coefficient Mapping

New coefficients expressed in terms of original coefficients and static values:

- `beta1` = `2*Mz0*alpha5`
- `beta2` = `alpha1`
- `beta3` = `2*P0*alpha3`
- `beta4` = `alpha5`
- `beta5` = `2*Mz0*alpha10`
- `beta6` = `alpha2`
- `beta7` = `alpha3`
- `beta8` = `alpha4`
- `beta9` = `alpha6`
- `beta10` = `4*Mz0*P0*alpha19`
- `beta11` = `Mz0*P0*alpha21`
- `beta12` = `2*P0*alpha8`
- `beta13` = `alpha10`
- `beta14` = `2*Mz0*alpha15`
- `beta15` = `2*Mz0*alpha19`
- `beta16` = `2*Mz0*alpha23`
- `beta17` = `2*Mz0*alpha27`
- `beta18` = `4*Mz0*alpha26`
- `beta19` = `Mz0*alpha21`
- `beta20` = `alpha7`
- `beta21` = `alpha8`
- `beta22` = `alpha9`
- `beta23` = `alpha11`
- `beta24` = `4*Mz0*P0*alpha36`
- `beta25` = `Mz0*P0*alpha38`
- `beta26` = `P0*alpha21`
- `beta27` = `2*P0*alpha19`
- `beta28` = `2*P0*alpha13`
- `beta29` = `4*P0*alpha17`
- `beta30` = `2*P0*alpha18`
- `beta31` = `2*P0*alpha20`

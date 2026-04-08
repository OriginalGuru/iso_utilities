# Condensed Invariant Polynomials

**Source:** `output_elec`  
**Condensation:** P → P0+dP, Mz → Mz0+dMz  
**Static variables:** `P0`, `Mz0`  
**Dynamic variables:** `dP`, `dMz`, `ε`, `Qx`, `Qy`, `Ex`, `Ey`, `Mx`, `My`  
**New invariants:** 43

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
9. `ExQx + EyQy`
10. `Ex^2 + Ey^2`
11. `Mx^2 + My^2`
12. `dMzdP`
13. `MxQx + MyQy`
14. `ExMx + EyMy`
15. `dPε`

### Degree 3

16. `dMz^2ε`
17. `dMzε^2`
18. `dMzdP^2`
19. `Qx^2dMz + Qy^2dMz`
20. `ExQxdMz + EyQydMz`
21. `Ex^2dMz + Ey^2dMz`
22. `Mx^2dMz + My^2dMz`
23. `dMz^3`
24. `MxQxdP + MyQydP`
25. `ExMxdP + EyMydP`
26. `ε^3`
27. `dP^2ε`
28. `Qx^2ε + Qy^2ε`
29. `ExQxε + EyQyε`
30. `Ex^2ε + Ey^2ε`
31. `Mx^2ε + My^2ε`
32. `dMzdPε`
33. `MxQxε + MyQyε`
34. `ExMxε + EyMyε`
35. `MxQxdMz + MyQydMz`
36. `ExMxdMz + EyMydMz`
37. `dMz^2dP`
38. `dP^3`
39. `Qx^2dP + Qy^2dP`
40. `ExQxdP + EyQydP`
41. `Ex^2dP + Ey^2dP`
42. `Mx^2dP + My^2dP`
43. `dPε^2`

## Collapsed Condensed Free Energy

F = beta1 * (dMz) + beta2 * (ε) + beta3 * (dP) + beta4 * (dMz^2) + beta5 * (dMzε) + beta6 * (ε^2) + beta7 * (dP^2) + beta8 * (Qx^2 + Qy^2) + beta9 * (ExQx + EyQy) + beta10 * (Ex^2 + Ey^2) + beta11 * (Mx^2 + My^2) + beta12 * (dMzdP) + beta13 * (MxQx + MyQy) + beta14 * (ExMx + EyMy) + beta15 * (dPε) + beta16 * (dMz^2ε) + beta17 * (dMzε^2) + beta18 * (dMzdP^2) + beta19 * (Qx^2dMz + Qy^2dMz) + beta20 * (ExQxdMz + EyQydMz) + beta21 * (Ex^2dMz + Ey^2dMz) + beta22 * (Mx^2dMz + My^2dMz) + beta23 * (dMz^3) + beta24 * (MxQxdP + MyQydP) + beta25 * (ExMxdP + EyMydP) + beta26 * (ε^3) + beta27 * (dP^2ε) + beta28 * (Qx^2ε + Qy^2ε) + beta29 * (ExQxε + EyQyε) + beta30 * (Ex^2ε + Ey^2ε) + beta31 * (Mx^2ε + My^2ε) + beta32 * (dMzdPε) + beta33 * (MxQxε + MyQyε) + beta34 * (ExMxε + EyMyε) + beta35 * (MxQxdMz + MyQydMz) + beta36 * (ExMxdMz + EyMydMz) + beta37 * (dMz^2dP) + beta38 * (dP^3) + beta39 * (Qx^2dP + Qy^2dP) + beta40 * (ExQxdP + EyQydP) + beta41 * (Ex^2dP + Ey^2dP) + beta42 * (Mx^2dP + My^2dP) + beta43 * (dPε^2)

## Coefficient Mapping

New coefficients expressed in terms of original coefficients and static values:

- `beta1` = `2*Mz0*alpha7`
- `beta2` = `alpha1`
- `beta3` = `2*P0*alpha3`
- `beta4` = `alpha7`
- `beta5` = `2*Mz0*alpha14`
- `beta6` = `alpha2`
- `beta7` = `alpha3`
- `beta8` = `alpha4`
- `beta9` = `alpha5`
- `beta10` = `alpha6`
- `beta11` = `alpha8`
- `beta12` = `4*Mz0*P0*alpha27`
- `beta13` = `Mz0*P0*alpha29`
- `beta14` = `Mz0*P0*alpha30`
- `beta15` = `2*P0*alpha10`
- `beta16` = `alpha14`
- `beta17` = `2*Mz0*alpha21`
- `beta18` = `2*Mz0*alpha27`
- `beta19` = `2*Mz0*alpha35`
- `beta20` = `2*Mz0*alpha39`
- `beta21` = `2*Mz0*alpha43`
- `beta22` = `2*Mz0*alpha47`
- `beta23` = `4*Mz0*alpha46`
- `beta24` = `Mz0*alpha29`
- `beta25` = `Mz0*alpha30`
- `beta26` = `alpha9`
- `beta27` = `alpha10`
- `beta28` = `alpha11`
- `beta29` = `alpha12`
- `beta30` = `alpha13`
- `beta31` = `alpha15`
- `beta32` = `4*Mz0*P0*alpha60`
- `beta33` = `Mz0*P0*alpha62`
- `beta34` = `Mz0*P0*alpha63`
- `beta35` = `P0*alpha29`
- `beta36` = `P0*alpha30`
- `beta37` = `2*P0*alpha27`
- `beta38` = `4*P0*alpha23`
- `beta39` = `2*P0*alpha24`
- `beta40` = `2*P0*alpha25`
- `beta41` = `2*P0*alpha26`
- `beta42` = `2*P0*alpha28`
- `beta43` = `2*P0*alpha17`

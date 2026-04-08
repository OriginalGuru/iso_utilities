# Condensed Invariant Polynomials

**Source:** `output_test`  
**Condensation:** P → P0+dP, Mz → Mz0+dMz  
**Static variables:** `P0`, `Mz0`  
**Dynamic variables:** `dP`, `dMz`, `ε`, `Qx`, `Qy`, `Ex`, `Ey`, `Mx`, `My`  
**New invariants:** 44

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
10. `ExQx + EyQy`
11. `Ex^2 + Ey^2`
12. `Mx^2 + My^2`
13. `dMzdP`
14. `MxQx + MyQy`
15. `ExMx + EyMy`
16. `dPε`

### Degree 3

17. `dMz^2ε`
18. `dMzε^2`
19. `dMzdP^2`
20. `Qx^2dMz + Qy^2dMz`
21. `ExQxdMz + EyQydMz`
22. `Ex^2dMz + Ey^2dMz`
23. `Mx^2dMz + My^2dMz`
24. `dMz^3`
25. `MxQxdP + MyQydP`
26. `ExMxdP + EyMydP`
27. `ε^3`
28. `dP^2ε`
29. `Qx^2ε + Qy^2ε`
30. `ExQxε + EyQyε`
31. `Ex^2ε + Ey^2ε`
32. `Mx^2ε + My^2ε`
33. `dMzdPε`
34. `MxQxε + MyQyε`
35. `ExMxε + EyMyε`
36. `MxQxdMz + MyQydMz`
37. `ExMxdMz + EyMydMz`
38. `dMz^2dP`
39. `dP^3`
40. `Qx^2dP + Qy^2dP`
41. `ExQxdP + EyQydP`
42. `Ex^2dP + Ey^2dP`
43. `Mx^2dP + My^2dP`
44. `dPε^2`

## Collapsed Condensed Free Energy

F = beta1 * (1) + beta2 * (dMz) + beta3 * (ε) + beta4 * (dP) + beta5 * (dMz^2) + beta6 * (dMzε) + beta7 * (ε^2) + beta8 * (dP^2) + beta9 * (Qx^2 + Qy^2) + beta10 * (ExQx + EyQy) + beta11 * (Ex^2 + Ey^2) + beta12 * (Mx^2 + My^2) + beta13 * (dMzdP) + beta14 * (MxQx + MyQy) + beta15 * (ExMx + EyMy) + beta16 * (dPε) + beta17 * (dMz^2ε) + beta18 * (dMzε^2) + beta19 * (dMzdP^2) + beta20 * (Qx^2dMz + Qy^2dMz) + beta21 * (ExQxdMz + EyQydMz) + beta22 * (Ex^2dMz + Ey^2dMz) + beta23 * (Mx^2dMz + My^2dMz) + beta24 * (dMz^3) + beta25 * (MxQxdP + MyQydP) + beta26 * (ExMxdP + EyMydP) + beta27 * (ε^3) + beta28 * (dP^2ε) + beta29 * (Qx^2ε + Qy^2ε) + beta30 * (ExQxε + EyQyε) + beta31 * (Ex^2ε + Ey^2ε) + beta32 * (Mx^2ε + My^2ε) + beta33 * (dMzdPε) + beta34 * (MxQxε + MyQyε) + beta35 * (ExMxε + EyMyε) + beta36 * (MxQxdMz + MyQydMz) + beta37 * (ExMxdMz + EyMydMz) + beta38 * (dMz^2dP) + beta39 * (dP^3) + beta40 * (Qx^2dP + Qy^2dP) + beta41 * (ExQxdP + EyQydP) + beta42 * (Ex^2dP + Ey^2dP) + beta43 * (Mx^2dP + My^2dP) + beta44 * (dPε^2)

## Coefficient Mapping

New coefficients expressed in terms of original coefficients and static values:

- `beta1` = `Mz0**6*alpha211 + Mz0**4*P0**2*alpha138 + Mz0**4*alpha46 + Mz0**2*P0**4*alpha119 + Mz0**2*P0**2*alpha27 + Mz0**2*alpha7 + P0**6*alpha115 + P0**4*alpha23 + P0**2*alpha3`
- `beta2` = `2*Mz0*(3*Mz0**4*alpha211 + 2*Mz0**2*P0**2*alpha138 + 2*Mz0**2*alpha46 + P0**4*alpha119 + P0**2*alpha27 + alpha7)`
- `beta3` = `Mz0**6*alpha345 + Mz0**4*P0**2*alpha272 + Mz0**4*alpha79 + Mz0**2*P0**4*alpha253 + Mz0**2*P0**2*alpha60 + Mz0**2*alpha14 + P0**6*alpha249 + P0**4*alpha56 + P0**2*alpha10 + alpha1`
- `beta4` = `2*P0*(Mz0**4*alpha138 + 2*Mz0**2*P0**2*alpha119 + Mz0**2*alpha27 + 3*P0**4*alpha115 + 2*P0**2*alpha23 + alpha3)`
- `beta5` = `15*Mz0**4*alpha211 + 6*Mz0**2*P0**2*alpha138 + 6*Mz0**2*alpha46 + P0**4*alpha119 + P0**2*alpha27 + alpha7`
- `beta6` = `2*Mz0*(3*Mz0**4*alpha345 + 2*Mz0**2*P0**2*alpha272 + 2*Mz0**2*alpha79 + P0**4*alpha253 + P0**2*alpha60 + alpha14)`
- `beta7` = `Mz0**4*alpha112 + Mz0**2*P0**2*alpha93 + Mz0**2*alpha21 + P0**4*alpha89 + P0**2*alpha17 + alpha2`
- `beta8` = `Mz0**4*alpha138 + 6*Mz0**2*P0**2*alpha119 + Mz0**2*alpha27 + 15*P0**4*alpha115 + 6*P0**2*alpha23 + alpha3`
- `beta9` = `Mz0**4*alpha180 + Mz0**2*P0**2*alpha127 + Mz0**2*alpha35 + P0**4*alpha116 + P0**2*alpha24 + alpha4`
- `beta10` = `Mz0**4*alpha193 + Mz0**2*P0**2*alpha131 + Mz0**2*alpha39 + P0**4*alpha117 + P0**2*alpha25 + alpha5`
- `beta11` = `Mz0**4*alpha205 + Mz0**2*P0**2*alpha135 + Mz0**2*alpha43 + P0**4*alpha118 + P0**2*alpha26 + alpha6`
- `beta12` = `Mz0**4*alpha212 + Mz0**2*P0**2*alpha139 + Mz0**2*alpha47 + P0**4*alpha120 + P0**2*alpha28 + alpha8`
- `beta13` = `4*Mz0*P0*(2*Mz0**2*alpha138 + 2*P0**2*alpha119 + alpha27)`
- `beta14` = `Mz0*P0*(Mz0**2*alpha146 + P0**2*alpha121 + alpha29)`
- `beta15` = `Mz0*P0*(Mz0**2*alpha149 + P0**2*alpha122 + alpha30)`
- `beta16` = `2*P0*(Mz0**4*alpha272 + 2*Mz0**2*P0**2*alpha253 + Mz0**2*alpha60 + 3*P0**4*alpha249 + 2*P0**2*alpha56 + alpha10)`
- `beta17` = `15*Mz0**4*alpha345 + 6*Mz0**2*P0**2*alpha272 + 6*Mz0**2*alpha79 + P0**4*alpha253 + P0**2*alpha60 + alpha14`
- `beta18` = `2*Mz0*(2*Mz0**2*alpha112 + P0**2*alpha93 + alpha21)`
- `beta19` = `2*Mz0*(2*Mz0**2*alpha138 + 6*P0**2*alpha119 + alpha27)`
- `beta20` = `2*Mz0*(2*Mz0**2*alpha180 + P0**2*alpha127 + alpha35)`
- `beta21` = `2*Mz0*(2*Mz0**2*alpha193 + P0**2*alpha131 + alpha39)`
- `beta22` = `2*Mz0*(2*Mz0**2*alpha205 + P0**2*alpha135 + alpha43)`
- `beta23` = `2*Mz0*(2*Mz0**2*alpha212 + P0**2*alpha139 + alpha47)`
- `beta24` = `4*Mz0*(5*Mz0**2*alpha211 + P0**2*alpha138 + alpha46)`
- `beta25` = `Mz0*(Mz0**2*alpha146 + 3*P0**2*alpha121 + alpha29)`
- `beta26` = `Mz0*(Mz0**2*alpha149 + 3*P0**2*alpha122 + alpha30)`
- `beta27` = `Mz0**4*alpha246 + Mz0**2*P0**2*alpha227 + Mz0**2*alpha54 + P0**4*alpha223 + P0**2*alpha50 + alpha9`
- `beta28` = `Mz0**4*alpha272 + 6*Mz0**2*P0**2*alpha253 + Mz0**2*alpha60 + 15*P0**4*alpha249 + 6*P0**2*alpha56 + alpha10`
- `beta29` = `Mz0**4*alpha314 + Mz0**2*P0**2*alpha261 + Mz0**2*alpha68 + P0**4*alpha250 + P0**2*alpha57 + alpha11`
- `beta30` = `Mz0**4*alpha327 + Mz0**2*P0**2*alpha265 + Mz0**2*alpha72 + P0**4*alpha251 + P0**2*alpha58 + alpha12`
- `beta31` = `Mz0**4*alpha339 + Mz0**2*P0**2*alpha269 + Mz0**2*alpha76 + P0**4*alpha252 + P0**2*alpha59 + alpha13`
- `beta32` = `Mz0**4*alpha346 + Mz0**2*P0**2*alpha273 + Mz0**2*alpha80 + P0**4*alpha254 + P0**2*alpha61 + alpha15`
- `beta33` = `4*Mz0*P0*(2*Mz0**2*alpha272 + 2*P0**2*alpha253 + alpha60)`
- `beta34` = `Mz0*P0*(Mz0**2*alpha280 + P0**2*alpha255 + alpha62)`
- `beta35` = `Mz0*P0*(Mz0**2*alpha283 + P0**2*alpha256 + alpha63)`
- `beta36` = `P0*(3*Mz0**2*alpha146 + P0**2*alpha121 + alpha29)`
- `beta37` = `P0*(3*Mz0**2*alpha149 + P0**2*alpha122 + alpha30)`
- `beta38` = `2*P0*(6*Mz0**2*alpha138 + 2*P0**2*alpha119 + alpha27)`
- `beta39` = `4*P0*(Mz0**2*alpha119 + 5*P0**2*alpha115 + alpha23)`
- `beta40` = `2*P0*(Mz0**2*alpha127 + 2*P0**2*alpha116 + alpha24)`
- `beta41` = `2*P0*(Mz0**2*alpha131 + 2*P0**2*alpha117 + alpha25)`
- `beta42` = `2*P0*(Mz0**2*alpha135 + 2*P0**2*alpha118 + alpha26)`
- `beta43` = `2*P0*(Mz0**2*alpha139 + 2*P0**2*alpha120 + alpha28)`
- `beta44` = `2*P0*(Mz0**2*alpha93 + 2*P0**2*alpha89 + alpha17)`

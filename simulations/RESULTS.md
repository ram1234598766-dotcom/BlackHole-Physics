# Partitionism - simulation results

Generated 2026-10-09 by `python3 -m simulations.run_all`.

Pure Python, no dependencies.  All quantities are exact within the stated tolerances; every random-unitary run uses a fixed seed so the numbers are reproducible.

## 0. Validation of the numerical machinery

```
Hermitian eigensolver, H = [[1, i], [-i, 2]]
  computed [0.38196601125, 2.61803398875]
  exact    [0.38196601125, 2.61803398875]
  max error = 1.110e-16
bit spreading: consistent
pure-state bipartition identity S(A)=S(B), max error over n=4,6,8,10 and all splits: 1.776e-15
reduced rho: max |trace-1| = 8.882e-16, most negative eigenvalue = 6.990e-17
random block unitary: 34 blocks tested on registers of 2-5 qubits,
  max change of norm = 5.551e-16
product state |000> under a random 3-qubit unitary: S(qubit 0) = 0.4058 nats

all validation checks pass
```

## 1. The evaporation ledger

```
========================================================================
TEST 1 - the evaporation ledger
========================================================================
random-unitary (Householder) ensemble, 3 trials per size

A. PURE MICROSTATE SENDER  (Partitionism: ledger respected)
------------------------------------------------------------------------

  simulated S(rad)/ln2 (average over trials) vs. Page's formula
  n0= 4 |  0.00  0.76  1.34  0.88  0.00
  n0= 6 |  0.00  0.96  1.85  2.33  1.78  0.97  0.00
  n0= 8 |  0.00  1.00  1.97  2.83  3.27  2.80  1.95  0.98  0.00
  n0=10 |  0.00  1.00  1.99  2.95  3.82  4.26  3.82  2.96  1.99  1.00  0.00
  Page   4 | -0.05  0.82  1.28  0.82 -0.05
  Page   6 | -0.01  0.95  1.82  2.28  1.82  0.95 -0.01
  Page   8 | -0.00  0.99  1.95  2.82  3.28  2.82  1.95  0.99 -0.00
  Page  10 | -0.00  1.00  1.99  2.95  3.82  4.28  3.82  2.95  1.99  1.00 -0.00

B. THERMAL SENDER WITH PURIFIER  (Partitionism: ledger blind)
------------------------------------------------------------------------
  n0=6 (register 12 qubits, purifier traced out)
   m | S(rad)/ln2 | I(R:Rad)/ln2 | I(R:Rem)/ln2 | sum/ln2
   1 |     1.0000 |       2.0000 |      10.0000 |  12.0000
   2 |     2.0000 |       4.0000 |       8.0000 |  12.0000
   3 |     3.0000 |       6.0000 |       6.0000 |  12.0000
   4 |     4.0000 |       8.0000 |       4.0000 |  12.0000
   5 |     5.0000 |      10.0000 |       2.0000 |  12.0000
   6 |     6.0000 |      12.0000 |      -0.0000 |  12.0000
  purifier entropy S(R)/ln2 = 6
  -> the purifier's mutual information with the two channels is
     transferred one-for-one:  I(R:Rad) + I(R:Rem) = const.

  note: the S(rad) column is the *ledger-blind* curve.  An observer
  who also has access to R follows the Page curve instead.
```

## 2. Quantised payout

```
========================================================================
TEST 2 - quantised payout: the evaporation staircase
========================================================================
area quantum   ΔA = 4 ln2 ℓ_P² = 7.242779e-70 m²
one quantum of entropy = k_B ln 2 = 9.569930e-24 J/K

Q1  the Page time moves from n0/2 to the first integer m >= n0 - m
------------------------------------------------------------------------
   n0 |  smooth m*  quantised m* | shift Δm | ΔS at m* (bits)
      2 |       1.0           1 |     0.00 |     0.00
      3 |       1.5           2 |     0.50 |    -0.50
      4 |       2.0           2 |     0.00 |     0.00
      5 |       2.5           3 |     0.50 |    -0.50
      9 |       4.5           5 |     0.50 |    -0.50
     10 |       5.0           5 |     0.00 |     0.00
     11 |       5.5           6 |     0.50 |    -0.50
     16 |       8.0           8 |     0.00 |     0.00
    101 |      50.5          51 |     0.50 |    -0.50
   1000 |     500.0         500 |     0.00 |     0.00
  10000 |    5000.0        5000 |     0.00 |     0.00

  the shift is at most half a quantum: Δm <= 1/2 for every n0.
  an odd number of quanta always pays out the last half-quantum early.

Q2  granularity of the staircase
------------------------------------------------------------------------
  The entropy of the radiation is not a continuous function of the
  emitted mass: it can only take values that are multiples of k_B ln 2,
  because each step of the ladder is one area quantum.  Two consequences.

  N quanta   granularity 1/N   max Δm (quanta)    max Δt/t
        10          1.00e-01              0.50   7.500e-02
       100          1.00e-02              0.50   7.500e-03
      1000          1.00e-03              0.50   7.500e-04
     10000          1.00e-04              0.50   7.500e-05
   1000000          1.00e-06              0.50   7.500e-07
10000000000          1.00e-10              0.50   7.500e-11
10000000000000000000000000000000000000000          1.00e-40              0.50   7.500e-41
100000000000000000000000000000000000000000000000000000000000000000000000000000          1.00e-77              0.50   7.500e-78

  the largest possible misplacement of the Page time is half a quantum;
  in time that is Δt/t = (3/4)/N, i.e. utterly negligible for any
  astrophysical black hole and finite for the small ones.

Q2b the shape of the ladder for a hole with only a few quanta
------------------------------------------------------------------------
     N    0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30   31   32   33   34   35   36   37   38   39   40
     5    0    1    2    2    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0
    10    0    1    2    3    4    5    4    3    2    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0
    20    0    1    2    3    4    5    6    7    8    9   10    9    8    7    6    5    4    3    2    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0
    40    0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   19   18   17   16   15   14   13   12   11   10    9    8    7    6    5    4    3    2    1    0

  values are S/k_B ln 2, i.e. bits.  A hole with a handful of area
  quanta has a Page curve that is a tent over a few steps - there is no
  'smooth' Page curve left to talk about.  That is the endpoint regime,
  and it is the only regime in which the staircase is not suppressed.
Q3  how many quanta do real systems have, and how big is the shift
------------------------------------------------------------------------
object                              mass (kg)    N quanta        Δt/t
solar-mass black hole               1.988e+30   1.513e+77   4.956e-78
Sgr A* (4.3e6 M☉)                   8.550e+36   2.798e+90   2.680e-91
M87* (6.5e9 M☉)                     1.293e+40   6.394e+96   1.173e-97
primordial BH, 10^12 kg             1.000e+12   3.827e+40   1.960e-41
Planck mass                         2.176e-08   1.813e+01   4.137e-02

  a Planck-mass hole - the endpoint of evaporation - carries about 18
  area quanta, so its Page curve is a tent of roughly eighteen steps
  and its Page time is misplaced by about 4%.  For any astrophysical
  black hole the same quantity is 1e-78.

Q4  analog horizons - the size of the last quantised stage
------------------------------------------------------------------------
  Here the 'Planck length' is set by the condensate healing length ξ.
  N quanta counts the horizon area in units of 4 ln2 ξ².
  R (µm)   ξ (µm)    N quanta last 10 quanta / lifetime
     5.0     0.30      1259.0                     0.008
    10.0     0.30      5036.0                     0.002
    20.0     0.30     20143.8                     0.000
    10.0     0.50      1812.9                     0.006

  If the interface is quantised at the analog Planck scale, the final
  quantised stage of an analog horizon is a finite, non-negligible
  fraction of its life, and is the honest place to look for the
  staircase.  For astrophysical black holes the effect is 1e-77.
```

## 3. Readout degeneracy

```
========================================================================
TEST 3 - Conjecture R: readout degeneracy (the saturated ball)
========================================================================

R1  what the readout reports as q → 1 (i.e. 'as r → 0')
------------------------------------------------------------------------
           q           u    S/Smax      g^E_uu       du/dq     K_readout
    0.500000      0.6931  0.500000   5.000e-01   2.000e+00     4.000e+00
    0.900005      2.3026  0.900005   9.999e-02   1.000e+01     1.000e+02
    0.990000      4.6051  0.990000   1.000e-02   1.000e+02     9.999e+03
    0.999000      6.9078  0.999000   1.000e-03   1.000e+03     1.000e+06
    0.999900      9.2104  0.999900   9.999e-05   1.000e+04     1.000e+08
    0.999990     11.5129  0.999990   1.000e-05   1.000e+05     9.999e+09
    0.999999     13.8155  0.999999   1.000e-06   1.000e+06     1.000e+12

  the readout curvature diverges: K ∝ (1-q)^-2, unbounded.

R2  what the substrate reports at the same values
------------------------------------------------------------------------
  total entropy of the ball          S_max                = 1.000000
  total entropy flux ∫ (dS/du) du                          = 1.000000
  total substrate length ∫ sqrt(g^E_uu) du (numeric)        = 1.999999
  total substrate length ∫ sqrt(g^E_uu) du (exact)         = 2.000000
  absolute difference (tail beyond u=30 is 6.12e-07)     = 6.11e-07

  every substrate invariant is finite and bounded.  There is no
  substrate-level divergence anywhere on this curve.

R3  the entanglement across the cut (the Bekenstein bound in action)
------------------------------------------------------------------------
         q    S(cut) / S_max  capacity used
  0.500000          0.500000       0.500000
  0.900005          0.900005       0.900005
  0.990000          0.990000       0.990000
  0.999000          0.999000       0.999000
  0.999999          0.999999       0.999999

  as q → 1 the cut saturates: S(cut) → S_max and no further
  refinement is possible.  This is what stops the compression, and
  it is a statement about information, not about forces.

R4  comparison with the classical Schwarzschild singularity
------------------------------------------------------------------------
  Schwarzschild radius of the Sun            r_s   = 2.9533e+03 m
  proper distance r_s → 0 (numeric)          L     = 4.635100e+03 m
  proper distance r_s → 0 (exact, π r_s / 2)        = 4.639095e+03 m
  ratio L / r_s (numeric 1.5694, exact π/2 = 1.5708)
  Kretschmann at r = r_s/2                          = 1.0095e-11
  Kretschmann at r = r_s/10                         = 1.5773e-07

  the classical solution has exactly the same shape: a *coordinate*
  quantity (Kretschmann) diverges while a *proper* quantity (distance
  to the centre) stays finite.  Conjecture R says the divergence is a
  property of the readout's Jacobian du/dq, and that keeping it while
  the substrate stays finite is the whole content of 'the theory
  breaks down at r = 0'.

  NOTE: the framework does *not* claim to reproduce the Schwarzschild
  exponent (K ∝ r^-6) until the map q(r) is derived; that derivation
  is open problem O2 of the main document.
```


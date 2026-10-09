# Partitionism - simulation suite

Pure Python (standard library only, no numpy).  Run from the repository root:

```
python3 -m simulations.run_all
```

This writes `simulations/RESULTS.md` and prints the same text.  Individual
tests can be run on their own:

```
python3 -m simulations.validation      # checks the numerical machinery itself
python3 -m simulations.test_ledger     # the evaporation ledger / Page curve
python3 -m simulations.test_quantization   # quantised payout, Page-time shift
python3 -m simulations.test_readout    # Conjecture R, readout degeneracy
```

`test_ledger` accepts `--nmax` (largest register, default 10) and `--trials`.

## What each file contains

| file | what it tests | method |
|---|---|---|
| `validation.py` | that the numerics are correct: Hermitian eigensolver, partial trace, bit spreading, norm preservation of the block unitary | comparison with exact results |
| `quantum.py` | shared utilities: Haar-random block unitaries (Householder), partial trace, von Neumann entropy | — |
| `constants.py` | CODATA 2018 constants and the standard black-hole formulae | — |
| `test_ledger.py` | **L1** the radiation's entropy is bounded by the smaller channel capacity, and turns over where the two capacities cross; **L2** the two channels share their entropy (no duplication); **L3** the monotonic "thermal" curve is the ledger-blind model | exact random-unitary circuits on pure states, registers up to 10 qubits |
| `test_quantization.py` | **Q1** the quantised Page time moves by at most half a quantum; **Q2** the granularity of the staircase; **Q3** how many area quanta real objects have; **Q4** the size of the last quantised stage for analog horizons | capacity counting, plus real physical constants |
| `test_readout.py` | **Conjecture R**: the readout curvature diverges while every substrate invariant stays finite | the saturated-ball model, numerically integrated and compared with exact values |

## Reproducibility

Every random-unitary run uses a fixed seed (`random.Random(...)`), so the
printed numbers are reproducible bit-for-bit.  The machinery is validated
first (see section 0 of `RESULTS.md`); if any of those checks fails, the
suite raises rather than reporting physics.

## Honest scope

These simulations test the *internal consistency and quantitative
consequences* of Partitionism's claims in controlled quantum systems.  They
do not show that the information substrate exists, and they are not
observational tests of black holes.

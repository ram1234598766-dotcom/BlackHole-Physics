"""Partitionism test 1: the evaporation ledger.

Two models of the same random-unitary evaportation dynamics:

  A.  Pure-microstate sender (Page's model).  The collapsed matter starts in a
      single random pure state of ``n0`` qubits; each step applies a Haar-random
      unitary to everything still inside the horizon and then peels one qubit
      off into the radiation.

  B.  Thermal sender with purifier.  The collapsed matter starts maximally
      mixed - implemented explicitly by entangling it with a reference register
      R that the observer never sees.  Same dynamics, different initial
      ledger.

Partitionism's claims under test:

  L1  the radiation's entropy is bounded by the *smaller* of the two channel
      capacities, S <= min(m, n0-m) ln2  - which is the Page curve, and whose
      turnover sits exactly where the two capacities cross;
  L2  the entropy of the radiation equals the entropy of what remains (pure
      global state) - the two channels *share* their entropy, they do not
      duplicate it;
  L3  the monotonic ("Hawking") curve is the *ledger-blind* model: it is what
      you get by throwing away the purifier, i.e. by assuming the initial
      ledger is full and never returned.

Run:  python3 -m simulations.test_ledger [--nmax 8] [--trials 3]
"""

import argparse
import math
import random
from statistics import mean, pstdev

from .quantum import apply_random_unitary, subsystem_entropy, LN2


def random_pure_state(n, rng):
    psi = [complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)) for _ in range(1 << n)]
    norm = math.sqrt(sum(abs(a) ** 2 for a in psi))
    return [a / norm for a in psi]


def run_pure(n0, rng):
    """Model A.  Returns (curve, purity_error, bound_error).

    ``purity_error`` is the largest mismatch between the entropy of the
    radiation and the entropy of what remains, which must vanish for a pure
    global state.  ``bound_error`` is the largest violation of the capacity
    bound S <= min(m, n0-m) ln2.
    """
    psi = random_pure_state(n0, rng)
    curve = [0.0]
    purity = 0.0
    bound = 0.0
    for t in range(1, n0 + 1):
        m = t - 1
        apply_random_unitary(psi, m, n0, rng)      # scramble what is inside
        s_rad = subsystem_entropy(psi, n0, list(range(t)))   # rad = [0,t)
        s_rem = subsystem_entropy(psi, n0, list(range(t, n0)))
        curve.append(s_rad)
        purity = max(purity, abs(s_rad - s_rem))
        bound = max(bound, s_rad - min(t, n0 - t) * LN2)
    return curve, purity, bound


def run_thermal(n0, rng):
    """Model B.  Register = R (n0 qubits) + BH/Rad (n0 qubits).

    R is Bell-paired with the BH register initially and never touched again.
    Returns (curve, i_rad, i_rem, sum_i) where i_* are mutual informations
    between R and each channel.
    """
    n = 2 * n0
    psi = [0j] * (1 << n)
    amp = 1.0 / math.sqrt(1 << n0)
    for i in range(1 << n0):
        psi[(i << n0) | i] = amp          # R bits = i, BH bits = i  (Bell)
    s_r = n0 * LN2                       # never changes: S(R) is invariant
    curve = [0.0]
    i_rad = [0.0]
    i_rem = [s_r]
    for t in range(1, n0 + 1):
        m = t - 1
        lo = n0 + m                        # first still-inside qubit
        apply_random_unitary(psi, lo, n, rng)
        rad = list(range(n0, n0 + t))       # emitted qubits
        rem = list(range(n0 + t, n))       # still-inside qubits
        s_rad = subsystem_entropy(psi, n, rad)
        s_rem = subsystem_entropy(psi, n, rem)
        curve.append(s_rad)
        i_rad.append(s_r + s_rad - s_rem)   # I(R:Rad) = S(R)+S(Rad)-S(Rem)
        i_rem.append(s_r + s_rem - s_rad)   # I(R:Rem) = S(R)+S(Rem)-S(Rad)
    return curve, i_rad, i_rem


def analytic_page(m, n0):
    """Average entropy of an m-qubit subsystem of a random pure n0-qubit state.

    Page's formula:  S ~ m ln2 - 2**m / (2 * 2**(n0-m)), valid for m <= n0/2.
    """
    total = n0
    d_a = 1 << m
    d_b = 1 << (total - m)
    # leading correction term, symmetrised via the smaller side
    small = min(m, total - m)
    frac = d_a if m <= total - m else d_b
    denom = 1 << (total - small)
    return small * LN2 - frac / (2.0 * denom)


def main():
    out = []
    p = out.append
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--thermal-n", type=int, default=6)
    args = ap.parse_args()

    p("=" * 72)
    p("TEST 1 - the evaporation ledger")
    p("=" * 72)
    p(f"random-unitary (Householder) ensemble, {args.trials} trials per size")
    p("")
    p("A. PURE MICROSTATE SENDER  (Partitionism: ledger respected)")
    p("-" * 72)
    print(f"{'n0':>4} {'max S/ln2':>11} {'bound':>7} {'bound viol.':>12} "
          f"{'turn over':>10} {'n0/2':>7} {'S(rem)-S(rad)':>16}")
    summary = {}
    for n0 in range(4, args.nmax + 1, 2):
        curves = []
        worst_bound = 0.0
        worst_purity = 0.0
        for k in range(args.trials):
            rng = random.Random(1000 * n0 + k)
            curve, pur, bnd = run_pure(n0, rng)
            curves.append(curve)
            worst_bound = max(worst_bound, bnd)
            worst_purity = max(worst_purity, pur)
        avg = [mean(c[m] for c in curves) for m in range(n0 + 1)]
        # turnover: first m after which the curve decreases
        turn = max(range(n0 + 1), key=lambda m: avg[m])
        summary[n0] = avg
        print(f"{n0:>4} {max(avg)/LN2:>11.4f} "
              f"{min(n0//2, n0-n0//2):>7} {worst_bound:>12.2e} "
              f"{turn:>10} {n0/2:>7.2f} {worst_purity:>16.2e}")

    p("")
    p("  simulated S(rad)/ln2 (average over trials) vs. Page's formula")
    for n0, avg in summary.items():
        row = "  n0=%2d | " % n0
        row += " ".join(f"{avg[m]/LN2:5.2f}" for m in range(n0 + 1))
        p(row)
    for n0, avg in summary.items():
        row = "  Page  %2d | " % n0
        row += " ".join(f"{analytic_page(m, n0)/LN2:5.2f}"
                        for m in range(n0 + 1))
        p(row)

    p("")
    p("B. THERMAL SENDER WITH PURIFIER  (Partitionism: ledger blind)")
    p("-" * 72)
    n0 = args.thermal_n
    rng = random.Random(4242)
    curve, i_rad, i_rem = run_thermal(n0, rng)
    p(f"  n0={n0} (register {2*n0} qubits, purifier traced out)")
    p("   m | S(rad)/ln2 | I(R:Rad)/ln2 | I(R:Rem)/ln2 | sum/ln2")
    for m in range(1, n0 + 1):
        tot = (i_rad[m] + i_rem[m]) / LN2
        p(f"  {m:2d} | {curve[m]/LN2:10.4f} | {i_rad[m]/LN2:12.4f} | "
          f"{i_rem[m]/LN2:12.4f} | {tot:8.4f}")
    p(f"  purifier entropy S(R)/ln2 = {n0}")
    p("  -> the purifier's mutual information with the two channels is")
    p("     transferred one-for-one:  I(R:Rad) + I(R:Rem) = const.")
    p("")
    p("  note: the S(rad) column is the *ledger-blind* curve.  An observer")
    p("  who also has access to R follows the Page curve instead.")


    return "\n".join(out)


if __name__ == "__main__":
    print(main())
"""Partitionism test 2: the quantised payout.

Prediction P1 of the framework: the radiation's entropy does not follow the
smooth Page curve, it follows a *staircase* - one logical qunit (k_B ln 2) per
area quantum ΔA = 4 ln 2 ℓ_P²  (the Bekenstein-Mukhanov spacing that also
saturates Landauer's bound: Bagchi, Ghosh & Sen, Gen. Relativ. Gravit. 56, 108
(2024), arXiv:2408.02077).

The mechanism is capacity saturation, not dynamics.  Test 1 established that
the radiation's entropy is bounded by the *smaller* of the two channel
capacities:

    S(rad) <= min( n_rad , n_bh ) * ln2

which is the Page curve, and whose turnover is where the two capacities
cross.  This script replaces the continuous capacities by the quantised ones
and measures what changes:

    Q1  the turnover moves from n0/2 to the first integer with m >= n0 - m;
    Q2  the largest deviation from the smooth curve, in bits and in units of
        m (i.e. in area quanta);
    Q3  the physical size of the effect for real black holes and for analog
        horizons, where the "Planck length" is the healing length.

Run:  python3 -m simulations.test_quantization
"""

import math

from .constants import G, C, HBAR, K_B, L_P, M_SUN, LN2

DELTA_A = 4.0 * LN2 * L_P ** 2        # area quantum, one bit of entropy


def smooth_page(m, total):
    """Continuous-capacity Page curve: min(m, total-m) bits."""
    return min(m, total - m)


def quantised_page(m, total):
    """Quantised capacity Page curve: capacities count whole area quanta."""
    n_rad = m                            # area quanta emitted
    n_bh = max(0, total - m)             # area quanta still out there
    return min(n_rad, n_bh)


def area_quanta(mass_kg):
    """Number of area quanta of a Schwarzschild black hole."""
    r_s = 2.0 * G * mass_kg / C ** 2
    area = 4.0 * math.pi * r_s ** 2
    return area / DELTA_A


def run_tests():
    out = []
    p = out.append

    p("=" * 72)
    p("TEST 2 - quantised payout: the evaporation staircase")
    p("=" * 72)
    p(f"area quantum   ΔA = 4 ln2 ℓ_P² = {DELTA_A:.6e} m²")
    p(f"one quantum of entropy = k_B ln 2 = {K_B*LN2:.6e} J/K")
    p("")

    # ---- Q1: where does the Page time move to? -------------------------
    p("Q1  the Page time moves from n0/2 to the first integer m >= n0 - m")
    p("-" * 72)
    p("   n0 |  smooth m*  quantised m* | shift Δm | ΔS at m* (bits)")
    for n0 in (2, 3, 4, 5, 9, 10, 11, 16, 101, 1000, 10 ** 4):
        m_smooth = n0 / 2.0
        m_q = next(m for m in range(n0 + 1) if m >= n0 - m)
        d_s = min(m_smooth, n0 - m_smooth)
        d_q = min(m_q, n0 - m_q)
        p(f" {n0:>6} | {m_smooth:9.1f} {m_q:>11} | {m_q - m_smooth:8.2f} | "
          f"{d_q - d_s:8.2f}")
    p("")
    p("  the shift is at most half a quantum: Δm <= 1/2 for every n0.")
    p("  an odd number of quanta always pays out the last half-quantum early.")
    p("")

    # ---- Q2: worst-case deviation from the smooth curve ----------------
    p("Q2  granularity of the staircase")
    p("-" * 72)
    p("  The entropy of the radiation is not a continuous function of the")
    p("  emitted mass: it can only take values that are multiples of k_B ln 2,")
    p("  because each step of the ladder is one area quantum.  Two consequences.")
    p("")
    p(f"{'N quanta':>10}{'granularity 1/N':>18}{'max Δm (quanta)':>18}"
      f"{'max Δt/t':>12}")
    for n0 in (10, 100, 1000, 10 ** 4, 10 ** 6, 10 ** 10, 10 ** 40, 10 ** 77):
        # N = A/ΔA ∝ M², so M ∝ N^(1/2) and t ∝ M³ ∝ N^(3/2).
        # A half-quantum misplacement of the Page time is a relative shift
        # of 1/N in the remaining mass, hence Δt/t = (3/2)/N.
        dt_over_t = 1.5 / n0
        p(f"{n0:>10}{1.0/n0:18.2e}{0.5:18.2f}{dt_over_t:12.3e}")
    p("")
    p("  the largest possible misplacement of the Page time is half a quantum;")
    p("  since N = A/ΔA ∝ M² and t ∝ M³, that is Δt/t = 3/(2N) in time,")
    p("  which is utterly negligible for any")
    p("  astrophysical black hole and finite for the small ones.")
    p("")
    p("Q2b the shape of the ladder for a hole with only a few quanta")
    p("-" * 72)
    p(f"{'N':>6}" + "".join(f"{m:>5}" for m in range(41)))
    for n0 in (5, 10, 20, 40):
        row = "".join(f"{quantised_page(m, n0):>5}" for m in range(41))
        p(f"{n0:>6}{row}")
    p("")
    p("  values are S/k_B ln 2, i.e. bits.  A hole with a handful of area")
    p("  quanta has a Page curve that is a tent over a few steps - there is no")
    p("  'smooth' Page curve left to talk about.  That is the endpoint regime,")
    p("  and it is the only regime in which the staircase is not suppressed.")
    # ---- Q3: physical magnitudes --------------------------------------
    p("Q3  how many quanta do real systems have, and how big is the shift")
    p("-" * 72)
    p(f"{'object':<34}{'mass (kg)':>11}{'N quanta':>12}{'Δt/t':>12}")
    cases = [
        ("solar-mass black hole", M_SUN),
        ("Sgr A* (4.3e6 M☉)", 4.3e6 * M_SUN),
        ("M87* (6.5e9 M☉)", 6.5e9 * M_SUN),
        ("primordial BH, 10^12 kg", 1e12),
        ("Planck mass", 2.176434e-8),
    ]
    for name, mass in cases:
        n = area_quanta(mass)
        # N = A/ΔA ∝ M² and t ∝ M³, so a half-quantum misplacement of the
        # Page time is Δt/t = (3/2)/N
        dt = 1.5 / n if n > 1 else float("nan")
        p(f"{name:<34}{mass:11.3e}{n:12.3e}{dt:12.3e}")
    p("")
    p("  a Planck-mass hole - the endpoint of evaporation - carries exactly")
    p("  N = 4 pi / ln 2 = 18.13 area quanta, so its Page curve is a tent of")
    p("  about eighteen steps and its Page time is misplaced by 3/(2N) = 8%.")
    p("  For any astrophysical black hole the same quantity is ~1e-77.")
    p("")

    # ---- Q4: the analog horizon, where the test is actually feasible ---
    p("Q4  analog horizons - the size of the last quantised stage")
    p("-" * 72)
    p("  Here the 'Planck length' is set by the condensate healing length ξ.")
    p("  N quanta counts the horizon area in units of 4 ln2 ξ².")
    p(f"{'R (µm)':>8}{'ξ (µm)':>9}{'N quanta':>12}"
      f"{'last 10 quanta / lifetime':>26}")
    for R_um, xi_um in [(5.0, 0.3), (10.0, 0.3), (20.0, 0.3), (10.0, 0.5)]:
        R = R_um * 1e-6
        xi = xi_um * 1e-6
        area = 4.0 * math.pi * R ** 2
        delta_a = 4.0 * LN2 * xi ** 2
        n = area / delta_a
        frac = 10.0 / n
        p(f"{R_um:8.1f}{xi_um:9.2f}{n:12.1f}{frac:26.3f}")
    p("")
    p("  If the interface is quantised at the analog Planck scale, the final")
    p("  quantised stage of an analog horizon is a finite, non-negligible")
    p("  fraction of its life, and is the honest place to look for the")
    p("  staircase.  For astrophysical black holes the effect is 1e-77.")
    return "\n".join(out)


if __name__ == "__main__":
    print(run_tests())

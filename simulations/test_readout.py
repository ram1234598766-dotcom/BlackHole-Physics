"""Partitionism test 3: Conjecture R - readout degeneracy.

The claim under test:

    A curvature singularity is not a property of the substrate.  It is the
    statement that the readout map from cut variables to metric components
    loses invertibility, i.e. that the entanglement Hessian

        g^E_μν = -∂²S_min / ∂x^μ ∂x^ν

    degenerates.  On the readout side every curvature invariant diverges; on
    the substrate side nothing diverges, because the saturation of the cut
    caps every quantity.

The saturated-ball model
------------------------
Let q ∈ [0,1) be the fraction of a cut's capacity in use and let the radial
readout coordinate be

    u = -ln(1 - q)      (so q → 1 pushes u → ∞)

with the ball's entropy the saturating function

    S(u) = S_max (1 - exp(-u/u0)) .

Then:

  *  dS/du = S_max exp(-u/u0)          -> 0   (entropy density in u dies)
  *  g^E_uu = -d²S/du² falls to 0            (the readout metric degenerates)
  *  du/dq = 1/(1-q) -> ∞                    (the readout's curvature blows
                                               up, K_readout ∝ 1/(1-q)²)
  *  every substrate invariant - total entropy, total "length"
     ∫√g^E_uu du, entanglement across the cut - stays finite.

Run:  python3 -m simulations.test_readout
"""

import math

from .constants import LN2


def saturated_ball(npts=200001, s_max=1.0, u0=1.0, u_max=30.0):
    """Sample the readout uniformly in u.

    u = -ln(1 - q) runs from 0 to u_max; the tail beyond u_max contributes
    O(exp(-u_max/2)) and is reported analytically.  Sampling uniformly in u
    (rather than uniformly in q) keeps the trapezium rule accurate.
    """
    rows = []
    du = u_max / npts
    for i in range(npts + 1):
        u = i * du
        q = 1.0 - math.exp(-u)                       # fraction of capacity used
        s = s_max * (1.0 - math.exp(-u / u0))        # entropy of the ball
        ds_du = s_max * math.exp(-u / u0) / u0
        d2s_du2 = -s_max * math.exp(-u / u0) / u0 ** 2
        g_uu = -d2s_du2                              # metric (sign convention)
        du_dq = 1.0 / (1.0 - q)                      # readout Jacobian
        rows.append(dict(q=q, u=u, s=s, ds_du=ds_du, g_uu=g_uu,
                         du_dq=du_dq, k_read=du_dq ** 2))
    return rows


def run_tests():
    out = []
    p = out.append
    p("=" * 72)
    p("TEST 3 - Conjecture R: readout degeneracy (the saturated ball)")
    p("=" * 72)

    rows = saturated_ball()
    s_max, u0 = 1.0, 1.0
    du = rows[1]["u"] - rows[0]["u"]

    p("")
    p("R1  what the readout reports as q → 1 (i.e. 'as r → 0')")
    p("-" * 72)
    p(f"{'q':>12}{'u':>12}{'S/Smax':>10}{'g^E_uu':>12}"
      f"{'du/dq':>12}{'K_readout':>14}")
    for q_target in (0.5, 0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999):
        row = min(rows, key=lambda r: abs(r["q"] - q_target))
        p(f"{row['q']:12.6f}{row['u']:12.4f}{row['s']/s_max:10.6f}"
          f"{row['g_uu']:12.3e}{row['du_dq']:12.3e}{row['k_read']:14.3e}")
    p("")
    p("  the readout curvature diverges: K ∝ (1-q)^-2, unbounded.")
    p("")

    p("R2  what the substrate reports at the same values")
    p("-" * 72)
    # substrate invariants, integrated over the uniform u grid
    length = 0.0        # ∫ sqrt(g^E_uu) du   = 2 sqrt(S_max) u0  (exact)
    entropy_flux = 0.0  # ∫ (dS/du) du        = S_max             (exact)
    for a, b in zip(rows, rows[1:]):
        length += 0.5 * (math.sqrt(a["g_uu"]) + math.sqrt(b["g_uu"])) * du
        entropy_flux += 0.5 * (a["ds_du"] + b["ds_du"]) * du
    length_exact = 2.0 * math.sqrt(s_max) * u0
    tail = 2.0 * math.sqrt(s_max) * u0 * math.exp(-rows[-1]["u"] / (2 * u0))
    p(f"  total entropy of the ball          S_max                = {s_max:.6f}")
    p(f"  total entropy flux ∫ (dS/du) du                          = "
      f"{entropy_flux:.6f}")
    p(f"  total substrate length ∫ sqrt(g^E_uu) du (numeric)        = "
      f"{length:.6f}")
    p(f"  total substrate length ∫ sqrt(g^E_uu) du (exact)         = "
      f"{length_exact:.6f}")
    p(f"  absolute difference (tail beyond u=30 is {tail:.2e})     = "
      f"{abs(length - length_exact):.2e}")
    p("")
    p("  every substrate invariant is finite and bounded.  There is no")
    p("  substrate-level divergence anywhere on this curve.")
    p("")

    p("R3  the entanglement across the cut (the Bekenstein bound in action)")
    p("-" * 72)
    p(f"{'q':>10}{'S(cut) / S_max':>18}{'capacity used':>15}")
    for q_target in (0.5, 0.9, 0.99, 0.999, 0.999999):
        row = min(rows, key=lambda r: abs(r["q"] - q_target))
        p(f"{row['q']:10.6f}{row['s']/s_max:18.6f}{row['q']:15.6f}")
    p("")
    p("  as q → 1 the cut saturates: S(cut) → S_max and no further")
    p("  refinement is possible.  This is what stops the compression, and")
    p("  it is a statement about information, not about forces.")
    p("")

    p("R4  comparison with the classical Schwarzschild singularity")
    p("-" * 72)
    from .constants import G, C, M_SUN
    rs = 2.0 * G * M_SUN / C ** 2
    # proper radial distance from r_s to r=0 in Schwarzschild (finite).
    # Inside the horizon t and r swap roles: the radial proper metric is
    # dr^2 / (r_s/r - 1), so the integrand is 1/sqrt(r_s/r - 1).
    steps = 200000
    dist = 0.0
    for i in range(steps):
        r = rs * (i + 0.5) / steps          # midpoint, r in (0, rs)
        integrand = 1.0 / math.sqrt(rs / r - 1.0)
        dist += integrand * (rs / steps)
    p(f"  Schwarzschild radius of the Sun            r_s   = {rs:.4e} m")
    p(f"  proper distance r_s → 0 (numeric)          L     = {dist:.6e} m")
    p(f"  proper distance r_s → 0 (exact, π r_s / 2)        = "
      f"{math.pi * rs / 2:.6e} m")
    p(f"  ratio L / r_s (numeric {dist/rs:.4f}, exact π/2 = "
      f"{math.pi/2:.4f})")
    p(f"  Kretschmann at r = r_s/2                          = "
      f"{48*G**2*M_SUN**2/(C**4*(rs/2)**6):.4e}")
    p(f"  Kretschmann at r = r_s/10                         = "
      f"{48*G**2*M_SUN**2/(C**4*(rs/10)**6):.4e}")
    p("")
    p("  the classical solution has exactly the same shape: a *coordinate*")
    p("  quantity (Kretschmann) diverges while a *proper* quantity (distance")
    p("  to the centre) stays finite.  Conjecture R says the divergence is a")
    p("  property of the readout's Jacobian du/dq, and that keeping it while")
    p("  the substrate stays finite is the whole content of 'the theory")
    p("  breaks down at r = 0'.")
    p("")
    p("  NOTE: the framework does *not* claim to reproduce the Schwarzschild")
    p("  exponent (K ∝ r^-6) until the map q(r) is derived; that derivation")
    p("  is open problem O2 of the main document.")
    return "\n".join(out)


if __name__ == "__main__":
    print(run_tests())

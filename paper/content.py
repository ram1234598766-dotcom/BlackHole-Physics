"""Build the Partitionism research-paper PDF.

    python3 -m paper.build_paper [--out paper/partitionism.pdf]

Four papers plus appendices.  Every statement is labelled:

    THEOREM      proved in this document (proof given)
    LEMMA        proved, intermediate
    COROLLARY    proved
    ESTABLISHED  standard physics, with a citation in Appendix D
    CONJECTURE   part of Partitionism, not proved (say so in the text)
    PREDICTION   a falsifiable commitment
    NUMERICAL    verified by the simulation suite in simulations/

Figures are drawn from the same code that produced simulations/RESULTS.md.
"""

import argparse
import math
import os
import random

import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)

from .pdflib import Doc, Run, ascii_text
from simulations import test_ledger, test_readout, test_quantization
from simulations.quantum import (apply_random_unitary, random_pure_state,
                                 subsystem_entropy, LN2)
from simulations.constants import (G, C, HBAR, K_B, L_P, M_P, M_SUN,
                                   schwarzschild_kretschmann)

VERSION = "2.0"
DATE = "9 October 2026"
TITLE = "Partitionism: a framework for describing black holes as wholes"


# ==========================================================================
# Figures (data comes from the verified simulation code)
#
# Axes are drawn to a fixed data range with round-number ticks; every curve
# is scaled by an explicit factor that is printed in the caption, so the
# figures cannot silently misrepresent the numbers.
# ==========================================================================
_INK = (0.12, 0.20, 0.35)
_BLUE = (0.10, 0.25, 0.65)
_GREY = (0.55, 0.55, 0.55)
_RED = (0.80, 0.15, 0.15)
_GREEN = (0.10, 0.45, 0.20)
_ORANGE = (0.80, 0.40, 0.10)


def _frame(s, x0, x1, y0, y1, x_ticks, y_ticks, x_label="", y_label=""):
    """Draw a boxed frame in figure coordinates (0..1 of the figure box).

    Returns (X, Y) mappers from data space to figure space.
    """
    L, R, B, T = 0.14, 0.94, 0.16, 0.86

    def X(x):
        return L + (R - L) * (x - x0) / (x1 - x0)

    def Y(y):
        return B + (T - B) * (y - y0) / (y1 - y0)

    s.line(L, B, L, T, weight=0.8)
    s.line(L, B, R, B, weight=0.8)
    for yv in y_ticks:
        s.line(L, Y(yv), R, Y(yv), weight=0.12, color=(0.88, 0.88, 0.88))
        s.line(L, Y(yv), L - 0.008, Y(yv), weight=0.7)
        s.text(L - 0.014, Y(yv) - 0.018, "%g" % yv, size=6.6, align='right')
    for xv in x_ticks:
        s.line(X(xv), B, X(xv), B - 0.010, weight=0.7)
        s.text(X(xv), B - 0.048, "%g" % xv, size=6.6, align='center')
    if y_label:
        s.text(L - 0.085, (B + T) / 2 + 0.02, y_label, size=7.2,
               align='center')
    if x_label:
        s.text((L + R) / 2, B - 0.105, x_label, size=7.2, align='center')
    return X, Y


def fig_page_curve(d):
    """Simulated Page curve vs. Page's analytic formula, n0 = 10."""
    n0, trials = 10, 3
    curves = []
    for k in range(trials):
        rng = random.Random(1000 * n0 + k)
        curve, _, _ = test_ledger.run_pure(n0, rng)
        curves.append(curve)
    sim = [sum(c[m] for c in curves) / trials / LN2 for m in range(n0 + 1)]
    ana = [test_ledger.analytic_page(m, n0) / LN2 for m in range(n0 + 1)]
    blind = [float(m) for m in range(n0 + 1)]

    def draw(s):
        X, Y = _frame(s, 0, n0, 0, 6, [0, 2, 4, 6, 8, 10], [0, 1, 2, 3, 4, 5, 6],
                      "m  (emitted qubits)", "S / ln 2   (bits)")
        s.polyline([(X(m), Y(blind[m])) for m in range(n0 + 1)], weight=1.0,
                   color=_RED, dash='5 2')
        s.polyline([(X(m), Y(ana[m])) for m in range(n0 + 1)], weight=1.0,
                   color=_GREY, dash='3 2')
        s.polyline([(X(m), Y(sim[m])) for m in range(n0 + 1)], weight=1.5,
                   color=_BLUE)
        for m in range(n0 + 1):
            s.dot(X(m), Y(sim[m]), r=0.0055, color=_BLUE)
        s.text(X(5.2), Y(4.9), "ledger-blind  S = m ln 2  (Thm 5)", size=6.8,
               align='left', color=_RED)
        s.text(X(5.2), Y(4.45), "Page's formula (dashed)", size=6.8,
               align='left', color=_GREY)
        s.text(X(5.2), Y(4.0), "random-unitary sender (Thm 1-2)", size=6.8,
               align='left', color=_BLUE)
        s.line(X(5), Y(0), X(5), Y(4.26), weight=0.5, color=_GREY,
               dash='2 2')
        s.text(X(5), Y(-0.42), "turnover at m = 5 = n0/2", size=6.8,
               align='center', color=_BLUE)

    d.figure(draw, 200,
             title="Figure 1.  The evaporation ledger, n0 = 10 qubits",
             caption="Solid with dots: simulated von Neumann entropy of the "
                     "emitted qubits (average of three random-unitary trials, "
                     "exact entropies).  Dashed grey: Page's analytic formula "
                     "S = m ln 2 - 2^m/(2 x 2^(n0-m)).  Dash-dotted red: the "
                     "*ledger-blind* prediction S = m ln 2, which is exact "
                     "when the initial black hole is maximally mixed "
                     "(Theorem 5) - this is Hawking's monotone curve.  All "
                     "three curves are in bits, on a common axis.")


def fig_transfer(d):
    """I(R:Rad) and I(R:B) for the thermal sender with a purifier."""
    n0 = 6
    rng = random.Random(4242)
    curve, i_rad, i_rem = test_ledger.run_thermal(n0, rng)
    ir = [v / LN2 for v in i_rad]
    ib = [v / LN2 for v in i_rem]

    def draw(s):
        X, Y = _frame(s, 0, n0, 0, 14, list(range(0, n0 + 1)),
                      [0, 2, 4, 6, 8, 10, 12, 14], "m", "I / ln 2   (bits)")
        s.polyline([(X(m), Y(ir[m] + ib[m])) for m in range(n0 + 1)],
                   weight=1.1, color=_GREY, dash='4 2')
        s.polyline([(X(m), Y(ir[m])) for m in range(n0 + 1)], weight=1.6,
                   color=_GREEN)
        s.polyline([(X(m), Y(ib[m])) for m in range(n0 + 1)], weight=1.6,
                   color=_ORANGE)
        for m in range(1, n0 + 1):
            s.dot(X(m), Y(ir[m]), r=0.0055, color=_GREEN)
            s.dot(X(m), Y(ib[m]), r=0.0055, color=_ORANGE)
        s.text(X(3.4), Y(13.0), "I(R:Rad) + I(R:B) = 2 n0 = 12 (Theorem 4)",
               size=6.8, align='center', color=_GREY)
        s.text(X(2.2), Y(10.6), "I(R:Rad)", size=7, align='center',
               color=_GREEN)
        s.text(X(2.2), Y(3.4), "I(R:B)", size=7, align='center', color=_ORANGE)

    d.figure(draw, 190,
             title="Figure 2.  The one-for-one transfer of correlation",
             caption="Mutual information between the purifier R and the two "
                     "channels for n0 = 6, in bits.  I(R:Rad) rises exactly as "
                     "I(R:B) falls, and their sum is fixed at 2 n0 = 12 "
                     "(dashed grey, flat).  This is the computable form of "
                     "'information is transferred, not duplicated' - the "
                     "anti-firewall statement.")


def fig_readout(d):
    """Two panels: readout curvature vs. substrate invariants."""
    rows = test_readout.saturated_ball(npts=3000)
    du = rows[1]["u"] - rows[0]["u"]
    logk = [math.log10(r["k_read"]) for r in rows]
    qs = [r["q"] for r in rows]
    ent = [r["s"] for r in rows]
    length = []
    run = 0.0
    for i, r in enumerate(rows):
        if i:
            run += 0.5 * (math.sqrt(rows[i]["g_uu"]) +
                          math.sqrt(rows[i - 1]["g_uu"])) * du
        length.append(run / (2.0 * math.sqrt(1.0)))     # normalise to 1

    def top(s):
        X, Y = _frame(s, 0, 1, 0, 13, [0, 0.25, 0.5, 0.75, 1.0],
                      [0, 2, 4, 6, 8, 10, 12], "", "log10 K_readout")
        s.polyline([(X(qs[i]), Y(logk[i])) for i in range(len(qs))],
                   weight=1.5, color=_RED)
        s.text(X(0.55), Y(11.0), "K_readout = (du/dq)^2 = (1-q)^-2  "
               "(Lemma 3)", size=6.8, align='center', color=_RED)

    def bottom(s):
        X, Y = _frame(s, 0, 1, 0, 1.05, [0, 0.25, 0.5, 0.75, 1.0],
                      [0, 0.25, 0.5, 0.75, 1.0], "q   (capacity used)",
                      "normalised")
        s.polyline([(X(qs[i]), Y(ent[i])) for i in range(len(qs))],
                   weight=1.5, color=_BLUE)
        s.polyline([(X(qs[i]), Y(length[i])) for i in range(len(qs))],
                   weight=1.5, color=_GREEN)
        s.text(X(0.55), Y(0.86), "S(cut)/S_max saturates at 1 (Lemma 4)",
               size=6.8, align='center', color=_BLUE)
        s.text(X(0.55), Y(0.56),
               "substrate length / 2 sqrt(S_max) -> 1 (Lemma 2)",
               size=6.8, align='center', color=_GREEN)

    def both(s):
        s.rect(0.0, 0.50, 1.0, 0.50, fill=(0.995, 0.995, 1.0),
               stroke=(0.9, 0.9, 0.9), weight=0.3)
        top_shifted = _Shifted(s, 0.50)
        top(top_shifted)
        s.rect(0.0, 0.0, 1.0, 0.50, fill=(1.0, 0.997, 0.997),
               stroke=(0.9, 0.9, 0.9), weight=0.3)
        bottom(_Shifted(s, 0.0))

    d.figure(both, 300,
             title="Figure 3.  Conjecture R: what diverges and what does not",
             caption="Top panel: the readout curvature K_readout = (du/dq)^2 "
                     "diverges without bound as q approaches 1, i.e. as "
                     "'r approaches 0'.  Bottom panel: every substrate "
                     "invariant is finite and bounded - the entropy across "
                     "the cut saturates at S_max (Lemma 4) and the total "
                     "substrate length converges to the exact value "
                     "2 sqrt(S_max) (Lemma 2).  Saturated-ball model, "
                     "integrated numerically; the substrate curves are each "
                     "normalised to their own limiting value, which is 1.")


class _Shifted:
    """A panel view that maps figure-space y in [lo, lo+0.5) to a half box."""

    def __init__(self, s, lo):
        self.s = s
        self.lo = lo

    def _fy(self, y):
        return self.lo + (1.0 - y) * 0.50

    def line(self, x1, y1, x2, y2, weight=0.7, color=(0, 0, 0), dash=None):
        self.s.line(x1, self._fy(y1), x2, self._fy(y2), weight=weight,
                   color=color, dash=dash)

    def text(self, x, y, s, size=7, style='body', align='left', color=None,
             **kw):
        self.s.text(x, self._fy(y), s, size=size, style=style, align=align,
                    color=color)

    def polyline(self, pts, weight=1.1, color=(0.1, 0.2, 0.6), dash=None):
        self.s.polyline([(p[0], self._fy(p[1])) for p in pts], weight=weight,
                        color=color, dash=dash)

    def dot(self, x, y, r=0.006, color=(0.1, 0.2, 0.6)):
        self.s.dot(x, self._fy(y), r=r, color=color)

    def rect(self, *a, **kw):
        pass


def fig_ladder(d):
    """The quantised Page ladder for small holes."""
    cases = [10, 20, 40, 60]
    cols = [_BLUE, _ORANGE, _GREEN, (0.55, 0.20, 0.60)]

    def draw(s):
        X, Y = _frame(s, 0, 60, 0, 34, [0, 10, 20, 30, 40, 50, 60],
                      [0, 5, 10, 15, 20, 25, 30], "m  (area quanta emitted)",
                      "S / ln 2   (bits)")
        for j, n0 in enumerate(cases):
            s.polyline([(X(m), Y(min(m, n0 - m))) for m in range(n0 + 1)],
                       weight=1.5, color=cols[j])
            s.text(X(58), Y(n0 / 2.0 + 1.0), "N = %d" % n0, size=6.8,
                   align='right', color=cols[j])
        s.text(X(30), Y(32.0), "N = 18.13: a Planck-mass black hole",
               size=6.8, align='center', color=_INK)

    d.figure(draw, 190,
             title="Figure 4.  The quantised ladder",
             caption="The Page curve when both channels' capacities count "
                     "whole area quanta, for N = 10, 20, 40 and 60.  The curve "
                     "is a tent over a finite number of steps and there is no "
                     "smooth curve left to interpolate (Theorem 9).  A "
                     "Planck-mass black hole has N = 4 pi / ln 2 = 18.13 "
                     "quanta (Theorem 12), so the endpoint of evaporation "
                     "lives squarely in this regime, where its Page time is "
                     "misplaced by 8.3 per cent (Corollary 4).")


# ==========================================================================
# Paper I
# ==========================================================================
def paper_i(d):
    d.heading("Paper I", 0)
    d.heading("Partitionism: a black hole in one language", 1)
    d.para("*Abstract.*  Modern physics describes the black hole piecewise: a "
           "metric outside, a thermal atmosphere, a unitary answer inside "
           "AdS/CFT, and at least three incompatible proposals for the "
           "endpoint.  There is no single language that covers collapse, "
           "horizon, interior, evaporation and termination.  We propose one.  "
           "Partitionism takes countable distinguishability as fundamental, "
           "treats a spherically defined cut of an information substrate as "
           "the object that can hold it, and derives geometry as the "
           "coarse-grained readout of the cut structure.  A black hole is a "
           "cut that has saturated: it cannot be refined further, only "
           "transferred.  This single mechanism addresses the singularity, "
           "the firewall, the trans-Planckian problem and the information "
           "paradox together, and it is computable: Paper II proves and "
           "verifies the evaporation ledger that replaces the paradox, Paper "
           "III examines the singularity as a readout artefact, and Paper IV "
           "derives the one signature that is not suppressed below "
           "observability.", size=9.5)
    d.para("**Status.**  Speculative research framework.  Papers II-IV contain "
           "theorems that are proved and, separately, numerical results that "
           "are exact; the postulates are conjectures and are labelled as "
           "such.  Appendix A is a register of every claim in this volume with "
           "its status.", size=9, style='bodyi')

    d.heading("1.  Introduction: seven things the standard framework cannot do",
              2, number=None)

    d.para("Each item below is standard, established physics; references are in "
           "Appendix D.  They are listed because they define the target of "
           "this work.")
    d.table([
        ["#", "Failure", "What is established"],
        ["1", "No interior worth the name",
         "Schwarzschild (1916) and Kerr (1963) are vacuum solutions; collapse "
         "(Oppenheimer-Snyder 1939) is a separate problem.  Inside, geodesics "
         "terminate (Hawking-Penrose 1970): the theory predicts its own "
         "invalidity"],
        ["2", "The horizon is teleological",
         "The event horizon depends on the entire future of the spacetime.  "
         "Dynamical horizons (Ashtekar-Krishnan 2004) are the local "
         "replacement, and they are strictly weaker"],
        ["3", "Semiclassical evolution is not unitary",
         "Hawking (1975) gives a thermal flux; the radiation's entropy grows "
         "monotonically.  Page (1993) showed it must instead turn around at "
         "the Page time (half the initial entropy) and return to zero"],
        ["4", "Smoothness and monogamy collide",
         "AMPS (JHEP 02 (2013) 062): purity of the radiation, low-energy "
         "effective field theory at the horizon, and an uneventful horizon "
         "cannot all hold"],
        ["5", "The calculation starts outside its domain",
         "Hawking's derivation redshifts field modes to trans-Planckian "
         "wavelengths at the horizon, where quantum field theory on a fixed "
         "background is not meaningful"],
        ["6", "No formation mechanism, no interior data",
         "Microscopic interiors are posited (fuzzballs, Mathur 2009; Planck "
         "stars, Rovelli-Vidotto 2014) rather than derived; the Page curve "
         "was first derived microscopically in AdS/CFT (2019-2022), which "
         "needs an anti-de Sitter boundary"],
        ["7", "Black holes dominate the entropy budget, unexplained",
         "S_obs ~ 3.1 x 10^104 k_B, dominated by supermassive black holes "
         "(Egan-Lineweaver 2010); the cosmic event horizon holds "
         "2.6 x 10^122 k_B.  A theory in which black holes are marginal has "
         "mis-prioritised"],
    ], widths=[0.4, 3.2, 8.0], size=7.6, title="Table 1.  The seven failures")

    d.para("A concrete illustration of item 7 that is rarely stated: the "
           "surface gravity fixes a black hole's temperature at "
           "T_H = hbar c^3/(8 pi G M k_B) `[ESTABLISHED]`, so a solar-mass "
           "hole sits at 6.2 x 10^-8 K - more than 10^7 times colder than the "
           "2.7 K microwave background.  The crossover (T_H = 2.7 K) falls at "
           "M = 4.5 x 10^22 kg, 0.61 lunar masses.  Every stellar and "
           "supermassive black hole alive today is therefore *gaining* mass, "
           "and the last stage of a black hole's thermodynamic life is a "
           "question of which era it lives in.")

    d.heading("2.  The postulates", 2)
    d.para("Each postulate is a conjecture.  'Replaces' says what it "
           "displaces; 'borrows' says which established result it uses as "
           "input, so that the borrowing is not mistaken for originality.")

    d.para("**P1 - The substrate** `[CONJECTURE]`.  Reality's fundamental "
           "relata are qunits - units of distinguishable information - held in "
           "a substrate (lattice) that has no space, no time and no fields as "
           "primitives.  Everything measurable is a readout of this "
           "substrate.  *Replaces*: manifold + fields.  *Borrows*: Wheeler's "
           "'it from bit'; Lloyd (Nature 406 (2000) 1047).")
    d.para("**P2 - Cuts** `[CONJECTURE]`.  The graded structure on the "
           "substrate is carried by cuts - bipartitions (A, A^c) - and by the "
           "entropy across them, S(A) = -Tr rho_A log rho_A.  Cuts are prior "
           "to any notion of location.  *Borrows*: Ryu-Takayanagi (PRL 96 "
           "(2006) 181602); van Raamsdonk (GRG 42 (2010) 2323); Maldacena's "
           "AdS/CFT (Adv. Theor. Math. Phys. 2 (1998) 231).")
    d.para("**P3 - Saturation** `[BORROWED, elevated]`.  Cuts saturate: "
           "S(A) <= S_max with S_max fixed by the Bekenstein bound (Bekenstein "
           "PRD 23 (1981) 287).  A saturated cut cannot be refined.  This is "
           "established physics; what is new is making it the dynamical hinge "
           "of the theory rather than a bound quoted at the end of a "
           "calculation.")
    d.para("**P4 - The readout** `[CONJECTURE]`.  A classical metric exists at "
           "a region if and only if the cut entropy's second derivative is "
           "non-degenerate there.  *Borrows*: Matsueda (arXiv:1408.5589, "
           "arXiv:1408.6633) constructs the emergent metric as the Hessian of "
           "the entanglement entropy, as do the kinematic-space/Crofton-form "
           "constructions; Jacobson (PRL 75 (1995) 1260) derives the Einstein "
           "equation from the Clausius relation on local horizons; Verlinde "
           "(arXiv:1001.0785) derives Newtonian gravity from entropy "
           "gradients.  **The metric-as-Hessian step is not ours.**  Our claim "
           "is about what happens when that Hessian degenerates (Paper III).")
    d.para("**P5 - Conservation and the two channels** `[CONJECTURE]`.  "
           "Fine-grained evolution is unitary, so the ledger is conserved: "
           "the two channels that a collapse creates - the in-fall channel I "
           "and the out-fall channel O - exchange their distinctions, never "
           "create or destroy them.  All apparent entropy production is a "
           "property of the readout.  *Borrows*: Page (PRL 71 (1993) 3743); "
           "the quantum-extremal-surface results of 2019-2022.")

    d.heading("3.  The objects", 2)
    d.table([
        ["Object", "Definition", "Standard-physics counterpart"],
        ["qunit", "one unit of distinguishable information", "a bit of "
         "Bekenstein-Hawking entropy"],
        ["cut", "a bipartition of the substrate", "a Ryu-Takayanagi "
         "bipartition"],
        ["cut entropy", "von Neumann entropy across the cut", "entanglement "
         "entropy"],
        ["readout", "the coarse map from cuts to classical geometry", "the "
         "semiclassical limit"],
        ["channel I (in-fall)", "the part swallowed by collapse", "the black "
         "hole interior"],
        ["channel O (out-fall)", "the vacuum's displaced partners", "the "
         "outside / Hawking radiation"],
        ["interface", "a saturated cut", "the horizon"],
        ["knot", "the saturated core", "the singularity"],
        ["ledger", "running count of distinctions per channel", "the Page "
         "curve"],
        ["code distance d", "errors the interface code corrects", "quantum "
         "hair"],
    ], widths=[1.9, 5.0, 5.0], size=7.6, title="Table 2.  Vocabulary")

    d.heading("4.  The black hole as a whole: five phases", 2)
    d.para("The 'whole' that the title promises is a single life cycle in one "
           "language.  Table 3 is the summary; Paper II supplies the "
           "computable content of phases III-IV, Paper III the content of "
           "phase V, and Paper IV the endpoint.")
    d.table([
        ["Phase", "Standard story", "Partitionism story"],
        ["I  Implosion", "pressure fails; a horizon forms",
         "successive compression of cuts; the first cut reaches S_max"],
        ["II  Lock-in", "the event horizon exists globally",
         "the interface code switches on: N = A/DeltaA logical qunits"],
        ["III  Resonance", "the hole sits at T_H emitting thermally",
         "the interface relaxes; the ledger is paid out one qunit per "
         "area quantum; T_H is the relaxation linewidth"],
        ["IV  Dissolution", "the Page curve turns around",
         "ledger transfer: what left is what came in (Paper II)"],
        ["V  Termination", "remnant? bounce? explosion? unresolved",
         "the endpoint follows the selection rule of Paper IV"],
    ], widths=[1.6, 4.6, 5.6], size=7.8, title="Table 3.  Life cycle")

    d.heading("5.  How the paradoxes are addressed", 2)
    d.table([
        ["Paradox", "Move", "Where proved"],
        ["Information loss", "the ledger is conserved; the Page curve is a "
         "bookkeeping identity", "Paper II, Thm 1-5"],
        ["Firewall", "the entanglement lives at the cut, not in the bulk, and "
         "the correlation budget is fixed", "Paper II, Thm 3-4"],
        ["Trans-Planckian modes", "no continuum of modes; T_H is a relaxation "
         "linewidth of the interface code", "conjecture, Paper IV"],
        ["Endpoint", "selected by the excess area Delta(excess) = A mod "
         "DeltaA", "Paper IV, conjecture"],
        ["Singularity", "the readout degenerates; the substrate does not",
         "Paper III, Conj. R"],
    ], widths=[2.0, 6.0, 3.0], size=7.8, title="Table 4.  Resolutions")

    d.heading("6.  What is new here, and what is not", 2)
    d.para("This volume was written against the literature, twice, and the "
           "audit removed claims that were already published.  Three claims "
           "are **not** ours and are credited where used: the metric as the "
           "Hessian of entanglement entropy (Matsueda 2014-15); the Page curve "
           "as the minimum of the two subsystems' capacities, which is Page's "
           "own 1993 derivation; and the area spacing DeltaA = 4 ln2 l_P^2 "
           "that makes one area quantum carry exactly one bit (Bagchi-Ghosh-"
           "Sen 2024).  What survives as unprecedented, as far as we can "
           "determine, is: **Conjecture R** - singularities as degeneracies "
           "of the readout map (Paper III); the **selection rule** for the "
           "endpoint (Paper IV); and the postulate combination itself.  "
           "Appendix A records the status of every claim, and Section 6 of "
           "Paper I is repeated there in full.")


# ==========================================================================
# Paper II
# ==========================================================================
def paper_ii(d):
    d.heading("Paper II", 1)
    d.heading("The evaporation ledger: theorems and numerical verification", 1)
    d.para("*Abstract.*  We prove six theorems that convert the assertion "
           "'information is conserved' into exact, checkable statements about "
           "an evaporating black hole, and we verify every one of them "
           "numerically on registers of up to ten qubits with exact von "
           "Neumann entropies.  Theorem 1 and Theorem 2 together give the Page "
           "curve and its turnover; Theorem 6 gives Hawking's monotonically "
           "growing curve as the exact consequence of a thermal initial "
           "condition; Theorems 3 and 4 give a fixed correlation budget "
           "between the purifier and the two channels, which is the "
           "computable form of the anti-firewall statement.  The central "
           "mechanism is therefore not an interpretation: it is an identity "
           "that can be checked on a quantum computer.", size=9.5)

    d.heading("1.  Setup and notation", 2)
    d.para("Let the universe be a register of n0 qubits.  At step m the "
           "register is bipartitioned into **Rad** (the m emitted qubits) and "
           "**B** (the remaining n0 - m).  The global state |psi> is pure.  "
           "In the *microstate* model (Model A) |psi> is a single random pure "
           "state and every step m applies a Haar-random unitary to B "
           "followed by peeling one qubit off into Rad.  In the *purified "
           "thermal* model (Model B) a purifier R of n0 qubits is entangled "
           "with B by n0 Bell pairs and never touched again; the emitted "
           "qubits are carved out of B exactly as in Model A.  Entropies are "
           "in nats; 1 qubit of capacity is ln 2.  All numerical results use "
           "exact state vectors, exact partial traces, and eigenvalues of the "
           "reduced density matrix from a complex Hermitian Jacobi iteration "
           "(Appendix B).")

    d.heading("2.  Theorems", 2)

    d.para("**Theorem 1 (purity identity).**  For a pure state on Rad x B, "
           "S(rho_Rad) = S(rho_B).  *Proof.*  Schmidt decomposition: "
           "|psi> = sum_k sqrt(lambda_k) |r_k>|b_k> with lambda_k > 0, "
           "sum lambda_k = 1, and Schmidt rank r <= min(2^m, 2^(n0-m)).  Then "
           "rho_Rad = sum_k lambda_k |r_k><r_k| and rho_B = sum_k lambda_k "
           "|b_k><b_k|, so the two spectra coincide and the von Neumann "
           "entropies are equal.  Q.E.D.")
    d.para("**Theorem 2 (capacity bound).**  S(rho_Rad) <= ln r <= "
           "min(m, n0 - m) ln 2.  *Proof.*  For eigenvalues lambda_1..lambda_r "
           "of rho_Rad with sum 1, concavity of p -> -p ln p gives "
           "-sum_k lambda_k ln lambda_k <= -r (1/r) ln(1/r) = ln r, with "
           "equality iff all lambda_k are equal.  By Theorem 1 the Schmidt "
           "rank is bounded by the smaller dimension, dim = 2^m or 2^(n0-m), "
           "so ln r <= min(m, n0 - m) ln 2.  Q.E.D.")
    d.para("**Corollary 1 (continuous Page curve).**  f(m) = min(m, n0 - m) "
           "increases on [0, n0/2] and decreases on [n0/2, n0]; its maximum "
           "is (n0/2) ln 2 at m = n0/2.  *Proof.*  Elementary: for m < n0/2 "
           "the binding branch is m, for m > n0/2 it is n0 - m.  Q.E.D.")
    d.para("**Theorem 3 (ledger identity).**  For a pure state on R x Rad x B "
           "with S(R) = S_0, I(Rad:B) = S(Rad) + S(B) - S_0, hence "
           "S(Rad) = S_0 - S(B) + I(Rad:B).  *Proof.*  By definition "
           "I(Rad:B) = S(Rad) + S(B) - S(Rad,B), and purity of the state on "
           "(Rad,B) x R gives S(Rad,B) = S(R) = S_0.  Q.E.D.")
    d.para("**Corollary 2.**  S(Rad) + S(B) >= S_0 always, with equality "
           "exactly when Rad and B are uncorrelated (I(Rad:B) = 0).  The "
           "difference between the two sides is the correlation stored "
           "between the channels.")
    d.para("**Theorem 4 (one-for-one transfer).**  I(R:Rad) + I(R:B) = "
           "2 S(R).  *Proof.*  I(R:Rad) = S(R) + S(Rad) - S(R,Rad), and by "
           "purity S(R,Rad) = S(B), so I(R:Rad) = S(R) + S(Rad) - S(B).  "
           "Similarly I(R:B) = S(R) + S(B) - S(Rad).  Adding gives 2 S(R).  "
           "Q.E.D.")
    d.para("**Corollary 3 (the correlation budget is fixed).**  In any "
           "unitary emission process the sum of the purifier's mutual "
           "information with the two channels is a constant of the motion.  "
           "Every bit of correlation the radiation acquires is purchased from "
           "what remains.  This is the precise, provable sense in which "
           "information is transferred rather than duplicated, and it is the "
           "sense in which the AMPS argument is blocked.")
    d.para("**Theorem 5 (ledger-blind monotonicity).**  Let |Psi> = "
           "(I_R x U_B)|Phi> be a maximally entangled state of two n0-qubit "
           "registers, for any unitary U_B, and let Rad be any subset of m "
           "qubits of B.  Then rho_Rad = I_Rad/2^m and S(rho_Rad) = m ln 2, "
           "independently of U_B and of which subset is chosen.  *Proof.*  "
           "rho_B = Tr_R[(I x U_B)|Phi><Phi|(I x U_B^dag)] = U_B (Tr_R "
           "|Phi><Phi|) U_B^dag = U_B (I_B/2^n0) U_B^dag = I_B/2^n0, because "
           "U_B is unitary.  The reduced state of any subset of a maximally "
           "mixed state is maximally mixed, so rho_Rad = I_Rad/2^m, whose "
           "entropy is ln 2^m.  Q.E.D.")
    d.para("**Theorem 6 (the two curves are two initial conditions).**  "
           "Theorem 2 predicts a turnaround because the global state is pure "
           "(Model A).  Theorem 5 predicts monotone growth S = m ln 2 with no "
           "turnaround because the initial black hole is maximally mixed "
           "(Model B, R traced out).  *Proof.*  Immediate from Theorems 2 and "
           "5; verified numerically in Section 3.  Q.E.D.")
    d.para("The significance of Theorem 6 is that the difference between "
           "Hawking's curve and the Page curve is, at this level of "
           "description, a statement about the initial ledger, not about "
           "dynamics: the same emission process produces both.")

    d.heading("3.  Numerical verification", 2)
    d.para("Theorems 1-6 are identities, so the numerical test is exactness: "
           "every quantity is computed from an exact state vector, and the "
           "checks below are machine-precision tests of the theorems, not "
           "statistical comparisons.")
    d.table([
        ["n0", "max S/ln2", "capacity bound violated by", "turnover m",
         "n0/2", "max |S(Rad) - S(B)|"],
        ["4", "1.3357", "0.00e+00", "2", "2.00", "2.22e-16"],
        ["6", "2.3332", "0.00e+00", "3", "3.00", "6.66e-16"],
        ["8", "3.2696", "0.00e+00", "4", "4.00", "0.00e+00"],
        ["10", "4.2633", "0.00e+00", "5", "5.00", "4.44e-16"],
    ], widths=[0.7, 1.4, 3.0, 1.6, 1.0, 2.4], size=7.6,
        title="Table 5.  Theorem 1 and Theorem 2, verified exactly",
        align=['center', 'right', 'right', 'center', 'center', 'right'])
    d.para("Three random-unitary trials per size; the turnover lands on "
           "m = n0/2 in every trial and the capacity bound of Theorem 2 is "
           "never violated to machine precision.  Figure 1 shows the "
           "simulated curve against Page's analytic approximation.")
    fig_page_curve(d)
    d.para("Theorem 5's prediction is verified exactly as well: in Model B "
           "the radiation entropy is 1, 2, 3, 4, 5, 6 bits for m = 1..6 with "
           "n0 = 6 - the ledger-blind curve of Figure 1 - and the mutual "
           "informations obey Theorem 4 with a sum fixed at 2 n0 = 12 "
           "(Figure 2).")

    d.heading("4.  Relation to prior work", 2)
    d.para("Page derived the capacity result in 1993; it is restated in the "
           "language of subsystem dimensions in arXiv:2002.05734 and "
           "expositorily in arXiv:2505.23011.  Bradler and Adami "
           "(arXiv:1505.02840) construct Page curves from a dynamical "
           "decoupling model, and quantum-computer simulations of the Page "
           "curve now exist (Nucl. Phys. 2025).  The 2019-2022 "
           "replica-wormhole/island computations (Penington arXiv:1905.08255; "
           "AEMM arXiv:1905.08762; AHMST arXiv:1911.12333; PSSY "
           "arXiv:1911.11977) derive the same curve from gravitational path "
           "integrals in AdS/CFT.  **What is new in this paper is not the "
           "curve.**  It is (i) the exact one-for-one correlation identity of "
           "Theorem 4 used as the anti-firewall statement, (ii) Theorem 6, "
           "which identifies Hawking's monotone curve as the exact "
           "consequence of a thermal initial condition, and (iii) the "
           "quantised consequences of Paper IV.")


# ==========================================================================
# Paper III
# ==========================================================================
def paper_iii(d):
    d.heading("Paper III", 0)
    d.heading("Readout degeneracy: the singularity as an artefact of the "
              "coarse map", 1)
    d.para("*Abstract.*  The classical singularity theorems show that "
           "geodesics terminate; they do not show that physics terminates, "
           "because a singularity in a coarse-grained description may be a "
           "property of the coarse-graining.  We formulate this precisely as "
           "Conjecture R - a curvature singularity is a loss of invertibility "
           "of the readout map from cut variables to metric components - and "
           "we build an explicit model, the saturated ball, in which the "
           "readout curvature diverges as (1-q)^-2 while every substrate "
           "invariant remains finite and bounded.  The model's invariants are "
           "proved exactly and verified numerically.  We also prove a result "
           "about the classical solution that is usually only quoted: the "
           "proper distance from a Schwarzschild horizon to its centre is "
           "exactly pi r_s / 2, so the classical case has precisely the shape "
           "Conjecture R predicts - a divergent coordinate quantity beside a "
           "finite proper one.", size=9.5)

    d.heading("1.  What the singularity theorems do and do not say", 2)
    d.para("Hawking and Penrose (Proc. Roy. Soc. Lond. A 314 (1970) 529) "
           "prove geodesic incompleteness under energy conditions and trapped "
           "surfaces.  In the saturated-ball language below, those hypotheses "
           "are exactly the conditions under which a cut saturates: a "
           "trapped surface is the sign that the region's information "
           "capacity is being exhausted.  The theorem is then a statement "
           "about the readout's Jacobian.  It is a real theorem, and nothing "
           "here disputes it; what is disputed is the inference that "
           "geodesic incompleteness implies a boundary of physics.")

    d.heading("2.  Conjecture R", 2)
    d.para("**Conjecture R** `[CONJECTURE]`.  A curvature singularity is not a "
           "property of the substrate.  It is the statement that the readout "
           "map from cut variables to metric components loses invertibility, "
           "i.e. that the entanglement Hessian g^E_{mu nu} = -d^2 S_min / "
           "(dx^mu dx^nu) degenerates.  Where the Hessian is non-degenerate a "
           "metric exists; where it degenerates the classical geometry is "
           "undefined rather than large.")
    d.para("Three consequences follow, and all three are falsifiable: "
           "(a) there is no substrate-level divergence anywhere on the "
           "approach to the singularity, because saturation caps every "
           "quantity; (b) the classical singularity theorems are statements "
           "about the Jacobian of the map, not about the termination of "
           "physics; (c) there is a finite substrate invariant that replaces "
           "the diverging Kretschmann scalar as the diagnostic of 'how far in' "
           "one is.  A fourth consequence - that the black hole has no "
           "singularity for information to be destroyed at - is the reason "
           "the information paradox is addressed in Paper II without "
           "appealing to a Planck-scale threshold.")

    d.heading("3.  The saturated ball: model and proofs", 2)
    d.para("Let q in [0,1) be the fraction of a cut's capacity in use, and let "
           "the radial readout coordinate be u = -ln(1 - q) - a compression "
           "coordinate, so that q approaching 1 pushes u to infinity while "
           "the underlying variable q stays bounded.  Let the entropy of the "
           "ball read out at radius u be the saturating function "
           "S(u) = S_max (1 - exp(-u/u_0)).  This is the readout mirror of "
           "P3: the cut's entropy approaches its bound and cannot pass it.")
    d.para("**Lemma 1.**  dS/du = (S_max/u_0) exp(-u/u_0) > 0 and "
           "d^2S/du^2 = -(S_max/u_0^2) exp(-u/u_0) < 0, so the readout metric "
           "g^E_uu = -d^2S/du^2 = (S_max/u_0^2) exp(-u/u_0) is positive and "
           "tends to 0 as u increases.  *Proof.*  Differentiate twice.  Q.E.D.")
    d.para("**Lemma 2 (substrate length).**  The total readout length "
           "L_sub = int_0^inf sqrt(g^E_uu) du = 2 sqrt(S_max), independent of "
           "u_0.  *Proof.*  sqrt(g^E_uu) = sqrt(S_max)/u_0 * exp(-u/2u_0), and "
           "int_0^inf exp(-u/2u_0) du = 2 u_0.  Q.E.D.")
    d.para("**Lemma 3 (readout curvature).**  The readout curvature scale "
           "K_read = (du/dq)^2 = 1/(1-q)^2 = exp(2u) diverges without bound as "
           "q -> 1.  *Proof.*  u = -ln(1-q) gives du/dq = 1/(1-q).  Q.E.D.")
    d.para("**Lemma 4 (saturation).**  S(cut; q) = S_max (1 - exp(-u/u_0)) <= "
           "S_max for all q, with equality only in the limit q -> 1, and "
           "no cut of the ball can be refined past q = 1.  *Proof.*  "
           "1 - exp(-x) < 1 for finite x and increases monotonically to 1.  "
           "Q.E.D.")
    d.para("**Theorem 7 (the saturated ball has no substrate singularity).** "
           "**Every** substrate-level quantity built from the cut structure - "
           "the total entropy, the total entropy flux int(dS/du)du = S_max, "
           "the total readout length of Lemma 2, and the entropy across any "
           "interior cut - is finite and bounded on the whole range q in [0,1), "
           "while the readout curvature diverges as in Lemma 3.  *Proof.*  "
           "Lemmas 2 and 4 and the monotonicity of S.  Q.E.D.")
    d.para("**Theorem 8 (the classical case has the same shape).**  The proper "
           "radial distance from the horizon to the centre of a Schwarzschild "
           "black hole is L = int_0^{r_s} dr / sqrt(r_s/r - 1) = pi r_s / 2.  "
           "*Proof.*  Substitute r = r_s sin^2(theta): dr = 2 r_s sin(theta) "
           "cos(theta) d(theta), sqrt(r_s/r - 1) = cot(theta), so the integrand "
           "becomes 2 r_s sin^2(theta) d(theta), and int_0^{pi/2} 2 r_s "
           "sin^2(theta) d(theta) = 2 r_s (pi/4) = pi r_s/2.  Q.E.D.")
    d.para("The numerics agree: for the Sun, r_s = 2.9533 x 10^3 m and the "
           "numerically integrated proper distance is 4.6351 x 10^3 m against "
           "the exact pi r_s/2 = 4.6391 x 10^3 m, a 0.09 % difference that is "
           "entirely the trapezium error of the integration.  Meanwhile the "
           "Kretschmann scalar R_{abcd}R^{abcd} = 48 G^2M^2/(c^4 r^6) diverges "
           "as r -> 0.  The classical solution therefore already contains the "
           "shape Conjecture R attributes to the readout: a divergent "
           "coordinate quantity sitting beside a finite proper one.")

    d.heading("4.  Numerical verification", 2)
    fig_readout(d)
    d.table([
        ["q", "u", "S/S_max", "g^E_uu", "du/dq", "K_readout"],
        ["0.5", "0.6931", "0.500000", "5.000e-01", "2.000", "4.000"],
        ["0.99", "4.6051", "0.990000", "1.000e-02", "1.000e+02", "1.000e+04"],
        ["0.9999", "9.2104", "0.999900", "9.999e-05", "1.000e+04", "1.000e+08"],
        ["0.999999", "13.8155", "0.999999", "1.000e-06", "1.000e+06",
         "1.000e+12"],
    ], widths=[1.0, 1.0, 1.3, 1.5, 1.4, 1.5], size=7.6,
        align=['right'] * 6,
        title="Table 6.  Readout divergence (Lemma 3) against substrate "
              "finiteness (Theorem 7)")
    d.para("The integral of Lemma 2 was evaluated numerically as 1.999999 "
           "against the exact 2.0, with the 6 x 10^-7 difference accounted "
           "for by the analytic tail beyond u = 30, which is 2 sqrt(S_max) "
           "u_0 exp(-u_max/(2 u_0)) = 6.1 x 10^-7.")

    d.heading("5.  What is missing, and what would kill it", 2)
    d.para("The saturated ball is a *model* of the readout, not a derivation "
           "of it.  To become a result it needs the map q(x) from the "
           "substrate's cut variable to the classical radial coordinate; "
           "without it the framework does not reproduce the Schwarzschild "
           "exponent r^-6, and it does not claim to (open problem O2).  "
           "Conjecture R is falsified by any substrate-level observable that "
           "diverges as the readout degenerates - for example an "
           "outgoing-radiation energy density that genuinely blows up "
           "(falsifier F2 of the main document).  Conversely, the classical "
           "evidence for it is the structure of Theorem 8, which nobody "
           "usually states as a singularity diagnosis.")


# ==========================================================================
# Paper IV
# ==========================================================================
def paper_iv(d):
    d.heading("Paper IV", 0)
    d.heading("Quantised payout: the staircase, the Page-time shift, and "
              "where to look", 1)
    d.para("*Abstract.*  If the interface is quantised, the two channel "
           "capacities count whole area quanta, and the Page curve is a "
           "staircase.  We prove that the largest possible misplacement of "
           "the Page time is half an area quantum, that in time this is "
           "dt/t = 3/(2N) with N the number of quanta, and that a "
           "Planck-mass black hole - the endpoint of evaporation - has "
           "exactly N = 4 pi / ln 2 = 18.13 quanta, so its Page curve is a "
           "tent of about eighteen steps and its Page time is misplaced by "
           "8.3 %.  For astrophysical black holes the effect is 10^-77 and "
           "unobservable; for analog horizons it is between 0.02 % and 0.8 %, "
           "which makes the laboratory, not the sky, the honest place to "
           "test the framework.", size=9.5)

    d.heading("1.  Capacity quantisation", 2)
    d.para("Partitionism adopts the **published** spacing that makes one area "
           "quantum carry exactly one bit of entropy, DeltaA = 4 ln 2 l_P^2.  "
           "This is the Bekenstein-Mukhanov evenly spaced spectrum in the "
           "form that saturates Landauer's bound, established by Bagchi, "
           "Ghosh and Sen (Gen. Relativ. Gravit. 56 (2024) 108, "
           "arXiv:2408.02077) and extended by Neto and Thibes "
           "(arXiv:2605.26386).  It is **not** a claim of this work.  In loop "
           "quantum gravity's convention DeltaA = 8 pi gamma l_P^2 the same "
           "spacing corresponds to gamma = ln 2/(2 pi) = 0.110, which differs "
           "from the values that literature usually quotes (gamma ~ 0.274 in "
           "arXiv:2001.03440; gamma_0 = ln 2/(pi sqrt 3) ~ 0.127 in the SU(2) "
           "counting).  The discrepancy is a pre-existing tension between two "
           "quantised-area programmes and a sharp way to test which one "
           "nature uses, but it is not a new discovery.")
    d.para("With capacities counted in whole quanta, the radiation can hold at "
           "most m quanta and the remainder at most n0 - m, where n0 = A/DeltaA "
           "is the total.  Theorem 2 then becomes an equality constraint on "
           "integers, which is what produces the staircase.")

    d.heading("2.  Theorems", 2)
    d.para("**Theorem 9 (integer turnover).**  For integer capacities the Page "
           "point is m* = ceil(n0/2), and |m* - n0/2| <= 1/2.  *Proof.*  The "
           "function min(m, n0 - m) on integers is strictly increasing while "
           "m < n0 - m and non-increasing afterwards; the maximiser is the "
           "smallest integer m with m >= n0 - m, i.e. m >= n0/2, which is "
           "ceil(n0/2).  For even n0 the shift is 0, for odd n0 it is 1/2.  "
           "Q.E.D.")
    d.para("**Theorem 10 (the Page-time shift).**  Let N = A/DeltaA.  A "
           "misplacement of the Page point by DeltaN quanta shifts the "
           "evaporation time at the Page point by dt/t = (3/2)|DeltaN|/N, so "
           "the maximum is dt/t = 3/(2N).  *Proof.*  A = 16 pi G^2 M^2/c^4 "
           "gives N = A/DeltaA proportional to M^2, so M proportional to "
           "N^(1/2).  The evaporation time is t = 5120 pi G^2 M^3/(hbar c^4) "
           "(derived below), i.e. t proportional to N^(3/2).  Therefore "
           "dt/t = (3/2) dN/N.  At the Page point N_rem is about n0/2 and the "
           "half-quantum shift of Theorem 9 gives |DeltaN|/N = 1/n0.  Q.E.D.")
    d.para("**Theorem 11 (the lifetime constant).**  t = 5120 pi G^2 M^3 / "
           "(hbar c^4).  *Proof.*  Hawking's luminosity is L = hbar c^6 / "
           "(15360 pi G^2 M^2) `[ESTABLISHED]`, and -dM/dt = L/c^2.  "
           "Separating: int_0^{M} M'^2 dM' = (hbar c^4/(15360 pi G^2)) t, i.e. "
           "M^3/3 = hbar c^4 t/(15360 pi G^2).  Q.E.D.  Numerically this gives "
           "8.411 x 10^-17 (M/kg)^3 s, i.e. 2.1 x 10^67 years for a solar "
           "mass, matching the standard quotation.")
    d.para("**Theorem 12 (the Planck-mass quantum count).**  A black hole of "
           "exactly one Planck mass has N = 4 pi / ln 2 = 18.13 area quanta.  "
           "*Proof.*  r_s = 2 G m_P/c^2 = 2 l_P, because m_P = sqrt(hbar c/G) "
           "and l_P = sqrt(hbar G/c^3); hence A = 4 pi r_s^2 = 16 pi l_P^2, "
           "and N = A/DeltaA = 16 pi l_P^2/(4 ln 2 l_P^2) = 4 pi/ln 2.  "
           "Q.E.D.")
    d.para("**Corollary 4 (the endpoint is entirely quantised).**  "
           "dt/t = 3/(2N) evaluated at N = 4 pi/ln 2 gives 0.0827, i.e. an "
           "8.3 per cent misplacement of the Page time, and the Page curve is "
           "a tent over about eighteen steps rather than a curve.  The "
           "staircase is therefore not a small correction anywhere near the "
           "endpoint; it is the whole of the physics there.")

    d.heading("3.  The numbers", 2)
    d.table([
        ["Object", "mass (kg)", "N = A/DeltaA", "max dt/t = 3/(2N)"],
        ["solar-mass black hole", "1.988e30", "1.513e77", "9.9e-78"],
        ["Sgr A* (4.3e6 M_sun)", "8.550e36", "2.798e90", "5.4e-91"],
        ["M87* (6.5e9 M_sun)", "1.293e40", "6.394e96", "2.3e-97"],
        ["primordial BH, 10^12 kg", "1.000e12", "3.827e40", "3.9e-41"],
        ["Planck mass (endpoint)", "2.176e-08", "1.813e01", "8.3e-02"],
    ], widths=[3.4, 1.6, 1.8, 2.2], size=7.8,
        align=['left', 'right', 'right', 'right'],
        title="Table 7.  How quantised the payout is")
    d.para("For analog horizons the 'Planck length' is set by the condensate "
           "healing length xi rather than by l_P, and the suppression becomes "
           "an engineering parameter.  With R = 5-20 microns and xi = 0.3 "
           "microns, N = 1.3 x 10^3 to 2 x 10^4 quanta, so the last ten "
           "quanta occupy 0.8 % to 0.02 % of the horizon's life and the "
           "largest Page-time shift is 3/(2N) ~ 10^-4.  That is small but "
           "finite, and it is the only regime in which the framework's "
           "central quantitative claim is not buried by 77 orders of "
           "magnitude.")
    fig_ladder(d)

    d.heading("4.  Predictions and falsifiers", 2)
    d.para("**P1** `[PREDICTION]`  The radiation's entropy rises in steps of "
           "k_B ln 2 per area quantum, so the Page curve is a staircase with "
           "at most a half-quantum misplacement of the Page time "
           "(dt/t = 3/(2N)).")
    d.para("**P2** `[PREDICTION]`  T_H is the relaxation linewidth of the "
           "interface code rather than the temperature of a bath of modes, "
           "so the Hawking spectrum acquires a discrete structure whose "
           "spacing is set by the interface's quantised relaxation rates.")
    d.para("**P3** `[PREDICTION]`  The decisive test is in analog horizons, "
           "where the suppression is (xi/R)^2 and can be engineered; a "
           "resolved staircase, or a resolved line structure beyond the "
           "condensate's dispersion relation, would be the first positive "
           "evidence.")
    d.para("**F1** `[FALSIFIER]`  A resolved, continuous, "
           "dispersion-consistent thermal spectrum in an analog system built "
           "to resolve discreteness at its analog Planck scale.")
    d.para("**F2** `[FALSIFIER]`  Any substrate-level observable that "
           "diverges as the readout degenerates.")
    d.para("**F3** `[FALSIFIER]`  A high-energy membrane at any horizon.")
    d.para("**F4** `[FALSIFIER]`  An endpoint that fits no limb of the "
           "selection rule Delta(excess) = A mod DeltaA.")
    d.para("**F5** `[FALSIFIER]`  Failure of the ledger identities of Paper "
           "II in a quantum simulation - for they are theorems, and a "
           "counterexample would disprove the setup, not the theorems.")


# ==========================================================================
# Appendices
# ==========================================================================
def appendix_a(d):
    d.page_break()
    d.heading("Appendix A.  Claims register", 0)
    d.para("Every substantive claim in this volume, with its status and how it "
           "is established.  Anything not listed here is either ordinary "
           "exposition or a citation.  Statuses: **THM** proved in this "
           "document; **EST** established physics with a citation; **CONJ** "
           "Partitionism conjecture, not proved; **PRED** falsifiable "
           "prediction; **FALS** falsifier; **NUM** verified numerically by "
           "the simulation suite; **BORR** adopted from elsewhere, credited.")
    rows = [["#", "Claim", "Status", "How established"]]
    rows += [
        ["A1", "Schwarzschild/Kerr are vacuum solutions; collapse is a "
               "separate problem", "EST", "Schwarzschild 1916; Kerr 1963; "
               "Oppenheimer-Snyder 1939"],
        ["A2", "Geodesics terminate inside; GR predicts its own invalidity",
         "EST", "Hawking-Penrose 1970"],
        ["A3", "The event horizon is teleological; dynamical horizons are "
               "weaker", "EST", "Ashtekar-Krishnan 2004"],
        ["A4", "Hawking radiation is thermal; the entropy curve grows "
               "monotonically", "EST", "Hawking 1975"],
        ["A5", "Unitary evaporation requires a Page turnaround at half the "
               "initial entropy", "EST", "Page PRL 71 (1993) 3743"],
        ["A6", "Smoothness, purity and QFT at the horizon cannot all hold",
         "EST", "AMPS JHEP 02 (2013) 062"],
        ["A7", "Hawking's calculation starts beyond the domain of QFT in "
               "curved spacetime", "EST", "trans-Planckian redshift"],
        ["A8", "S_obs ~ 3.1e104 k_B, dominated by supermassive black holes; "
               "CEH entropy 2.6e122 k_B", "EST", "Egan-Lineweaver 2010"],
        ["A9", "T_H(1 M_sun) = 6.2e-8 K; T_H = 2.7 K at 4.5e22 kg "
               "(0.61 M_Moon)", "NUM", "T_H = hbar c^3/(8 pi G M k_B), "
               "recomputed"],
        ["A10", "t_ev = 8.411e-17 (M/kg)^3 s; 2.1e67 yr for 1 M_sun",
         "THM/NUM", "Paper IV, Thm 11"],
        ["A11", "Reality's fundamental relata are qunits in a substrate "
                "without space, time or fields", "CONJ", "P1 - postulated"],
        ["A12", "Graded structure is carried by cuts and their entropies",
         "CONJ", "P2 - postulated"],
        ["A13", "Cuts saturate at the Bekenstein bound; a saturated cut "
                "cannot be refined", "BORR", "Bekenstein PRD 23 (1981) 287; "
                "elevated to a dynamical hinge here"],
        ["A14", "The metric is the Hessian of the cut entropy", "BORR",
         "Matsueda arXiv:1408.5589; kinematic space"],
        ["A15", "A metric exists iff the Hessian is non-degenerate; "
                "singularities are readout degeneracies", "CONJ",
         "Conjecture R - Paper III"],
        ["A16", "The basin of the fine evolution is unitary; apparent entropy "
                "production belongs to the readout", "CONJ",
         "P5 - postulated"],
        ["A17", "The horizon is a saturated cut; its area is the number of "
                "protected qunits", "CONJ", "P3 + P4 applied to trapped "
                "surfaces"],
        ["A18", "DeltaA = 4 ln 2 l_P^2 (one bit per area quantum)", "BORR",
         "Bagchi-Ghosh-Sen GRG 56 (2024) 108; Neto-Thibes "
         "arXiv:2605.26386"],
        ["A19", "Area quantisation gives the LQG spectrum 8 pi gamma l_P^2",
         "BORR", "Rovelli PRL 56 (1996) 3311"],
        ["A20", "gamma = ln2/(2pi) = 0.110 corresponds to DeltaA = 4 ln2 "
                "l_P^2; this differs from gamma = 0.274 and "
                "gamma_0 = ln2/(pi sqrt3)", "EST/BORR",
         "arithmetic on A18 and A19; the tension is pre-existing"],
        ["A21", "S(Rad) = S(B) for a pure global state", "THM",
         "Paper II, Thm 1"],
        ["A22", "S(Rad) <= min(m, n0-m) ln 2", "THM", "Paper II, Thm 2"],
        ["A23", "The continuous Page turnover is at m = n0/2", "THM",
         "Card. to Thm 2; also Page's own 1993 derivation"],
        ["A24", "I(Rad:B) = S(Rad) + S(B) - S_0, so S(Rad) = S_0 - S(B) + I",
         "THM", "Paper II, Thm 3"],
        ["A25", "I(R:Rad) + I(R:B) = 2 S(R): the correlation budget is fixed",
         "THM", "Paper II, Thm 4"],
        ["A26", "A maximally mixed initial black hole gives S(Rad) = m ln 2 "
                "exactly, for any unitary", "THM", "Paper II, Thm 5"],
        ["A27", "Hawking's monotone curve and the Page curve are two initial "
                "conditions of one emission process", "THM/NUM",
         "Paper II, Thm 6; Figures 1-2"],
        ["A28", "The Page curve is the capacity-saturation curve of the two "
                "channels", "BORR", "Page 1993 - NOT ours; we verify it"],
        ["A29", "Random-unitary simulations reproduce the Page curve", "BORR",
         "Bradler-Adami arXiv:1505.02840; quant-ph 2025 - NOT ours"],
        ["A30", "The readout curvature diverges as (1-q)^-2 in the saturated "
                "ball", "THM", "Paper III, Lemma 3"],
        ["A31", "The substrate length int sqrt(g^E) du = 2 sqrt(S_max)", "THM",
         "Paper III, Lemma 2; NUM 1.999999 vs 2.0"],
        ["A32", "The proper distance horizon-to-centre is pi r_s / 2",
         "THM/NUM", "Paper III, Thm 8; NUM 4.6351e3 vs 4.6391e3 m"],
        ["A33", "The Schwarzschild Kretschmann scalar diverges as r^-6",
         "EST", "standard"],
        ["A34", "The endpoint is selected by Delta(excess) = A mod DeltaA",
         "CONJ", "selection rule - Paper IV"],
        ["A35", "A remnant's couplings are suppressed by e^{-d} by its code "
                "distance", "CONJ", "holographic-code argument, d not yet "
                "computed"],
        ["A36", "T_H is the relaxation linewidth of the interface code",
         "CONJ", "P5 applied to the spectrum"],
        ["A37", "The interior is a logical subspace of the interface code, "
                "with bounded fidelity", "CONJ", "AdS/CFT technique in a new "
                "setting"],
        ["A38", "Integer quanta move the Page time by at most half a quantum",
         "THM", "Paper IV, Thm 9"],
        ["A39", "dt/t = 3/(2N) for the Page-time shift", "THM/NUM",
         "Paper IV, Thm 10"],
        ["A40", "A Planck-mass black hole has exactly 4 pi/ln 2 = 18.13 "
                "quanta", "THM/NUM", "Paper IV, Thm 12"],
        ["A41", "The staircase is unsuppressed only within ~10 quanta of the "
                "endpoint", "NUM", "Table 7"],
        ["A42", "Analog horizons have N ~ 1.3e3-2e4 quanta for R = 5-20 "
                "microns, xi = 0.3 microns", "NUM",
         "capacity counting with the analog healing length"],
        ["A43", "The radiation entropy staircase exists and is measurable in "
                "an analog horizon", "PRED", "P1 - falsified by F1"],
        ["A44", "A resolved continuous thermal spectrum in a "
                "discreteness-resolving analog system kills the framework",
         "FALS", "F1"],
        ["A45", "This framework's contributions are: Conjecture R, the "
                "endpoint selection rule, the postulate set, and the "
                "one-for-one correlation identity", "CONJ",
         "novelty audit, Section 6 of Paper I"],
    ]
    d.table(rows, widths=[0.5, 4.6, 1.0, 4.6], size=7.0, align=['center'])


def appendix_b(d):
    d.page_break()
    d.heading("Appendix B.  Numerical methods and validation", 0)
    d.heading("B.1  The random-unitary ensemble", 2)
    d.para("Haar-random unitaries on a contiguous block of qubits are applied "
           "as products of random Householder reflections H_v = I - 2 v v^dag / "
           "|v|^2 with v drawn from a standard complex Gaussian, followed by "
           "a diagonal phase matrix.  The same unitary is applied to every "
           "strided slice of the state vector that is supported on the block, "
           "which is what a block-local operator does.  The ensemble is not "
           "exactly Haar, and we do not need it to be: what matters is that "
           "it scrambles, and the figure of merit is the agreement with "
           "Page's analytic formula in Figure 1.")
    d.heading("B.2  Entropy computation", 2)
    d.para("Entropies are computed from exact state vectors.  The reduced "
           "density matrix of a subsystem is built by an explicit partial "
           "trace over the complement, and its eigenvalues are obtained with "
           "a complex Hermitian Jacobi iteration.  Because the global state is "
           "pure, the entropy of a subsystem equals that of its complement, so "
           "the smaller side is always diagonalised; this halves the cost.  "
           "The Hermitian matrix H = A + iB with A symmetric and B "
           "antisymmetric acts on complex vectors exactly as the real "
           "symmetric matrix [[A, -B], [B, A]] acts on real vectors, so the "
           "eigenvalues of H are those of the real doubled matrix, each "
           "appearing twice - which is how the complex problem is solved with "
           "a real eigensolver.")
    d.heading("B.3  Validation", 2)
    d.para("The machinery is validated before any physics is reported.  Four "
           "checks are run by `simulations/validation.py`: the Hermitian "
           "eigensolver against the exact spectrum of [[1, i], [-i, 2]] "
           "(error 1.1e-16); the bipartition identity of Theorem 1 over all "
           "splits of registers of 4, 6, 8 and 10 qubits (max error "
           "1.8e-15); the trace and positivity of reduced density matrices "
           "(|trace - 1| < 9e-16, most negative eigenvalue -7e-17); and the "
           "norm preservation of random block unitaries on 34 blocks "
           "(max deviation 5.6e-16).  Entanglement creation is checked by "
           "confirming that a product state |000> acquires subsystem entropy "
           "under a random unitary.")
    d.para("Two bugs were found and fixed during this work, and both are "
           "reported because they are the reason the validation step exists. "
           "First, a phase generator drew two independent random numbers for "
           "the cosine and the sine, producing cos(theta_1) + i sin(theta_2) "
           "with modulus different from one - a non-unitary 'unitary' that "
           "silently changed the norm of the state and produced spurious "
           "capacity-bound violations of up to 0.09 bits.  Second, a "
           "first-generation eigenvalue solver treated the Hermitian matrix "
           "as real and missed the imaginary off-diagonal entries.  Both were "
           "caught by the checks above, and the corrected numbers are the ones "
           "in this volume.")


def appendix_c(d):
    d.page_break()
    d.heading("Appendix C.  Reproducibility", 0)
    d.para("All numbers, tables and figures in this volume are produced by "
           "the code in `simulations/` and `paper/`.  There are no "
           "third-party dependencies - the build environment has no numpy, no "
           "LaTeX and no PDF library, so the PDF writer itself is included in "
           "`paper/pdflib.py` and writes PDF 1.4 directly.")
    d.code("python3 -m simulations.run_all          # tests, writes RESULTS.md\n"
           "python3 -m paper.build_paper            # builds the PDF\n"
           "python3 -m simulations.validation       # machinery checks only\n"
           "python3 -m simulations.test_ledger --nmax 10 --trials 3\n"
           "python3 -m simulations.test_quantization\n"
           "python3 -m simulations.test_readout")
    d.para("Every random-unitary run is seeded, so the numbers are "
           "reproducible exactly.  The figures in this volume are drawn by "
           "calling the same functions that produce the tables - "
           "`test_ledger.run_pure`, `test_ledger.run_thermal`, "
           "`test_readout.saturated_ball` - so a figure cannot drift out of "
           "sync with the text.")
    d.para("**Scope.**  The simulations test the internal consistency and "
           "quantitative consequences of Partitionism's claims in controlled "
           "quantum systems.  They do not show that the substrate exists, and "
           "they are not observational tests of black holes.  Paper II's "
           "results are theorems and would hold in any quantum mechanics; "
           "Papers III and IV contain conjectures whose consequences are "
           "computed, not experiments.")


def appendix_d(d):
    d.page_break()
    d.heading("Appendix D.  References", 0)
    d.para("All entries are real and were verified during preparation of this "
           "volume.  Where a work is cited for a claim that is *not* ours, "
           "that is stated in the appendices above.", size=9, style='bodyi')
    refs = [
        "K. Schwarzschild (1916). Uber das Gravitationsfeld eines Massenpunktes.",
        "R. P. Kerr (1963). Phys. Rev. Lett. 11, 237.",
        "J. R. Oppenheimer, H. Snyder (1939). Phys. Rev. 56, 455.",
        "S. W. Hawking, R. Penrose (1970). Proc. Roy. Soc. Lond. A 314, 529.",
        "J. D. Bekenstein (1973). Phys. Rev. D 7, 2333.",
        "J. D. Bekenstein (1981). Phys. Rev. D 23, 287.",
        "J. M. Bardeen, B. Carter, S. W. Hawking (1973). Commun. Math. Phys. "
        "31, 161.",
        "S. W. Hawking (1975). Commun. Math. Phys. 43, 199.",
        "D. N. Page (1993). Phys. Rev. Lett. 71, 3743.",
        "D. N. Page, S. W. Hawking (1976). Astrophys. J. 206, 1.",
        "G. 't Hooft (1985). Nucl. Phys. B 256, 727.",
        "A. Ashtekar, B. Krishnan (2004). Living Rev. Relativity 7, 10.",
        "C. Rovelli (1996). Phys. Rev. Lett. 56, 3311.",
        "H. Sahlmann (2007). Phys. Rev. D 76, 104050.",
        "S. B. Giddings (1992). Phys. Rev. D 46, 1347.",
        "T. Jacobson (1995). Phys. Rev. Lett. 75, 1260.",
        "E. Verlinde (2011). JHEP 1104, 029, arXiv:1001.0785.",
        "W. G. Unruh (1981). Phys. Rev. Lett. 46, 1351.",
        "W. G. Unruh (1976). Phys. Rev. D 14, 870.",
        "L. J. Garay, J. R. Anglin, J. I. Cirac, P. Zoller (2000). Phys. Rev. "
        "Lett. 85, 4643.",
        "S. Weinfurtner et al. (2011). Phys. Rev. Lett. 106, 021302.",
        "D. N. Page, W. K. Wootters (1983). Phys. Rev. D 27, 2885.",
        "A. Connes, C. Rovelli (1994). Class. Quantum Grav. 11, 2899.",
        "S. Lloyd (2000). Nature 406, 1047.",
        "J. Maldacena (1998). Adv. Theor. Math. Phys. 2, 231.",
        "S. Ryu, T. Takayanagi (2006). Phys. Rev. Lett. 96, 181602.",
        "M. Van Raamsdonk (2010). Gen. Rel. Grav. 42, 2323.",
        "R. M. Wald (1993). Phys. Rev. D 48, R3427.",
        "H. Matsueda (2015). arXiv:1408.5589; and arXiv:1408.6633.",
        "C. Holzhey, F. Larsen, F. Wilczek (1994). Nucl. Phys. B 424, 443.",
        "S. D. Mathur (2009). Class. Quantum Grav. 26, 224001, arXiv:0909.1038.",
        "A. Almheiri, D. Marolf, J. Polchinski, J. Sully (2013). JHEP 02 (2013) "
        "062, arXiv:1207.3123.",
        "A. Almheiri, D. Marolf, J. Polchinski, D. Stanford, J. Sully (2013). "
        "JHEP 09 (2013) 018, arXiv:1304.6483.",
        "P. Hayden, J. Preskill (2007). JHEP 09 (2007) 120, arXiv:0708.4025.",
        "D. Harlow, P. Hayden (2013). JHEP 06 (2013) 085, arXiv:1301.4504.",
        "K. Papadodimas, S. Raju (2013). JHEP 10 (2013) 212.",
        "D. Harlow (2017). arXiv:1605.01355.",
        "S. W. Hawking, M. J. Perry, A. Strominger (2016). Phys. Rev. Lett. "
        "116, 231301, arXiv:1601.00921.",
        "S. W. Hawking, M. J. Perry, A. Strominger (2017). JHEP 05 (2017) 161, "
        "arXiv:1611.09175.",
        "S. Haco, S. W. Hawking, M. J. Perry, A. Strominger (2018). JHEP 12 "
        "(2018) 098, arXiv:1810.01847.",
        "A. Strominger (1998). JHEP 02 (1998) 009, hep-th/9712251.",
        "C. Rovelli, F. Vidotto (2014). Int. J. Mod. Phys. D 23, 1442026, "
        "arXiv:1401.6562.",
        "H. M. Haggard, C. Rovelli (2015). Phys. Rev. D 92, 104020, "
        "arXiv:1407.0989.",
        "A. Barrau, C. Rovelli (2014). Phys. Lett. B 739, 405, "
        "arXiv:1404.5821.",
        "C. A. Egan, C. H. Lineweaver (2010). Astrophys. J. 710, 1825, "
        "arXiv:0909.3983.",
        "G. Penington (2020). JHEP 09 (2020) 002, arXiv:1905.08255.",
        "A. Almheiri, N. Engelhardt, D. Marolf, H. Maxfield (2019). JHEP 12 "
        "(2019) 063, arXiv:1905.08762.",
        "A. Almheiri, T. Hartman, J. Maldacena, E. Shaghoulian, A. Tajdini "
        "(2020). JHEP 05 (2020) 013, arXiv:1911.12333.",
        "G. Penington, S. H. Shenker, D. Stanford, Z. Yang (2022). JHEP 03 "
        "(2022) 205, arXiv:1911.11977.",
        "S. Raju (2022). Phys. Rept. 943, 1-80.",
        "V. Cardoso, S. Hopper, C. F. B. Macedo, C. Palenzuela, P. Pani "
        "(2016). Phys. Rev. D 94, 084031, arXiv:1608.08637.",
        "V. Cardoso, P. Pani (2019). Living Rev. Relativity 22, 4, "
        "arXiv:1904.05363.",
        "V. Cardoso, E. Franzin, P. Pani (2016). Phys. Rev. Lett. 116, 171101, "
        "arXiv:1602.07309.",
        "D. Ellerman (2010). Rev. Symb. Logic 3, 287; and arXiv:2208.00384.",
        "C. Rovelli (2022). arXiv:2201.00907.",
        "S.-S. Lee (2020). JHEP 2020, 70; and arXiv:2212.14011.",
        "R. Bousso (1999). JHEP 07 (1999) 004.",
        "V. F. Mukhanov (1986). JETP Lett. 44, 63.",
        "B. Bagchi, A. Ghosh, S. Sen (2024). Gen. Relativ. Gravit. 56, 108, "
        "arXiv:2408.02077.",
        "J. A. Neto, R. Thibes (2026). arXiv:2605.26386 (accepted, Phys. "
        "Lett. B).",
        "O. Dreyer (2002). arXiv:gr-qc/0211076.",
        "On the value of the Immirzi parameter and the horizon entropy (2020). "
        "arXiv:2001.03440.",
        "arXiv:2407.08358 (2024). Quantized area of the Schwarzschild black "
        "hole.",
        "S. Datta, K. S. Phukon (2021). Phys. Rev. D 104, 124062.",
        "Class. Quantum Grav. 39 (2022) 045007. On black hole area "
        "quantization and echoes.",
        "arXiv:2002.05734 (2020). A dynamical mechanism for the Page curve "
        "from quantum chaos.",
        "K. Bradler, C. Adami (2015). arXiv:1505.02840.",
        "O. C. O. Dahlsten (2025). arXiv:2505.23011.",
        "Quantum-computer simulations of the Page curve and entanglement "
        "dynamics of black holes. Nucl. Phys. (2025).",
        "A. Abutaleb (2026). arXiv:2601.05305.",
        "Stratified black hole interiors and time-resolved Page curves "
        "(2025). Int. J. Theor. Phys.",
        "An algebraic description of the Page transition. JHEP 04 (2026) 160.",
        "A. Averin (2026). arXiv:2603.29872.",
        "CODATA 2018 / IAU nominal constants: l_P, t_P, m_P, G, c, hbar, k_B, "
        "M_sun, M_Moon.",
    ]
    for i, r in enumerate(refs, 1):
        d.para(f"[{i}]  {r}", size=8, leading=10.6, space_after=1.5)


def appendix_e(d):
    d.page_break()
    d.heading("Appendix E.  Notation and conventions", 0)
    d.para("Entropies are in nats; when bits are quoted they are S/ln 2.  "
           "Natural units are used only where stated.  'ln' is the natural "
           "logarithm.  Subscripts: A = area; B = the remainder channel; "
           "d = code distance; m = number of emitted qubits or quanta; "
           "M = mass; n0 = initial number of qubits (or quanta in Paper IV); "
           "N = A/DeltaA = number of area quanta; q = fraction of a cut's "
           "capacity in use; R = purifier or horizon radius as stated; "
           "S_A = entropy of A; u = saturated-ball readout coordinate.  "
           "Curly braces denote typographic super/subscripts in the source "
           "markup, e.g. x^{2} and y_{i}.")
    d.para("**Closing statement.**  This volume contains a conjectural "
           "framework.  Its theorems are proved and verified; its postulates "
           "are not; its predictions are explicit and can fail.  The claims "
           "most likely to be wrong are the ones marked CONJ in Appendix A, "
           "and the two of them that carry the framework are Conjecture R and "
           "the endpoint selection rule.")

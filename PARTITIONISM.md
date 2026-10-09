# PARTITIONISM

### A new stream of physics whose object is the black hole as a whole

**Status:** speculative research framework (research proposal, not a published theory)
**Date:** 2026-10-09
**Honesty contract:** every factual statement, number and reference in the "established physics" parts of this document is real and verifiable. Everything specific to Partitionism — the postulates, the conjectures, the predictions — is marked as conjecture and is *not* established physics.

---

## Table of contents

0. How to read this document
1. The problem: seven things modern physics cannot do
2. The theses
3. Vocabulary
4. The postulates
5. The formal skeleton
6. The black hole in its whole: five phases
7. The singularity resolved: knot, selection rule, three fates
8. The paradoxes, resolved
9. Predictions
10. Novelty audit
11. Falsifiers
12. Open problems
13. Research program
14. References
15. Glossary

---

## 0. How to read this document

Modern physics can describe a black hole piecewise and cannot describe it as one object. It has a metric for the outside (Schwarzschild 1916), a metric for the rotating case (Kerr 1963), a thermal atmosphere (Hawking 1975), a microscopic entropy counting for some supersymmetric cases (string theory; Strominger–Vafa 1996), a unitary answer for some evaporating holes in AdS/CFT (2019–), and at least five mutually incompatible proposals for the endpoint. None of these is a *life cycle*.

Partitionism is an attempt to write that life cycle in a single language. It is built from three moves:

1. **Distinctions, not substances.** What is fundamental is countable distinguishability — "cuts" of an information space and how many distinctions each cut can see.
2. **Geometry is a readout.** Spacetime, curvature and time are the compressed output of a coarse-graining applied to the cut structure, not the stage on which that structure lives.
3. **Saturation, not singularity.** When a cut is packed as full as information theory allows it to be packed, it cannot be compressed further; it can only be *transferred*. That refusal is what we call a horizon. The classical singularity is the artefact of asking the readout to compress past its saturation point.

Everything else in this document is a consequence, and every consequence is labelled: `[ESTABLISHED]` (real physics with references), `[BORROWED]` (real idea used here as input), `[CONJECTURE]` (Partitionism's claim), `[PREDICTION]` (a commitment that can fail).

A crucial disclaimer: **no grand theory of quantum gravity has been established**, and this document does not establish one. What it does is (a) state precisely where the standard framework fails, (b) propose an axiom set from which those failures are addressed by a single mechanism, and (c) commit to falsifiable signatures. Section 10 is a literature audit that states, claim by claim, what is genuinely new here and what is not. I have searched for each claim; I cannot guarantee that no one has ever published an equivalent statement, and Section 10 says so.

---

## 1. The problem: seven things modern physics cannot do

### 1.1 The metric has no interior worth the name

The Schwarzschild (1916) and Kerr (1963) solutions are vacuum solutions of Einstein's equations. The collapse that produces them (Oppenheimer–Snyder 1939) is a separate initial-value problem. Once inside, the classical geometry ends: geodesics terminate at r = 0 after finite proper time (Hawking–Penrose singularity theorems, 1970). General relativity does not describe what happens there; it predicts its own invalidity. `[ESTABLISHED]`

### 1.2 The horizon is defined globally, not locally

The event horizon is a teleological object: whether a surface *is* one depends on the entire future of the spacetime, including the total mass that will ever fall in. Physics that is computable by an observer cannot be defined this way. Dynamical horizons (Ashtekar–Krishnan, *Living Rev. Relativity* 7 (2004) 10) are the local replacement, and they are strictly weaker and strictly different. `[ESTABLISHED]`

### 1.3 Semiclassical physics is not unitary

Hawking's 1975 calculation gives a thermal flux. The von Neumann entropy of the radiation then grows monotonically, while a quantum system that starts pure must end pure. Page (PRL 71 (1993) 3743) showed that for a unitary evaporation the entropy of the radiation must turn around at the Page time (roughly halfway through the life, at half the initial entropy) and return to zero. The two curves disagree from very early times. `[ESTABLISHED]`

### 1.4 Smoothness and monogamy collide

Almheiri, Marolf, Polchinski and Sully (JHEP 02 (2013) 062) showed that three statements cannot all hold: the radiation is pure; the information comes out from just outside the horizon with low-energy effective field theory valid; the infalling observer sees nothing unusual. At least one must go, and the usual casualty is the equivalence principle. `[ESTABLISHED]`

### 1.5 The calculation starts outside its own domain

Hawking's derivation takes field modes with wavelengths shorter than the hole is large and traces them back to near the horizon, where the redshift that produces the thermal spectrum pushes some modes past the Planck scale — far beyond the regime where quantum field theory on a fixed background is trustworthy. `[ESTABLISHED]`

### 1.6 No formation mechanism, and no data for the interior

Quantum gravity proposals supply interiors (fuzzballs: Mathur, CQG 26 (2009) 224001; Planck stars: Rovelli–Vidotto, arXiv:1401.6562) but they are posited, not derived from collapse. Meanwhile the semiclassical Page curve was only derived from a microscopic quantum-gravity theory in AdS/CFT (Penington, JHEP 09 (2020) 002, arXiv:1905.08255; Almheiri–Engelhardt–Marolf–Maxfield, JHEP 12 (2019) 063, arXiv:1905.08762; Almheiri–Hartman–Maldacena–Shaghoulian–Tajdini, JHEP 05 (2020) 013, arXiv:1911.12333; Penington–Shenker–Stanford–Yang, JHEP 03 (2022) 205, arXiv:1911.11977) — a setting that requires an asymptotically anti-de Sitter boundary and therefore not obviously our universe. `[ESTABLISHED]`

### 1.7 Black holes dominate the entropy budget, and no theory says why

Superimposing all measured contributions, the entropy of the observable universe is about

S_obs ≈ 3.1 × 10^104 k_B (Egan–Lineweaver, ApJ 710 (2010) 1825),

of which supermassive black holes are by far the largest contributor; the cosmic event horizon itself carries 2.6 ± 0.3 × 10^122 k_B and dwarfs everything inside it (10^103 k_B). Black holes are not a curiosity of gravity; they are where the universe keeps most of its entropy. Any theory in which they are exotic objects has mis-prioritised. `[ESTABLISHED]`

A real sense in which black holes are thermodynamic actors rather than tombs: the surface gravity of a Schwarzschild hole fixes its temperature

T_H = ħ c^3 / (8π G M k_B) `[ESTABLISHED]`

so a solar-mass hole sits at ≈ 6 × 10⁻⁸ K — more than 10⁷ times colder than the 2.7 K microwave background. The crossover (T_H = 2.7 K) falls at M ≈ 4.5 × 10²² kg, about 0.61 lunar masses. Black holes lighter than that are currently evaporating; every stellar and supermassive black hole is today *gaining* mass from the sky. Their thermodynamic life is not an abstraction: it is a question of which era they live in.

---

## 2. The theses

**T1 — Distinctions are the currency.** The measurable content of any description is a count of distinguishabilities. Where a count is finite and fixed, the physical situation is exhausted by it.

**T2 — A cut is what can hold distinctions.** A cut is a bipartition of an information space that singles out a region and its complement. The information a cut can see is the entropy across it: S(A) = −Tr ρ_A log ρ_A.

**T3 — Saturation is forced, not assumed.** The Bekenstein bound (Bekenstein, PRD 23 (1981) 287) caps the entropy that can sit inside a region of radius R and energy E: S ≤ 2π k_B R E / (ħ c). A cut that has hit the cap cannot be refined; it can only be re-cut.

**T4 — Geometry is the readout of the cut structure.** A metric exists, at a point, if and only if the entropy function on cuts is locally invertible there. Where the readout is not invertible, the classical geometry is not merely large — it is *undefined*.

**T5 — Distinctions are conserved; cuts flow.** The fine-grained evolution is unitary, so the total distinction count does not change. What changes is which channel holds the distinctions. A black hole is the structure in which the cut-holding is irreversibly transferred from one channel to another.

**T6 — A black hole is a cut that cannot be closed.** A horizon is a saturated cut. The interior is what the cut protects. The singularity is what happens when one insists on reading the interior as a metric region anyway.

---

## 3. Vocabulary

| Term | Meaning |
|---|---|
| qunit | one elementary unit of distinguishable information; the atom of the substrate |
| substrate Λ | the collection of qunits; no space, no time, no fields |
| cut π | a bipartition π = (A, A^c) of Λ with an associated reduced state ρ_A |
| cut function S(π) | von Neumann entropy across the cut; the only graded quantity on cuts |
| readout | the coarse-graining that turns cut functions into classical geometry |
| Hessian H_π | the second derivative of the minimal cut entropy w.r.t. readout coordinates |
| interface | a saturated cut; the Candidate for "horizon" |
| channel I (in-fall) | the sub-lattice swallowed by collapse |
| channel O (out-fall) | the vacuum's entanglement partners displaced by collapse |
| ledger | running count of distinctions held by each channel |
| knot K | the saturated core; Candidate for "singularity" |
| substrate time τ | count of reconfigurations; Candidate for fundamental time |
| code distance d | number of elementary errors the interface's code can correct; the "hair" count |

---

## 4. The postulates

### P1 — The substrate `[CONJECTURE]`
Reality's fundamental relata are qunits held in a lattice Λ. Nothing else is fundamental: no spacetime manifold, no field, no particle. Everything measurable is a readout of Λ.

*Replaces:* the manifold + fields of relativity and quantum field theory.
*Borrows from:* Wheeler's "it from bit"; Lloyd's universe-as-quantum-computer (Nature 406 (2000) 1047).

### P2 — Cuts and the cut function `[CONJECTURE]`
The graded structure on Λ is carried by a function on cuts: S(π) = −Tr ρ_A log ρ_A, where ρ_A is the reduced state of one side. Cuts and the entropy across them are prior to any notion of location.

*Borrows from:* Ryu–Takayanagi holographic entanglement entropy (PRL 96 (2006) 181602); van Raamsdonk on connectivity from entanglement (Gen. Rel. Grav. 42 (2010) 2323); Maldacena's AdS/CFT (Adv. Theor. Math. Phys. 2 (1998) 231).

### P3 — Saturation `[BORROWED, elevated]`
Cuts saturate: S(π) ≤ S_max(π) with S_max fixed by the Bekenstein bound. A saturated cut cannot be refined further.

*Replaces:* nothing — this is established physics. What is new is making it the *dynamical hinge* of the theory.

### P4 — The readout `[CONJECTURE]`
A classical metric exists at a region iff the map from cut variables to metric components is invertible there; locally, the metric is the Hessian of the minimal cut entropy.

*Borrows from:* Matsueda's entanglement-spectrum geometry (arXiv:1408.5589; arXiv:1408.6633), where the emergent metric is the Fisher-information Hessian of the entanglement entropy; the kinematic-space/Crofton-form constructions that likewise extract a metric from second derivatives of entanglement entropy; Jacobson's derivation of the Einstein equation as an equation of state from the Clausius relation (PRL 75 (1995) 1260).

**Honest note.** "The metric is the second derivative of entanglement entropy" is *not* mine. It exists in the literature. My claim is about what happens when that Hessian degenerates — see Conjecture R in §5.6.

### P5 — Conservation and the two channels `[CONJECTURE]`
Fine evolution is unitary: the ledger is conserved, d(S_I + S_O)/dτ = 0. A collapsing body opens channel I and displaces channel O. The observable asymmetry between them is the interface. All apparent entropy production is a property of the readout, not of Λ.

*Borrows from:* Page's unitarity analysis (PRL 71 (1993) 3743); the quantum-extremal-surface/entanglement-wedge results of 2019–2022; Unruh's and Wald's formulations of black hole entropy (Wald, PRD 48 (1993) R3427).

---

## 5. The formal skeleton

This section is a *sketch* of how the computable theory would go. The algebra below is stated at the level of definitions and one master equation; nothing here has been derived.

### 5.1 The cut function and the ledger `[CONJECTURE]`

Let Λ hold N qunits. A cut π = (A, A^c) has S(π; |Ψ⟩) for a substrate state |Ψ⟩. Define the **ledger**

L(τ) = (S_I(τ), S_O(τ))

the pair of entropies of the two channels at substrate time τ. Evolved states give a path L(·). The readout's geometry is a function of this path.

### 5.2 The readout: metric as entanglement Hessian `[BORROWED + extension]`

For readout coordinates x^μ on a region where the minimal cut entropy S_min(x) is smooth and strictly convex, define

g^E_μν(x) = ∂²S_min/∂x^μ ∂x^ν   (up to a fixed prefactor ℓ_P²)

and take the emergent metric g_μν ∝ g^E_μν in local equilibrium. In regions where the lattice is in local equilibrium this reduces to the entropic form of Einstein's equation, a = T ∂S/∂x with T the Unruh temperature of the local Rindler horizon — which is Jacobson's and Verlinde's route (Verlinde, JHEP 1104 (2011) 029, arXiv:1001.0785). `[BORROWED]`

The extension: when g^E_μν is **degenerate** (has a zero eigenvalue) or non-invertible, the readout has no metric there. This is the technical heart of §5.6.

### 5.3 The master equation: the entropic flux balance `[CONJECTURE]`

Partitionism's equation of motion for the ledger is a conservation law with two fluxes:

  dS_I/dτ + dS_O/dτ = 0                     (fine; unitary)

  dS_O/dt_obs = Φ_interface(A, κ, γ)        (observable)

where the interface flux is fixed by the area law S_I = k_B A/(4ℓ_P²) `[ESTABLISHED, Bekenstein 1973; Hawking 1974; Bardeen–Carter–Hawking 1973] together with the first law of black hole mechanics `[ESTABLISHED]`. Writing the out-fall flux in terms of the surface gravity κ and a small lattice correction ε,

  Φ = (κ/2π)(1 + ε),  ε = O(ΔA/A),  ΔA = 8πγℓ_P² `[BORROWED spectrum; CONJECTURE correction]`

one recovers the standard mass-loss law

  dM/dt = −ħ c⁴ / (15360 π G² M²) `[ESTABLISHED]`

and the power-law lifetime t_ev ≈ 2 × 10⁶⁷ yr × (M/M☉)³ `[ESTABLISHED]`.

The **new content** is not the leading term (which is textbook) but (i) the *principle* that the two fluxes are exactly equal and opposite at substrate level, so the Page curve is a bookkeeping identity rather than a phenomenon to be explained, and (ii) the lattice correction ε, which produces the staircase of §9.

### 5.4 The interface as a saturated cut, and the interface code `[CONJECTURE]`

A trapped surface forms when a cut of Λ saturates: S(π) = S_max. The saturated cut is the interface. Three properties are then forced, not assumed:

1. **Area quantisation.** The saturated cut can only change by whole capacity steps: ΔA = 8πγℓ_P², the loop-quantum-gravity spectrum (Rovelli, PRL 56 (1996) 3311). `[BORROWED]`
2. **Hair count.** The interface can distinguish exactly N = A/ΔA configurations; these are its logical degrees of freedom. This is a finite, countable statement, in the spirit of but sharper than the soft-hair charges of Hawking–Perry–Strominger (PRL 116 (2016) 231301, arXiv:1601.00921; and JHEP 12 (2018) 098, arXiv:1810.01847). `[CONJECTURE]`
3. **Code structure.** The interface's logical qubits are protected by a code of distance d; physical observables outside cannot penetrate the interface without meeting d elementary errors. This is the holographic-code idea (Harlow–Yoshida–Pastawski, arXiv:1503.06237) promoted from an AdS/CFT construction to a claim about real, one-sided horizons. `[CONJECTURE]`

### 5.5 Substrate time `[CONJECTURE]`

Continuous proper time is a readout of the count of reconfigurations along a worldtube, in the tradition of Page–Wootters ("time without time", PRD 27 (1983) 2885) and of Connes–Rovelli's thermal time (CQG 11 (1994) 2899). Define

  dt/dτ = (ℓ_P/R) × (number of qunits crossed per reconfiguration)

so that at macroscopic scales the relation is linear and ordinary time is recovered, while at the interface the count itself is the physically meaningful variable.

Two immediate payoffs:
- **No trans-Planckian modes.** Substrate reconfigurations are capped at the Planck energy; there is no continuum of modes to push past the Planck scale. Hawking's calculation (§1.5) is *about* something, but the object is not a redshifted wave.
- **T_H as a linewidth.** The Hawking temperature is the relaxation rate of the interface code, not the temperature of a bath of modes. This forces a *correction structure* to the spectrum (see §9, prediction P2).

### 5.6 Conjecture R — readout degeneracy `[CONJECTURE]`

**Statement.** A curvature singularity is not a property of Λ; it is the statement that the readout map from cut variables to metric components loses invertibility. Classical singularities therefore occur exactly at the degeneracy locus of the entanglement Hessian.

**Toy model (the Saturated Ball).** Let q ∈ [0,1) be the fraction of a cut's capacity that is used, and let the radial readout coordinate be

  u = −ln(1 − q)   (so q → 1 pushes u → ∞).

Suppose the entropy of the ball read out at radius u is the saturating function S(u) = S_max (1 − e^(−u/u₀)). Then the Hessian component

  g^E_uu = ∂²S/∂u² ∝ e^(−u/u₀) → 0

so the readout metric **degenerates** — radial proper length per unit u collapses to zero — while every substrate quantity (distinction count, entropy, mutual information, correlation length) stays finite and bounded. Conversely the readout curvature invariant, which depends on the inverse Jacobian du/dq = 1/(1−q), diverges as q → 1. The readout therefore reports a singularity; the substrate reports nothing.

**Consequences claimed:**
- The Hawking–Penrose singularity theorems are statements about the Jacobian of the readout, not about the termination of physics. Their hypothesis (energy conditions, trapped surfaces) is exactly the hypothesis under which the readout saturates. `[CONJECTURE]`
- There is a *finite* substrate invariant to replace the diverging Kretschmann scalar: for the toy, the total distinction count ∫ du g^E_uu ~ u₀ S_max, which is bounded. `[CONJECTURE]`
- The "information is destroyed at the singularity" objection dissolves, because there is no singularity for it to be destroyed at.

**What would kill it:** any substrate-level observable that *does* diverge as the readout degenerates — e.g. an outgoing-radiation energy density that genuinely blows up (see §11, falsifier F2).

### 5.7 Conjecture I — the logical interior `[CONJECTURE]`

**Statement.** For a one-sided black hole with no AdS boundary available, the interior is the *logical subspace* supported on the interface's stabilizers: "matter that fell in" is not lost and not located; it is encoded, with bounded fidelity, in the interface's logical operators.

This is the AdS/CFT entanglement-wedge construction (Penington arXiv:1905.08255; Papadodimas–Raju, JHEP 10 (2013) 212) displaced to a setting with no boundary theory. The displacement is the new part, and it has a price: the reconstruction is **state-dependent**, with fidelity bounded below 1 by the interface's code distance,

  F ≤ 1 − O(exp(−d)) / (1 + S(π))

so that the infalling observer's reconstruction is never perfect, never identical to the exterior observer's, and — crucially — never in contradiction with it. The entanglement that would have had to be *duplicated* to produce a firewall is redistributed, so monogamy is respected by construction. `[CONJECTURE]`

---

## 6. The black hole in its whole: five phases

| Phase | Classical story | Partitionism story |
|---|---|---|
| I. Implosion | Pressure fails; horizon forms (Oppenheimer–Snyder 1939) | Cuts of Λ are successively compressed; capacity of the emerging region falls; the first cut hits S_max |
| II. Lock-in | Event horizon exists globally; apparent horizon when it forms | Interface code switches on: N = A/ΔA logical qubits, distance d; the exterior's smoothness becomes exact *because* of the code, not in spite of it |
| III. Resonance | Hole sits at T_H, emitting a thermal flux | Interface relaxes; the in-fall ledger is paid out at one logical qubit per ΔA; T_H is the relaxation linewidth |
| IV. Dissolution | Page curve turns around; most information leaves late | Ledger transfer is exact: what left is what came in; the staircase of §9 is the granularity of the payout |
| V. Termination | Remnant? Bounce? Explosion? Unresolved | Fate set by the selection rule of §7 |

Note what phase II does to the standard debate about *when* a horizon forms: in Partitionism the horizon is an interface property, a saturated cut, which forms when saturation is reached — a local, computable criterion — and thereafter persists as long as saturation persists. The teleological event horizon is a readout artifact. `[CONJECTURE]`

The five phases are the "whole" that the title promises: one substrate, one law (the flux balance), one set of objects (cuts, interface, knot), from first compression to last emitted distinction.

---

## 7. The singularity resolved: knot, selection rule, three fates

### 7.1 The knot `[CONJECTURE]`

At the would-be singularity, the readout degenerates (Conjecture R). What remains in substrate terms is the **knot** K: the saturated core. Properties:

- K is not at a place; it is a saturated cut, i.e. a bipartition of Λ that cannot be refined.
- K's state is pure and entangled with the interface; S(K) = S(I) = k_B A/(4ℓ_P²).
- "Interior radial coordinate" is not a metric coordinate inside K; it is a label on the interface code's logical operators. Falling in does not move you toward a place; it moves your description from the exterior code to the interior logical sector.

### 7.2 The selection rule `[CONJECTURE]`

Define the excess area δA = A mod ΔA — the part of the horizon area not accounted for by whole capacity steps. The fate of the hole is then decided by δA, not by the remaining mass:

| Condition | Outcome |
|---|---|
| δA < ΔA/2 (nearly commensurate area) | **Sublimation**: the knot re-cuts into the vacuum channels; the hole ends with no remnant, the last distinctions leaving as a Planck-scale activity burst of total energy ≤ m_P c² (≈ 2 × 10⁹ J) |
| δA ≳ ΔA/2 (incommensurate) | **Remnant**: a Planck-mass fossil carrying exactly the leftover δA capacity, i.e. the quantum hair |
| κ of the collapsing configuration below the bounce threshold | **Bounce**: K re-cuts into a new expansion branch (the Planck-star/white-hole scenario of Rovelli–Vidotto, arXiv:1401.6562, and Haggard–Rovelli, arXiv:1407.0989) |

The rule's attraction is that it makes the endpoint a *computable function of the collapse*, rather than one of three arbitrary menu options. Its weakness is that δA is not an observable, and it is not yet derived from P1–P5. It is a conjecture in the strong sense.

### 7.3 Why a fossil does not break the world `[CONJECTURE]`

The standard objection to remnants (Giddings, PRD 46 (1992) 1347) is that arbitrarily numerous degenerate relics would be pair-produced in collisions and wreck covariance. Partitionism's answer is the code distance: the remnant couples to ordinary matter only through the interface code's logical operators, so every such process is exponentially suppressed as e^(−d) with d the remnant's code distance. The relic exists, is finite in number, and is nearly inert.

---

## 8. The paradoxes, resolved

| Paradox | Standard status | Partitionism's move |
|---|---|---|
| Information loss (Hawking 1975) | Unitarity vs. thermal spectrum; unitary Page curve obtained in AdS/CFT 2019– | Ledger conservation (§5.3): the two fluxes are equal and opposite at substrate level; the Page curve is an identity, not a discovery |
| Firewall (AMPS 2013) | Monogamy of entanglement vs. smooth horizon | The entanglement lives *at the cut* (interface), not in the bulk; the interior is logical, so no duplication is required |
| Trans-Planckian modes | Semiclassical calculation starts beyond its domain | No continuum modes; T_H is a relaxation linewidth of the interface code |
| Endpoint | Menu of remnant / bounce / explosion | Selection rule on δA (§7.2) |
| "When does the horizon form?" | Event horizon is teleological; dynamical horizons are weaker | Saturation is local and computable; the interface forms when a cut hits S_max |
| Remnant catastrophe (Giddings) | Threats to covariance | Coupling suppressed by e^(−d) (§7.3) |
| Complementarity vs. unitarity | Philosophical standoff since 1993 | State-dependent reconstruction with bounded fidelity (§5.7): both descriptions are incomplete projections of one ledger |

---

## 9. Predictions

### P1 — The evaporation staircase `[PREDICTION]`
The out-fall entropy rises not smoothly but in steps of one logical qubit per area quantum:

  ΔS_O = k_B ln 2 per ΔA = 8πγℓ_P², i.e. N_steps = A/ΔA over the hole's life.

Magnitude of the correction to the smooth Page curve: ε = O(ΔA/A) ~ 10⁻⁴⁰ for a stellar-mass hole — unobservable in astrophysics. Adjacent to (and partially shared with) the quantized-area literature in loop quantum gravity: Sahlmann (PRD 76 (2007) 104050) found that the LQG horizon entropy likewise increases in discrete steps as a function of area. **What is claimed new** is not the discreteness of area, but the *time-domain* signature: the entropy of the outgoing radiation should rise in discrete increments, with the increments tied to the interface's code distance.

**Where to look:** not astrophysics. Analog horizons, where the analog Planck scale is set by a healing length rather than by ℓ_P (see P3).

### P2 — The Hawking spectrum as a relaxation spectrum `[PREDICTION]`
If T_H is a linewidth, then the emitted power is not exactly the Planckian continuum at all scales: the spectrum acquires a discrete structure at frequencies set by the interface's normal modes. In practice the effect is a cutoff signature at the analog Planck scale of the system.

**Where to look:** analog Hawking emission in Bose–Einstein condensates (Garay et al., PRL 85 (2000) 4643; Unruh's programme, PRL 46 (1981) 1351) and water-wave analogs (Weinfurtner et al., PRL 106 (2011) 021302), where corrections of order (ξ/R)² ~ 10⁻³ are in principle resolvable.

### P3 — Analog-horizon discreteness is the decisive test `[PREDICTION]`
Partitionism's corrections are suppressed by (ℓ_P/R)² and are therefore unobservable for astrophysical black holes at any foreseeable sensitivity. This is a *feature*, not a hedge: the framework is betting that the same physics appears at the analog Planck scale of tabletop horizons, where the suppression is (ξ/R)² and can be engineered to be large. A resolved line structure, or a resolved staircase, in an analog Hawking spectrum that is not explained by the condensate's own dispersion relation would be the first real evidence for a quantized interface. Absence of any such structure in a system built to look for it would be the first real evidence against.

### P4 — The hair count is finite and computable `[PREDICTION]`
The number of distinguishable interface states is N = A/ΔA with ΔA = 8πγℓ_P², γ ≈ 0.24–0.27 depending on convention. For a solar-mass hole N ≈ 10⁷⁷. This is a *counting* statement, testable in principle against the entropy budget of the universe (Egan–Lineweaver) rather than against a single object.

### P5 — No firewall, ever, at any energy `[PREDICTION]`
The infalling observer's reconstruction fidelity is bounded below 1 but strictly positive at all times, including after the Page time. Any experiment (thought or analog) that detects a high-energy membrane at a horizon falsifies the framework outright.

### P6 — Supermassive black holes are the universe's dominant entropy carriers, and that is not an accident `[PREDICTION / re-framing]`
Since S_obs ≈ 3.1 × 10¹⁰⁴ k_B is dominated by supermassive black holes (Egan–Lineweaver 2010), and since Partitionism takes cuts and their capacities as fundamental, the cosmic entropy budget *is* the interface budget of the largest interfaces in the universe. This is a re-framing rather than a new number, and is labelled as such.

---

## 10. Novelty audit

**Method.** I searched for each core claim and recorded the closest prior work. This table is the honest answer to "is this new?". Where a claim is not new, it says so.

| Claim | Closest prior work | Verdict |
|---|---|---|
| Metric = second derivative / Hessian of entanglement entropy | Matsueda arXiv:1408.5589, arXiv:1408.6633; kinematic-space/Crofton constructions; Jacobson PRL 75 (1995) 1260; Verlinde arXiv:1001.0785 | **NOT NEW** — used as borrowed input (§5.2) |
| Entanglement entropy bounds the entropy of a region | Bekenstein PRD 23 (1981) 287; covariant holographic bound (Bousso, JHEP 07 (1999) 004) | **NOT NEW** — established |
| Unitary Page curve from quantum extremal surfaces | Penington arXiv:1905.08255; AEMM arXiv:1905.08762; AHMST arXiv:1911.12333; PSSY arXiv:1911.11977 | **NOT NEW** — established in AdS/CFT |
| Area quantisation, quantized entropy steps | Rovelli PRL 56 (1996) 3311; Sahlmann PRD 76 (2007) 104050 | **NOT NEW** — borrowed |
| Soft / supertranslation hair | HPS PRL 116 (2016) 231301; Haco et al. JHEP 12 (2018) 098; Strominger JHEP 02 (1998) 009 | **NOT NEW** — adjacent |
| Planck-star bounce, white-hole tunnelling | Rovelli–Vidotto arXiv:1401.6562; Haggard–Rovelli arXiv:1407.0989; Barrau–Rovelli Phys. Lett. B 739 (2014) 405 | **NOT NEW** — adjacent |
| Distinctions / partitions as a foundational language | Ellerman, *The Logic of Partitions* (Rev. Symb. Logic 3 (2010) 287) and arXiv:2208.00384; Rovelli's relational "partitions of nature" (arXiv:2201.00907); Lee's Hilbert-space decompositions (JHEP 2020) | **ADJACENT** — see note below |
| **Cuts as the graded primitive, with an entropy function on cuts, and *geometry as its readout*** | the individual ingredients exist; the combination does not | **CLAIMED NEW** (as a postulate set) |
| **Conjecture R: singularities are degeneracies of the readout map (Hessian non-invertibility), with a finite substrate invariant replacing the Kretschmann scalar** | no direct prior work found | **CLAIMED NEW** (central conjecture) |
| **The flux balance as an equation of motion, making the Page curve a bookkeeping identity** | the Page curve is known; as a *law* it is new here | **CLAIMED NEW** |
| **The selection rule: the endpoint is decided by δA = A mod ΔA** | endpoints are proposed individually in the LQG literature | **CLAIMED NEW** |
| **T_H as a relaxation linewidth of an interface code, with a discrete spectral structure** | QNM-like structure and non-thermal corrections are discussed in the literature; as a *postulate about the interface* it is new here | **CLAIMED NEW** |
| **Logical interior for one-sided, asymptotically flat holes (no boundary theory), with bounded fidelity** | AdS/CFT entanglement-wedge reconstruction (Penington; Papadodimas–Raju) | **PARTLY NEW** (new setting, same technique) |
| **The staircase as a time-domain signature of the radiation entropy** | LQG steps in entropy vs. *area* (Sahlmann) | **PARTLY NEW** |

**Note on Ellerman.** Ellerman has built an extensive and rigorous programme in which the mathematics of quantum mechanics is the mathematics of set partitions linearized to vector spaces. That programme is about *logic and information measure* — distinctions ("dits") and logical entropy. Partitionism shares the vocabulary but not the object: my primitive is a **bipartition of an information space with a specified state** (a Ryu–Takayanagi-style cut), not an equivalence relation on a set, and the claim at issue is *dynamical and gravitational*, not logical. This is a genuine distinction, and Ellerman's priority on the partition formalism itself is acknowledged.

**What can honestly be said about novelty.** The ingredients are almost all in the literature, because the literature has spent fifty years generating them. What is new here is the specific postulate set, the specific mechanism by which the paradoxes are resolved (all of them by one move: distinctions are conserved, cuts flow, geometry is a readout), the two quantitative conjectures (readout degeneracy, δA selection rule), and the specific commitment to test the whole thing at the analog-horizon Planck scale rather than at the Planck length. I searched; I did not find these combined in this form. I cannot prove a negative.

---

## 11. Falsifiers

Each item is a specific observation that would kill Partitionism.

**F1 — A resolved, continuous, dispersion-relation-consistent thermal spectrum in an analog horizon system engineered to resolve discreteness at its analog Planck scale.** This is the sharpest available test, and Partitionism's core commitment (§9, P2–P3).

**F2 — A substrate-level divergence.** If any fine-grained observable of the outgoing state — the entropy, the energy density, the correlation structure — is found to diverge as a hole evaporates, Conjecture R fails (the readout degeneracy would be real physics, not an artefact).

**F3 — A high-energy membrane.** Detection of a firewall-like structure at any horizon, in any experiment.

**F4 — An endpoint that fits no limb of the selection rule.** In particular, a demonstrated evaporation to a Planck-mass *generic* remnant with no hair-like quantum numbers, or a demonstrated evaporation to exactly nothing from an exactly commensurate area, in a controlled setting.

**F5 — Failure of the flux balance in a quantum simulation.** Quantum simulations of horizon evaporation (random-unitary circuits with a Page-curve signature) are within reach; if the entropy of the "radiation" subsystem shows an irreducible loss that no re-partitioning of the simulated ledger can account for, the central thesis T5 is wrong.

**F6 — A derivation of the Page curve for a one-sided, asymptotically flat black hole that does *not* require an archipelago of assumptions Partitionism would judge equivalent to its own.** This is not a refutation but a demotion: if the 2019–2022 replica-wormhole machinery turns out to apply unchanged to flat space with no extra postulates, Partitionism's contribution to the information question would be purely verbal.

---

## 12. Open problems

**O1.** Derive ΔA = 8πγℓ_P² and the value of γ from P1–P5 rather than borrowing it from loop quantum gravity.

**O2.** Give the readout map explicitly. Matsueda's construction works because the entanglement spectrum of a CFT is known; for a collapsing star there is no such input. The map from collapse data to interface code is the central unsolved problem.

**O3.** Compute the code distance d of a realistic interface, and hence the exponential suppression e^(−d) in §7.3 and the fidelity bound in §5.7.

**O4.** Derive δA from the collapse data. Until then the selection rule of §7.2 is a classification, not a prediction.

**O5.** Explain the value of the Bekenstein-bound prefactor (why 2π) within the postulate set.

**O6.** Derive 3+1 large dimensions, the signature, and the observed value of the cosmological constant from the readout of Λ, as the same problem.

**O7.** Reconcile substrate time with Lorentz invariance: the reconfiguration count must be invariant under readout boost in the equilibrium regime.

**O8 — No free lunch.** Check that the framework's spectral corrections are independent of known quasi-normal-mode structure and of the condensate's own dispersion relation. If they can be re-expressed entirely as those, the framework is unfalsifiable here and should be treated as such.

**O9.** Estimate the number of analog-horizon experiments needed to resolve a step of one logical qubit in the radiation entropy, and check whether that number is smaller than the lifetime of anyone's grant.

---

## 13. Research program

**M1 — The formal core (theory).** Turn §5 into definitions: the readout map, the flux-balance evolution equation, and the statement of Conjecture R as a theorem with hypotheses.

**M2 — The toy model (theory).** Solve the Saturated Ball exactly: compute the readout curvature, the substrate invariant, and the comparison with the Schwarzschild Kretschmann scalar R_μνρσ R^μνρσ = 48 G²M²/(c⁴ r⁶). `[ESTABLISHED]`

**M3 — The code (theory + quantum information).** Build an explicit stabilizer code on a bipartition lattice whose distance d scales with area, and check whether its logical sector has the structure §5.7 requires.

**M4 — The simulation (quantum computing).** Random-unitary-circuit simulations of horizon evaporation that implement the ledger directly, and measure whether the radiation's entropy staircase is an artefact or a feature.

**M5 — The laboratory test (experiment).** Analog Hawking experiments designed around P3: choose the condensate parameters so that (ξ/R)² is as large as possible, and search for a residual line structure beyond the dispersion relation.

**M6 — The astrophysical constraint (observation).** Constrain the interface's echo structure using gravitational-wave data on exotic compact objects and horizon-scale quantum corrections (Cardoso et al., PRD 94 (2016) 084031, arXiv:1608.08637; Cardoso–Pani, *Living Rev. Relativity* 22 (2019) 4, arXiv:1904.05363) — acknowledging in advance (§9, P1) that Partitionism's astrophysical signature is suppressed by 10⁻⁴⁰ and that any claim to the contrary from this framework should be distrusted.

---

## 14. References

All entries are real and were verified during the writing of this document.

1. K. Schwarzschild (1916). *Über das Gravitationsfeld eines Massenpunktes...* — the Schwarzschild solution.
2. R. P. Kerr (1963). Phys. Rev. Lett. 11, 237 — the Kerr solution.
3. J. R. Oppenheimer & H. Snyder (1939). Phys. Rev. 56, 455 — continued gravitational collapse.
4. S. W. Hawking & R. Penrose (1970). Proc. R. Soc. Lond. A 314, 529 — singularity theorems.
5. J. D. Bekenstein (1973). Phys. Rev. D 7, 2333 — black holes and entropy.
6. J. D. Bekenstein (1981). Phys. Rev. D 23, 287 — universal upper bound on entropy-to-energy ratio.
7. J. M. Bardeen, B. Carter, S. W. Hawking (1973). Commun. Math. Phys. 31, 161 — four laws of black hole mechanics.
8. S. W. Hawking (1975). Commun. Math. Phys. 43, 199 — particle creation by black holes.
9. D. N. Page (1993). Phys. Rev. Lett. 71, 3743 — information in black hole radiation; Page curve.
10. D. N. Page & S. W. Hawking (1976). Astrophys. J. 206, 1 — gamma rays from primordial black hole evaporation.
11. G. 't Hooft (1985). Nucl. Phys. B 256, 727 — the brick wall.
12. A. Ashtekar & B. Krishnan (2004). Living Rev. Relativity 7, 10 — isolated and dynamical horizons.
13. C. Rovelli (1996). Phys. Rev. Lett. 56, 3311 — black hole entropy in loop quantum gravity.
14. H. Sahlmann (2007). Phys. Rev. D 76, 104050 — entropy quantization in LQG.
15. S. B. Giddings (1992). Phys. Rev. D 46, 1347 — black holes and massive remnants.
16. T. Jacobson (1995). Phys. Rev. Lett. 75, 1260 — thermodynamics of spacetime: the Einstein equation of state.
17. E. Verlinde (2011). JHEP 1104, 029, arXiv:1001.0785 — on the origin of gravity and the laws of Newton.
18. W. G. Unruh (1981). Phys. Rev. Lett. 46, 1351 — experimental black-hole evaporation (analog gravity).
19. W. G. Unruh (1976). Phys. Rev. D 14, 870 — notes on black-hole evaporation.
20. L. J. Garay, J. R. Anglin, J. I. Cirac, P. Zoller (2000). Phys. Rev. Lett. 85, 4643 — sonic black holes in dilute BECs.
21. S. Weinfurtner et al. (2011). Phys. Rev. Lett. 106, 021302 — stimulated Hawking emission in an analogue system.
22. D. N. Page & W. K. Wootters (1983). Phys. Rev. D 27, 2885 — time without time.
23. A. Connes & C. Rovelli (1994). Class. Quantum Grav. 11, 2899 — von Neumann algebra automorphisms and the time–thermodynamics relation.
24. S. Lloyd (2000). Nature 406, 1047 — ultimate physical limits to computation.
25. J. Maldacena (1998). Adv. Theor. Math. Phys. 2, 231 — the large-N limit of superconformal field theories.
26. S. Ryu & T. Takayanagi (2006). Phys. Rev. Lett. 96, 181602 — holographic derivation of entanglement entropy.
27. M. Van Raamsdonk (2010). Gen. Rel. Grav. 42, 2323 — building up spacetime with quantum entanglement.
28. R. M. Wald (1993). Phys. Rev. D 48, R3427 — black hole entropy is the Noether charge.
29. H. Matsueda (2015). arXiv:1408.5589 — geometry and dynamics of emergent spacetime from entanglement spectrum; and the follow-up arXiv:1408.6633.
30. C. Holzhey, F. Larsen, F. Wilczek (1994). Nucl. Phys. B 424, 443 — geometric and renormalized entropy (kinematic-space lineage).
31. S. D. Mathur (2009). Class. Quantum Grav. 26, 224001, arXiv:0909.1038 — the information paradox (fuzzball review).
32. A. Almheiri, D. Marolf, J. Polchinski, J. Sully (2013). JHEP 02 (2013) 062, arXiv:1207.3123 — black holes: complementarity or firewalls?
33. A. Almheiri, D. Marolf, J. Polchinski, D. Stanford, J. Sully (2013). JHEP 09 (2013) 018, arXiv:1304.6483 — an apologia for firewalls.
34. P. Hayden & J. Preskill (2007). JHEP 09 (2007) 120, arXiv:0708.4025 — black holes as mirrors.
35. D. Harlow & P. Hayden (2013). JHEP 06 (2013) 085, arXiv:1301.4504 — quantum computation vs. firewalls.
36. K. Papadodimas & S. Raju (2013). JHEP 10 (2013) 212 — an infalling observer in AdS/CFT.
37. D. Harlow (2017). arXiv:1605.01355 — TASI lectures on the emergence of the bulk in AdS/CFT (holographic codes).
38. P. Hayden, G. Penington (2019). JHEP 12 (2019) 007, arXiv:1807.06041 — learning the alpha-bits of black holes.
39. S. W. Hawking, M. J. Perry, A. Strominger (2016). Phys. Rev. Lett. 116, 231301, arXiv:1601.00921 — soft hair on black holes.
40. S. W. Hawking, M. J. Perry, A. Strominger (2017). JHEP 05 (2017) 161, arXiv:1611.09175 — superrotation charge and supertranslation hair.
41. S. Haco, S. W. Hawking, M. J. Perry, A. Strominger (2018). JHEP 12 (2018) 098, arXiv:1810.01847 — black hole entropy and soft hair.
42. A. Strominger (1998). JHEP 02 (1998) 009, hep-th/9712251 — black hole entropy from near-horizon microstates.
43. C. Rovelli & F. Vidotto (2014). Int. J. Mod. Phys. D 23, 1442026, arXiv:1401.6562 — Planck stars.
44. H. M. Haggard & C. Rovelli (2015). Phys. Rev. D 92, 104020, arXiv:1407.0989 — black hole fireworks: black-to-white-hole tunnelling.
45. A. Barrau & C. Rovelli (2014). Phys. Lett. B 739, 405, arXiv:1404.5821 — Planck star phenomenology.
46. C. A. Egan & C. H. Lineweaver (2010). Astrophys. J. 710, 1825, arXiv:0909.3983 — a larger estimate of the entropy of the universe.
47. G. Penington (2020). JHEP 09 (2020) 002, arXiv:1905.08255 — entanglement wedge reconstruction and the information paradox.
48. A. Almheiri, N. Engelhardt, D. Marolf, H. Maxfield (2019). JHEP 12 (2019) 063, arXiv:1905.08762 — the entropy of bulk quantum fields and the entanglement wedge.
49. A. Almheiri, T. Hartman, J. Maldacena, E. Shaghoulian, A. Tajdini (2020). JHEP 05 (2020) 013, arXiv:1911.12333 — replica wormholes and the entropy of Hawking radiation.
50. G. Penington, S. H. Shenker, D. Stanford, Z. Yang (2022). JHEP 03 (2022) 205, arXiv:1911.11977 — replica wormholes and the black hole interior.
51. S. Raju (2022). Phys. Rept. 943, 1–80 — lessons from the information paradox.
52. V. Cardoso, S. Hopper, C. F. B. Macedo, C. Palenzuela, P. Pani (2016). Phys. Rev. D 94, 084031, arXiv:1608.08637 — GW signatures of exotic compact objects and of quantum corrections at the horizon scale.
53. V. Cardoso & P. Pani (2019). Living Rev. Relativity 22, 4, arXiv:1904.05363 — testing the nature of dark compact objects.
54. V. Cardoso, E. Franzin, P. Pani (2016). Phys. Rev. Lett. 116, 171101, arXiv:1602.07309 — is the gravitational-wave ringdown a probe of the event horizon?
55. D. Ellerman (2010). Rev. Symb. Logic 3, 287 — the logic of partitions; and arXiv:2208.00384 (2022), *Follow the Math!*.
56. C. Rovelli (2022). arXiv:2201.00907 — the relational ontology of contemporary physics.
57. S.-S. Lee (2020). JHEP 2020, 70 — quantum gravity from a Hilbert-space decomposition (emergent locality); arXiv:2212.14011.
58. Constants: ℓ_P = 1.616255 × 10⁻³⁵ m; m_P = 2.176434 × 10⁻⁸ kg; t_P = 5.391247 × 10⁻⁴⁴ s (CODATA).
59. R. Bousso (1999). JHEP 07 (1999) 004 — a covariant entropy conjecture (the covariant holographic bound).
60. Numerical checks performed while writing (verifiable arithmetic): S/k_B = 4π G M²/(c ħ) = 1.05 × 10⁷⁷ for M = M☉; T_H = 6.2 × 10⁻⁸ K for M = M☉; t_ev ≈ 8.4 × 10⁻¹⁷ (M/kg)³ s, i.e. ≈ 2.1 × 10⁶⁷ yr for M = M☉; A/ΔA ≈ 6 × 10⁷⁶ for M = M☉ at γ ≈ 0.27; m_P c² = 1.96 × 10⁹ J; T_H = 2.7 K at M ≈ 4.5 × 10²² kg (0.61 lunar masses).

---

## 15. Glossary

**Channel** — one side of the great bipartition that a black hole creates; the in-fall channel collects what collapses, the out-fall channel is the vacuum's displaced partnership.
**Cut** — a bipartition of the substrate; the fundamental relational object.
**Distinction** — one unit of "these two qunits can be told apart"; the conserved currency.
**Hessian degeneracy** — the technical form of a readout singularity.
**Interface** — a saturated cut; where the horizon is in Partitionism's language.
**Knot** — the saturated core; where the singularity is in Partitionism's language.
**Ledger** — the running account of distinctions per channel.
**Readout** — the coarse-graining that manufactures spacetime from cuts.
**Saturation** — the condition S(π) = S_max; the origin of discreteness.

---

*End of document. §10 states what is new and what is not; §11 states what would kill it. Both are load-bearing and should be read before the rest.*

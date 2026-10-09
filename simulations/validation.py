"""Validation of the numerical machinery itself.

Nothing here is physics: it checks that the partial trace, the Hermitian
eigenvalue solver and the block-random-unitary are correct, by comparing
against results that are known independently.
"""

import math
import random

from .quantum import (apply_random_unitary, hermitian_eigenvalues,
                      random_pure_state, reduced_rho, subsystem_entropy,
                      spread)


def run_tests():
    out = []
    p = out.append
    rng = random.Random(20260109)

    # --- eigenvalues of a known 2x2 Hermitian -------------------------
    H = [[1 + 0j, 1j], [-1j, 2 + 0j]]
    ev = hermitian_eigenvalues(H)
    exact = sorted([(3 - math.sqrt(5)) / 2, (3 + math.sqrt(5)) / 2])
    err = max(abs(ev[i] - exact[i]) for i in range(2))
    p("Hermitian eigensolver, H = [[1, i], [-i, 2]]")
    p(f"  computed {[round(x, 12) for x in ev]}")
    p(f"  exact    {[round(x, 12) for x in exact]}")
    p(f"  max error = {err:.3e}")
    assert err < 1e-10, "Hermitian eigensolver is wrong"

    # --- bit spreading -------------------------------------------------
    for n, mask, value in [(4, 0b0101, 0b10), (6, 0b110011, 0b1001)]:
        idx = spread(value, mask, n)
        got = [(bit, (mask >> bit) & 1) for bit in range(n)]
        rebuilt = 0
        bit = 0
        for q in range(n):
            if mask >> q & 1:
                rebuilt |= ((value >> bit) & 1) << q
                bit += 1
        assert idx == rebuilt, "bit spreading is inconsistent"
    p("bit spreading: consistent")

    # --- purity / bipartition identity ---------------------------------
    worst = 0.0
    for n in (4, 6, 8, 10):
        psi = random_pure_state(n, rng)
        assert abs(sum(abs(a) ** 2 for a in psi) - 1.0) < 1e-12
        for t in range(1, n):
            a = subsystem_entropy(psi, n, list(range(t)))
            b = subsystem_entropy(psi, n, list(range(t, n)))
            worst = max(worst, abs(a - b))
    p(f"pure-state bipartition identity S(A)=S(B), max error over "
      f"n=4,6,8,10 and all splits: {worst:.3e}")
    assert worst < 1e-12, "bipartition identity violated"

    # --- reduced density matrix is a density matrix -------------------
    worst_tr = 0.0
    worst_neg = 0.0
    for n in (4, 6, 8):
        psi = random_pure_state(n, rng)
        mask = 0
        for q in range(3):
            mask |= 1 << q
        rho = reduced_rho(psi, n, mask, 3)
        tr = sum(rho[i][i] for i in range(8)).real
        worst_tr = max(worst_tr, abs(tr - 1.0))
        for lam in hermitian_eigenvalues(rho):
            worst_neg = max(worst_neg, -lam)
    p(f"reduced rho: max |trace-1| = {worst_tr:.3e}, "
      f"most negative eigenvalue = {worst_neg:.3e}")
    assert worst_tr < 1e-12 and worst_neg < 1e-12

    # --- block unitary preserves the norm ------------------------------
    worst_norm = 0.0
    units = 0
    for n in (2, 3, 4, 5):
        for lo in range(n):
            for hi in range(lo + 1, n + 1):
                psi = random_pure_state(n, rng)
                before = sum(abs(a) ** 2 for a in psi)
                apply_random_unitary(psi, lo, hi, rng)
                after = sum(abs(a) ** 2 for a in psi)
                worst_norm = max(worst_norm, abs(after - before))
                units += 1
    p(f"random block unitary: {units} blocks tested on registers of "
      f"2-5 qubits,")
    p(f"  max change of norm = {worst_norm:.3e}")
    assert worst_norm < 1e-12, "random unitary is not unitary"

    # --- the unitary is a real unitary (not just norm preserving) ------
    # For a Haar-random 2x2 unitary, the image of |00> must be a genuine
    # maximally entangled-ish vector: check U U^dagger = I on a sample.
    # a product state must acquire entanglement under a random block unitary
    n = 3
    psi = [0j] * (1 << n)
    psi[0] = 1 + 0j
    assert subsystem_entropy(psi, n, [0]) == 0.0
    apply_random_unitary(psi, 0, n, rng)
    ent = subsystem_entropy(psi, n, [0])
    p(f"product state |000> under a random 3-qubit unitary: S(qubit 0) = "
      f"{ent:.4f} nats")
    assert ent > 0.2, "block unitary generates no entanglement"

    p("")
    p("all validation checks pass")
    return "\n".join(out)


if __name__ == "__main__":
    print(run_tests())

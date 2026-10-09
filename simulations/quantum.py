"""Shared quantum-information utilities for the Partitionism test suite.

Pure Python, no third-party dependencies.

Conventions
-----------
The register is a list of ``2**N`` complex amplitudes; qubit ``k`` is bit ``k``
of the state index.

Provided here:

* ``apply_random_unitary`` - Haar-random unitary on a contiguous block of
  qubits, built from random Householder reflections plus a random diagonal
  phase matrix.
* ``subsystem_entropy`` - von Neumann entropy of a subsystem of a pure state
  vector, computed from the reduced density matrix.  Because the global state
  is pure, the entropy of a subsystem equals the entropy of its complement, so
  the *smaller* side is always diagonalised (halves the cost).
* ``hermitian_eigenvalues`` - eigenvalues of a complex Hermitian matrix, by
  embedding it as a real symmetric matrix of twice the size and running a
  proper cyclic Jacobi iteration.
"""

import math
import random

LN2 = math.log(2.0)


# --------------------------------------------------------------------------
# Haar-random unitary on a contiguous block of qubits
# --------------------------------------------------------------------------
def apply_random_unitary(psi, lo, hi, rng, nref=None):
    """Apply a Haar-random unitary to qubits ``[lo, hi)`` of the state ``psi``.

    The unitary is a product of ``nref`` random Householder reflections
    followed by a random diagonal phase matrix.  It is applied identically to
    every strided slice of the state vector supported on the block, which is
    exactly what a block-local operator does.
    """
    n = len(psi).bit_length() - 1
    width = hi - lo
    d = 1 << width
    if nref is None:
        nref = d
    refl = []
    for _ in range(nref):
        refl.append([complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
                     for _ in range(d)])
    phases = []
    for _ in range(d):
        theta = 2.0 * math.pi * rng.random()
        phases.append(complex(math.cos(theta), math.sin(theta)))
    stride = 1 << lo
    lo_range = 1 << lo
    hi_range = 1 << (n - hi)

    for ah in range(hi_range):
        high = ah << hi
        for al in range(lo_range):
            base = high + al
            cur = psi[base: base + d * stride: stride]
            for v in refl:
                w = 0j
                norm = 0.0
                for i in range(d):
                    vi = v[i]
                    w += vi.conjugate() * cur[i]
                    norm += vi.real * vi.real + vi.imag * vi.imag
                if norm == 0.0:
                    continue
                scale = 2.0 * w / norm
                for i in range(d):
                    cur[i] -= scale * v[i]
            for i in range(d):
                cur[i] *= phases[i]
            psi[base: base + d * stride: stride] = cur
    return psi


def random_pure_state(n, rng):
    psi = [complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
           for _ in range(1 << n)]
    norm = math.sqrt(sum(abs(a) ** 2 for a in psi))
    return [a / norm for a in psi]


# --------------------------------------------------------------------------
# Reduced density matrix
# --------------------------------------------------------------------------
def spread(value, mask, n):
    """Drop the bits of ``value`` onto the qubit positions selected by ``mask``."""
    out = 0
    bit = 0
    for q in range(n):
        if mask >> q & 1:
            out |= ((value >> bit) & 1) << q
            bit += 1
    return out


def reduced_rho(psi, n, keep_mask, nkeep):
    """Reduced density matrix of the ``nkeep`` qubits selected by ``keep_mask``."""
    dk = 1 << nkeep
    dt = 1 << (n - nkeep)
    trace_mask = ((1 << n) - 1) & ~keep_mask
    rho = [[0j] * dk for _ in range(dk)]
    keep_idx = [spread(ik, keep_mask, n) for ik in range(dk)]
    for t in range(dt):
        toff = spread(t, trace_mask, n)
        for ik in range(dk):
            i = keep_idx[ik] | toff
            pi = psi[i]
            row = rho[ik]
            for jk in range(dk):
                row[jk] += pi * psi[keep_idx[jk] | toff].conjugate()
    return rho


def subsystem_entropy(psi, n, keep):
    """von Neumann entropy (in nats) of the subsystem on qubits ``keep``.

    For a pure global state this equals the entropy of the complement, so the
    smaller of the two sides is diagonalised.
    """
    keep = sorted(keep)
    if not keep or len(keep) >= n:
        return 0.0
    if 2 * len(keep) > n:                       # use the complement instead
        mask = 0
        for q in range(n):
            if q not in keep:
                mask |= 1 << q
        return subsystem_entropy(psi, n, [q for q in range(n) if mask >> q & 1])
    keep_mask = 0
    for q in keep:
        keep_mask |= 1 << q
    rho = reduced_rho(psi, n, keep_mask, len(keep))
    return entropy_from_rho(rho)


def entropy_from_rho(rho):
    ent = 0.0
    for lam in hermitian_eigenvalues(rho):
        if lam > 1e-13:
            ent -= lam * math.log(lam)
    return ent


# --------------------------------------------------------------------------
# Eigenvalues of a complex Hermitian matrix
# --------------------------------------------------------------------------
def hermitian_eigenvalues(mat):
    """Eigenvalues of a Hermitian matrix (real, ascending).

    A Hermitian matrix H = A + iB with A symmetric and B antisymmetric acts on
    complex vectors (x + iy) exactly as the real symmetric matrix

        M = [[A, -B], [B, A]]

    acts on the real vector [x; y].  Hence the eigenvalues of H are the
    eigenvalues of M, each appearing twice.
    """
    d = len(mat)
    m = 2 * d
    a = [[0.0] * m for _ in range(m)]
    for i in range(d):
        ai = a[i]
        ab = a[d + i]
        for j in range(d):
            h = mat[i][j]
            ai[j] = h.real
            ai[d + j] = -h.imag
            ab[j] = h.imag
            ab[d + j] = h.real
    evals = sorted(jacobi_symmetric(a))
    # each eigenvalue of H appears twice in the spectrum of M, so after
    # sorting they form adjacent pairs: keep every second entry
    return evals[0::2]


def jacobi_symmetric(a, tol=1e-13, max_sweeps=200):
    """Eigenvalues of a real symmetric matrix, by cyclic Jacobi rotations."""
    d = len(a)
    for _ in range(max_sweeps):
        off = 0.0
        for p in range(d):
            for q in range(p + 1, d):
                off += a[p][q] * a[p][q]
        if off < tol * tol * d:
            break
        for p in range(d):
            for q in range(p + 1, d):
                apq = a[p][q]
                if apq == 0.0:
                    continue
                app = a[p][p]
                aqq = a[q][q]
                tau = (aqq - app) / (2.0 * apq)
                if tau >= 0.0:
                    t = 1.0 / (tau + math.sqrt(1.0 + tau * tau))
                else:
                    t = -1.0 / (-tau + math.sqrt(1.0 + tau * tau))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = t * c
                for k in range(d):
                    if k == p or k == q:
                        continue
                    akp = a[k][p]
                    akq = a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[p][k] = a[k][p]
                    a[k][q] = s * akp + c * akq
                    a[q][k] = a[k][q]
                a[p][p] = app - t * apq
                a[q][q] = aqq + t * apq
                a[p][q] = 0.0
                a[q][p] = 0.0
    return [a[i][i] for i in range(d)]

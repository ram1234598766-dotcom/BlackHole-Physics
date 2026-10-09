"""Assemble and write the Partitionism proceedings PDF.

    python3 -m paper.build_paper [--out paper/partitionism.pdf]
"""

import argparse
import os
import sys

from .pdflib import Doc
from . import content


def build(out_path):
    d = Doc(title="Partitionism: a framework for describing black holes as "
                   "wholes - proceedings",
            author="Partitionism research programme",
            subject="Black holes as wholes: theorems, proofs and numerical "
                    "verification")
    d._footer_left = ("Partitionism %s  |  every claim labelled: THEOREM / "
                      "ESTABLISHED / CONJECTURE / PREDICTION" % content.VERSION)

    # ---------------- title page ----------------
    d.spacer(60)
    d.para("**PARTITIONISM**", size=25, style='bold', align='center',
           leading=34, space_after=2)
    d.para("A framework for describing black holes as wholes", size=14,
           style='bodyi', align='center', leading=20, space_after=10)
    d.rule(weight=1.0, space=10)
    d.para("Proceedings of four papers", size=11, align='center', leading=16,
           space_after=2)
    d.para("**Paper I**   Partitionism: a black hole in one language\n"
           "**Paper II**  The evaporation ledger: theorems and numerical "
           "verification\n"
           "**Paper III** Readout degeneracy: the singularity as an artefact "
           "of the coarse map\n"
           "**Paper IV**  Quantised payout: the staircase, the Page-time "
           "shift, and where to look",
           size=10, align='center', leading=15, space_after=8)
    d.para("**Appendix A**  Claims register        "
           "**Appendix B**  Numerical methods and validation\n"
           "**Appendix C**  Reproducibility        "
           "**Appendix D**  References\n"
           "**Appendix E**  Notation and conventions",
           size=9, align='center', leading=14, space_after=16)
    d.rule(weight=0.6, space=10)
    d.para(f"Version {content.VERSION}      {content.DATE}      "
           "speculative research framework", size=9.5, align='center',
           leading=14, space_after=18)

    # epistemic notice
    d.para("**Epistemic notice.**  This volume contains four kinds of "
           "statement and they are labelled wherever they appear: **THEOREM** "
           "and **LEMMA** (proved in place, with the proof given), "
           "**ESTABLISHED** (standard physics, cited in Appendix D), "
           "**CONJECTURE** (part of Partitionism; not proved, and said so in "
           "the text), and **PREDICTION** or **FALSIFIER** (a commitment that "
           "can fail).  Nothing is presented as established physics unless it "
           "is.  Appendix A is a register of every substantive claim in the "
           "volume with its status and the means by which it is established - "
           "including, explicitly, the four claims that were withdrawn after "
           "a literature search found that they had already been published "
           "(items A18, A28, A29 and A14).  The framework is speculative.  "
           "What distinguishes it from speculation without content is that its "
           "central mechanism is now a theorem (Paper II) and a computed "
           "signature (Paper IV), and that it can be killed by experiment "
           "(falsifiers F1-F5).", size=9.5, leading=13.5)

    # ---------------- papers ----------------
    d.page_break()
    content.paper_i(d)
    d.page_break()
    content.paper_ii(d)
    d.page_break()
    content.paper_iii(d)
    d.page_break()
    content.paper_iv(d)
    content.appendix_a(d)
    content.appendix_b(d)
    content.appendix_c(d)
    content.appendix_d(d)
    content.appendix_e(d)

    n = d.save(out_path)
    return n


def main(argv=None):
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--out", default=os.path.join(here, "partitionism.pdf"))
    args = ap.parse_args(argv)
    n = build(args.out)
    size = os.path.getsize(args.out)
    print(f"wrote {args.out}: {n} pages, {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

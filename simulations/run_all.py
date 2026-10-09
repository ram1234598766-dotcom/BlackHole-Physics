"""Run the whole Partitionism test suite and write RESULTS.md.

    python3 -m simulations.run_all

Outputs:
    simulations/RESULTS.md   - a human-readable record of every test
"""

import datetime
import os

from . import test_ledger
from . import test_quantization
from . import test_readout
from . import validation


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parts = []
    parts.append("# Partitionism - simulation results\n")
    parts.append(f"Generated {datetime.date.today().isoformat()} by "
                 "`python3 -m simulations.run_all`.\n")
    parts.append("Pure Python, no dependencies.  All quantities are exact "
                 "within the stated tolerances; every random-unitary run "
                 "uses a fixed seed so the numbers are reproducible.\n")

    parts.append("## 0. Validation of the numerical machinery\n")
    parts.append("```")
    parts.append(validation.run_tests())
    parts.append("```\n")

    parts.append("## 1. The evaporation ledger\n")
    parts.append("```")
    parts.append(test_ledger.main())
    parts.append("```\n")

    parts.append("## 2. Quantised payout\n")
    parts.append("```")
    parts.append(test_quantization.run_tests())
    parts.append("```\n")

    parts.append("## 3. Readout degeneracy\n")
    parts.append("```")
    parts.append(test_readout.run_tests())
    parts.append("```\n")

    text = "\n".join(parts) + "\n"
    path = os.path.join(here, "RESULTS.md")
    with open(path, "w") as fh:
        fh.write(text)
    print(text)
    print(f"\nwritten to {path}")


if __name__ == "__main__":
    main()

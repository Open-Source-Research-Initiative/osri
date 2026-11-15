# SPDX-License-Identifier: MIT
"""Port the baseline calibration in the Carroll (1997) Econ-ARK reproduction."""
import argparse
import csv
import json

import numpy as np
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType
from common import output_directory, save_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    output = output_directory(args.output)
    parameters = dict(cycles=0, seed=args.seed, AgentCount=1000, T_sim=120,
                      CRRA=2.0, DiscFac=0.96, Rfree=[1.0], LivPrb=[1.0],
                      PermGroFac=[1.02], PermShkStd=[0.1], TranShkStd=[0.1],
                      UnempPrb=0.005, IncUnemp=0.0, BoroCnstArt=None,
                      CubicBool=True, T_cycle=1,
                      aXtraMin=0.001, aXtraMax=20, aXtraCount=48)
    (output / "parameters.json").write_text(json.dumps(parameters, indent=2) + "\n")
    consumer = IndShockConsumerType(**parameters)
    consumer.solve()
    consumer.track_vars = ["mNrm", "cNrm", "aNrm"]
    consumer.initialize_sim()
    consumer.simulate()
    history = consumer.history
    m, c, a = (np.asarray(history[name]) for name in ["mNrm", "cNrm", "aNrm"])
    with (output / "households.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["period", "mean_market_resources_normalized", "mean_consumption_normalized", "mean_assets_normalized"])
        writer.writerows(zip(range(parameters["T_sim"]), m.mean(axis=1), c.mean(axis=1), a.mean(axis=1)))
    save_record(output, "household-saving", ["econ-ark", "numpy", "numba"], parameters,
                {"last_mean_resources": float(m[-1].mean()), "last_mean_consumption": float(c[-1].mean()),
                 "last_mean_assets": float(a[-1].mean()), "normalization": "permanent income"},
                {"finite_history": bool(np.isfinite([m, c, a]).all()),
                 "positive_consumption": bool((c > 0).all()),
                 "borrowing_constraint": bool((a >= -1e-10).all()),
                 "budget_identity": bool(np.allclose(m, c + a, rtol=1e-9, atol=1e-10))},
                ["https://doi.org/10.1162/003355397555109",
                 "https://github.com/econ-ark/BufferStock-LifeCycle/blob/0a278360b77eeac1df1e91374c168b3091365fbf/Code/Python/BufferStock-LifeCycle.py"])


if __name__ == "__main__":
    main()

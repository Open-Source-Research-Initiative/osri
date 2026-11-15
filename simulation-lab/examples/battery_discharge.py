# SPDX-License-Identifier: MIT
"""Adapt PyBaMM's published Listing 1; write voltage in V against time in s."""
import argparse
import csv
import os

os.environ.setdefault("PYBAMM_DISABLE_TELEMETRY", "true")

import numpy as np
import pybamm
from common import output_directory, save_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = output_directory(args.output)
    parameters = pybamm.ParameterValues("Marquis2019")
    parameters["Current function [A]"] = parameters["Nominal cell capacity [A.h]"]
    parameters.to_json(str(output / "parameters.json"))
    model = pybamm.lithium_ion.DFN()
    solver = pybamm.IDAKLUSolver(rtol=1e-6, atol=1e-8)
    sim = pybamm.Simulation(model, parameter_values=parameters, solver=solver)
    solution = sim.solve([0, 3600])
    times = np.linspace(0, float(solution.t[-1]), 121)
    volts = solution["Terminal voltage [V]"](times)
    with (output / "voltage.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_s", "voltage_V"])
        writer.writerows(zip(times, volts))
    save_record(output, "battery-discharge", ["pybamm", "pybammsolvers", "numpy"],
                {"parameter_set": "Marquis2019", "rate_C": 1, "horizon_s": 3600,
                 "rtol": 1e-6, "atol": 1e-8, "model": "DFN", "mesh": "PyBaMM version defaults"},
                {"termination": str(solution.termination), "end_time_s": float(times[-1]),
                 "initial_voltage_V": float(volts[0]), "final_voltage_V": float(volts[-1])},
                {"finite_voltage": bool(np.isfinite(volts).all()),
                 "time_increases": bool(np.all(np.diff(times) > 0)),
                 "within_requested_horizon": bool(0 < times[-1] <= 3600),
                 "positive_voltage": bool(np.all(volts > 0))},
                ["https://doi.org/10.5334/jors.309"])


if __name__ == "__main__":
    main()

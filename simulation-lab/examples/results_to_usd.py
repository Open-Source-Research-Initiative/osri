# SPDX-License-Identifier: MIT
"""Package a battery run as a USD data prim without inventing physical geometry."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil

from pxr import Sdf, Usd, UsdGeom
from common import output_directory, save_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="battery-discharge output directory")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = args.input / "voltage.csv"
    record = json.loads((args.input / "run.json").read_text())
    expected = record["files_sha256"]["voltage.csv"]
    if record["example"] != "battery-discharge":
        parser.error("input does not match the battery run record")
    for name in ["voltage.csv", "parameters.json"]:
        if hashlib.sha256((args.input / name).read_bytes()).hexdigest() != record["files_sha256"].get(name):
            parser.error(f"{name} does not match the battery run record")
    if not record["checks"] or not all(record["checks"].values()):
        parser.error("input battery run contains failed checks")
    with source.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    times = [float(row["time_s"]) for row in rows]
    volts = [float(row["voltage_V"]) for row in rows]
    if not times or not all(math.isfinite(x) for x in times + volts) or not all(b > a for a, b in zip(times, times[1:])):
        parser.error("invalid voltage time series")
    output = output_directory(args.output)
    for name in ["voltage.csv", "parameters.json", "run.json"]:
        shutil.copy2(args.input / name, output / ("source-" + name))
    stage = Usd.Stage.CreateNew(str(output / "battery.usda"))
    root = UsdGeom.Xform.Define(stage, "/BatteryRun").GetPrim()
    stage.SetDefaultPrim(root)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    stage.SetTimeCodesPerSecond(1)
    stage.SetStartTimeCode(times[0])
    stage.SetEndTimeCode(times[-1])
    root.CreateAttribute("research:source", Sdf.ValueTypeNames.Asset).Set(Sdf.AssetPath("./source-voltage.csv"))
    root.CreateAttribute("research:parameters", Sdf.ValueTypeNames.Asset).Set(Sdf.AssetPath("./source-parameters.json"))
    root.CreateAttribute("research:runRecord", Sdf.ValueTypeNames.Asset).Set(Sdf.AssetPath("./source-run.json"))
    root.CreateAttribute("research:sourceSHA256", Sdf.ValueTypeNames.String).Set(expected)
    root.CreateAttribute("research:voltageUnit", Sdf.ValueTypeNames.String).Set("V")
    root.CreateAttribute("research:timeUnit", Sdf.ValueTypeNames.String).Set("s")
    root.CreateAttribute("research:interpretation", Sdf.ValueTypeNames.String).Set("Terminal voltage data; no cell geometry or physical USD model")
    voltage = root.CreateAttribute("research:terminalVoltage", Sdf.ValueTypeNames.Double)
    for time, value in zip(times, volts):
        voltage.Set(value, Usd.TimeCode(time))
    stage.GetRootLayer().Save()
    restored = Usd.Stage.Open(str(output / "battery.usda"))
    attr = restored.GetPrimAtPath("/BatteryRun").GetAttribute("research:terminalVoltage")
    save_record(output, "results-to-usd", ["usd-core"], {"time_codes_per_second": 1, "meters_per_unit": 1},
                {"samples": len(times), "source_sha256": expected},
                {"same_sample_times": attr.GetTimeSamples() == times,
                 "same_sample_values": all(attr.Get(t) == v for t, v in zip(times, volts)),
                 "time_unit_preserved": restored.GetTimeCodesPerSecond() == 1 and restored.GetPrimAtPath("/BatteryRun").GetAttribute("research:timeUnit").Get() == "s",
                 "packaged_source_matches": hashlib.sha256((output / "source-voltage.csv").read_bytes()).hexdigest() == expected},
                ["https://openusd.org/release/api/class_usd_attribute.html",
                 "https://doi.org/10.5334/jors.309"])


if __name__ == "__main__":
    main()

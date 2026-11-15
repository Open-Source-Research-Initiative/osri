# SPDX-License-Identifier: MIT
"""Compare simulated European call payoffs with Black-Scholes under the same model."""
import argparse
import csv
import math
import statistics

import QuantLib as ql
from common import output_directory, save_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--paths", type=int, default=50000)
    args = parser.parse_args()
    if args.paths < 2:
        parser.error("--paths must be at least 2")
    if not 1 <= args.seed <= 2**32 - 1:
        parser.error("--seed must be between 1 and 4294967295; zero does not select a fixed QuantLib seed")
    output = output_directory(args.output)
    spot, strike, rate, volatility, maturity = 100.0, 100.0, 0.05, 0.2, 1.0
    day_count = ql.Actual365Fixed()
    today = ql.Date(1, 1, 2025)
    ql.Settings.instance().evaluationDate = today
    risk_free = ql.YieldTermStructureHandle(ql.FlatForward(today, rate, day_count))
    vol = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), volatility, day_count))
    process = ql.BlackScholesProcess(ql.QuoteHandle(ql.SimpleQuote(spot)), risk_free, vol)
    option = ql.VanillaOption(ql.PlainVanillaPayoff(ql.Option.Call, strike),
                             ql.EuropeanExercise(today + 365))
    option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
    analytic = option.NPV()
    # One exact GBM transition is sufficient for a terminal-only payoff.
    sequence = ql.GaussianRandomSequenceGenerator(
        ql.UniformRandomSequenceGenerator(1, ql.UniformRandomGenerator(args.seed)))
    generator = ql.GaussianPathGenerator(process, maturity, 1, sequence, False)
    payoffs = []
    with (output / "payoffs.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["path", "terminal_price_currency", "discounted_payoff_currency"])
        for i in range(args.paths):
            terminal = generator.next().value().back()
            payoff = math.exp(-rate * maturity) * max(terminal - strike, 0.0)
            payoffs.append(payoff)
            writer.writerow([i, terminal, payoff])
    mean = statistics.mean(payoffs)
    standard_error = statistics.stdev(payoffs) / math.sqrt(args.paths)
    # Independent closed-form expression checks the package's analytic engine.
    normal = statistics.NormalDist()
    d1 = (math.log(spot / strike) + (rate + volatility**2 / 2) * maturity) / (volatility * math.sqrt(maturity))
    d2 = d1 - volatility * math.sqrt(maturity)
    formula = spot * normal.cdf(d1) - strike * math.exp(-rate * maturity) * normal.cdf(d2)
    save_record(output, "option-monte-carlo", ["QuantLib"],
                {"spot": spot, "strike": strike, "rate_per_year": rate,
                 "volatility_per_sqrt_year": volatility, "maturity_years": maturity,
                 "dividend_yield": 0, "paths": args.paths, "seed": args.seed},
                {"analytic_price": analytic, "independent_formula_price": formula,
                 "mc_price": mean, "standard_error": standard_error,
                 "ci95": [mean - 1.96 * standard_error, mean + 1.96 * standard_error],
                 "z_score": (mean - analytic) / standard_error if standard_error > 0 else None},
                {"analytic_matches_formula": abs(analytic - formula) < 1e-10,
                 "finite_nonnegative_payoffs": all(math.isfinite(p) and p >= 0 for p in payoffs),
                 "nonzero_sample_variance": standard_error > 0,
                 "mc_within_five_standard_errors": abs(mean - analytic) <= 5 * standard_error},
                ["https://doi.org/10.1086/260062"])


if __name__ == "__main__":
    main()

#!/bin/sh
set -eu
git clone https://github.com/rickecon/TaxFuncIntegr.git source
git -C source checkout --detach 715cc76e3305c00dd64d79521c504bb388c6d87d
git clone --depth 1 --branch 0.19.0 https://github.com/PSLmodels/Tax-Calculator.git taxcalc-source
# Expected Tax-Calculator commit: 8b845d1ae65115c1544603418c39252957931457

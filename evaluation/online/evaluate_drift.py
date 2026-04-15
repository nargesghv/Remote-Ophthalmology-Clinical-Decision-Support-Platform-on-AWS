from __future__ import annotations

import numpy as np


def population_stability_index(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    breakpoints = np.linspace(0, 100, bins + 1)
    expected_perc = np.percentile(expected, breakpoints)
    psi = 0.0

    for i in range(bins):
        exp_bin = ((expected >= expected_perc[i]) & (expected < expected_perc[i + 1])).mean()
        act_bin = ((actual >= expected_perc[i]) & (actual < expected_perc[i + 1])).mean()
        exp_bin = max(exp_bin, 1e-6)
        act_bin = max(act_bin, 1e-6)
        psi += (act_bin - exp_bin) * np.log(act_bin / exp_bin)
    return float(psi)

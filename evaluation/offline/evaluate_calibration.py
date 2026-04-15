from __future__ import annotations

import numpy as np


def expected_calibration_error(confidences, predictions, labels, n_bins=10):
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    confidences = np.asarray(confidences)
    predictions = np.asarray(predictions)
    labels = np.asarray(labels)

    for i in range(n_bins):
        mask = (confidences > bins[i]) & (confidences <= bins[i + 1])
        if np.any(mask):
            acc = np.mean(predictions[mask] == labels[mask])
            conf = np.mean(confidences[mask])
            ece += abs(acc - conf) * np.mean(mask)
    return float(ece)


def main():
    confidences = [0.9, 0.8, 0.7, 0.4]
    predictions = [1, 1, 0, 0]
    labels = [1, 1, 1, 0]
    print({"ece": expected_calibration_error(confidences, predictions, labels)})


if __name__ == "__main__":
    main()

import os.path as osp

import numpy as np

from jenks_natural_breaks import classify


def test_main():
    data = np.load(osp.join(osp.dirname(__file__), "test_data.npy"))
    expected = [
        0.0005421961588045754,
        0.20570633478192457,
        0.4197343611487738,
        0.6230659944190866,
        0.8134908717021093,
        0.9995623760709071
    ]

    result = classify(data, 5)

    def fp_compare(v1, v2):
        return v1 - v2 < 10e-6

    assert all(fp_compare(r, e) for r, e in zip(result, expected))

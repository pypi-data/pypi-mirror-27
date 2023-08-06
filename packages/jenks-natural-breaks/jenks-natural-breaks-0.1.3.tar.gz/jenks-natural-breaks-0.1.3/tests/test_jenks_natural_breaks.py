import os.path as osp

import numpy as np

from jenks_natural_breaks import classify


def test_main():
    data = np.load(osp.join(osp.dirname(__file__), "test_data.npy"))
    expected = [
        0.00054219615880457539, 
        0.207831589876042, 
        0.42214371025157071, 
        0.62704148582439201, 
        0.81435907344112834, 
        0.99956237607090714]

    result = classify(data, 5)

    def fp_approx_equal(v1, v2):
        return abs(v1 - v2) < 10e-6

    assert all(fp_approx_equal(r, e) for r, e in zip(result, expected)), (
        "result ({}) != expected ({})".format(result, expected))

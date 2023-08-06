__version__ = '0.1.2'

import numpy as np

from ._jenks_matrices import ffi as _ffi
from ._jenks_matrices import lib as _lib


def _jenks_matrices(data, n_classes):
    lower_class_limits = np.zeros((len(data) + 1, n_classes + 1), dtype=np.uint32)
    variance_combinations = np.zeros((len(data) + 1, n_classes + 1), dtype=np.float64)

    lower_class_limits[1, :] = 1
    variance_combinations[2:, :] = float("Inf")

    _lib.jenks_matrices(
        len(data), n_classes,
        _ffi.cast("double *", data.ctypes.data),
        _ffi.cast("int *", lower_class_limits.ctypes.data),
        _ffi.cast("double *", variance_combinations.ctypes.data))

    return lower_class_limits, variance_combinations


def _jenks_breaks(data, lower_class_limits, n_classes):
    k = len(data) - 1
    class_breaks = [data[-1]] * (n_classes + 1)
    class_breaks[0] = data[0]

    for i in range(n_classes, 1, -1):
        idx = lower_class_limits[k, i] - 2
        class_breaks[i - 1] = data[idx]
        k = lower_class_limits[k, i] - 1

    return class_breaks


def classify(data, n_classes):
    assert len(data.shape) == 1 and n_classes < data.shape[0]
    data = np.copy(data)
    data.sort()
    lower_class_limits, _ = _jenks_matrices(data, n_classes)
    return _jenks_breaks(data, lower_class_limits, n_classes)

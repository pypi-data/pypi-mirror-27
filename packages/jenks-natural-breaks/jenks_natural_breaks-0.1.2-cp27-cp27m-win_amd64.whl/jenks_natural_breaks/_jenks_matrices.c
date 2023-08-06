#ifndef _MSC_VER // [
#   include <inttypes.h>
#elif (_MSC_VER < 1300)
    typedef unsigned int      uint32_t;
#else
    typedef unsigned __int32  uint32_t;
#endif // _MSC_VER ]

#define idx(row_len, i, j) ((row_len) * (i) + (j))

void jenks_matrices(
    const int data_len, const int n_classes, double *data,
    uint32_t *lower_class_limits,
    double *variance_combinations) {

    const int row_len = n_classes + 1;
    
    int l, m, j;
    for (l = 2; l < data_len + 1; l++) {
        double sum = 0,
            sum_squares = 0,
            variance = 0;

        for (m = 1; m < l + 1; m++) {

            int lower_class_limit = l - m + 1;
            double val = data[lower_class_limit - 1];

            sum += val;
            sum_squares += val * val;

            variance = sum_squares - (sum * sum) / m;

            if (lower_class_limit != 1) {
                for (j = 2; j < n_classes + 1; j++) {
                    const double test_variance = variance
                        + variance_combinations[idx(row_len, lower_class_limit - 1, j - 1)];
                    if (variance_combinations[idx(row_len, l, j)] >= test_variance) {
                        lower_class_limits[idx(row_len, l, j)] = lower_class_limit;
                        variance_combinations[idx(row_len, l, j)] = test_variance;
                    }
                }
            }
        }

        lower_class_limits[idx(row_len, l, 1)] = 1;
        variance_combinations[idx(row_len, l, 1)] = variance;
    }
}

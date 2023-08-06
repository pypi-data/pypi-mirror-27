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

            // increase the current sum and sum-of-squares
            sum += val;
            sum_squares += val * val;

            // the variance at this point in the sequence is the difference
            // between the sum of squares and the total x 2, over the number
            // of samples.
            variance = sum_squares - (sum * sum) / m;

            if (lower_class_limit != 1) {
                for (j = 2; j < n_classes + 1; j++) {
                    // if adding this element to an existing class
                    // will increase its variance beyond the limit, break
                    // the class at this point, setting the `lower_class_limit`
                    // at this point.
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

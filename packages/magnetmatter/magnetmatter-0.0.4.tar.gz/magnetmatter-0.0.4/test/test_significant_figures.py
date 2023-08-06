import sys
"""adding path to look for modules"""
sys.path.append(r"C:\AU-PHD\General_Data\_Python\modules")
from prf_plot_tools import round2significant_error


def test_equal_zero():
    values = [0.0, 0.00000, 0, -0.0, -0, +0]
    errors = values
    answers = [a for a in "0(0) 0(0) 0(0) 0(0) 0(0) 0(0)".split()]
    for i, answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

def test_equal_nan():
    import numpy as np
    values = [np.nan, +np.nan]
    errors = values
    answers = [a for a in "NaN NaN".split()]
    for i, answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

def test_value_nan():
    import numpy as np
    values = [np.nan, +np.nan]
    errors = [0.003, 12.04]
    answers = [a for a in "NaN NaN".split()]
    for i, answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

def test_error_nan():
    import numpy as np
    values = [345.324, 0.00432]
    errors = [np.nan, +np.nan]
    answers = [a for a in "NaN NaN".split()]
    for i, answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

def string2float(string):
    return [float(a) for a in string.split()]

big     =  string2float("2072.74693769    8153.57782491     -1455.27113026     9998.63173947     1296.19060769")
small   = string2float("  -0.38897303      -0.86366239         0.33228131        0.9999999999     -0.999999999")
small2  = string2float("  -0.18897303      -0.96366239         0.13228131        0.9999999999     -0.399999999")
smaller = string2float("   0.00443839       0.00012597         0.00171697        0.00908751        0.00974499")
tiny    = string2float("   7.85794635e-06  -3.64176573e-07     5.25855874e-06    8.92513106e-07   -9.80637317e-06")

small   = string2float("  -0.38897303      -0.86366239         0.33228131        0.9999999999     -0.999999999")
small2  = string2float("  -0.18897303      -0.96366239         0.13228131        0.9999999999     -0.399999999")
def test_equal_small(values = small, errors = small2):
    answers = "  -0.4(2)      -1(1)         0.3(1)        1(1)     -1.0(4)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

small   = string2float("  -0.38897303      -0.86366239         0.33228131        0.9999999999     -0.999999999")
smaller = string2float("   0.00443839       0.00012597         0.00171697        0.00908751        0.00974499")
def test_small_value_vs_smaller_error(values = small, errors = smaller):
    answers = "-0.389(4)      -0.8637(1)             0.332(2)        1.000(9)     -1.00(1)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

small   = string2float("  -0.38897303      -0.86366239         0.33228131        0.9999999999     -0.999999999")
tiny    = string2float("   7.85794635e-06  -3.64176573e-07     5.25855874e-06    8.92513106e-07   -9.80637317e-06")
def test_small_value_vs_tiny_error(values = small, errors = tiny):
    answers = "-0.388973(8)      -0.8636624(4)         0.332281(5)        1.0000000(9)     -1.00000(1)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

big     =  string2float("2072.74693769    8153.57782491     -1455.27113026     9998.63173947     1296.19060769")
smaller = string2float("   0.00443839       0.00012597         0.00171697        0.00908751        0.00974499")
def test_big_value_vs_smaller_error(values = big, errors = smaller):
    answers = "2072.747(4)    8153.5778(1)     -1455.271(2)     9998.632(9)     1296.19(1)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

smaller = string2float("   0.00443839       0.00012597         0.00171697        0.00908751        0.00974499")
def test_equal_smaller(values = smaller, errors = smaller):
    answers = "0.004(4)       0.0001(1)         0.002(2)        0.009(9)        0.01(1)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

tiny    = string2float("   7.85794635e-06  -3.64176573e-07     5.25855874e-06    8.92513106e-07   -9.80637317e-06")
def test_equal_tiny(values = tiny, errors = tiny):
    answers = "0.000008(8)  -0.0000004(4)   0.000005(5)    0.0000009(9)   -0.00001(1)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

big     =  string2float("2072.74693769    8153.57782491     -1455.27113026     9998.63173947     1296.19060769")
def test_equal_big(values = big, errors = big):
    answers = "2(2)e+03    8(8)e+03     -1(1)e+03     1(1)e+04     1(1)e+03".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

big     =  string2float("2072.74693769    8153.57782491     -1455.27113026     9998.63173947     1296.19060769")
big2     =  string2float("207.74693769    18153.57782491     -145.27113026     -19998.63173947     16.19060769")
def test_equal_big(values = big, errors = big2):
    answers = "21(2)e+02    1(2)e+04     -15(1)e+02     1(2)e+04     130(2)e+01".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

real_values = string2float("-0.04782128 0.23840357")
real_errors = string2float("20.025845908 0.0")
def test_real_cases_no_constrain(values = real_values, errors = real_errors):
    answers = "-0(2)e+01 0.23840357(0)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i]) == answer

real_values = string2float("-0.04782128 0.23840357")
real_errors = string2float("20.025845908 0.0")
constrain = 11
def test_real_cases_11_constrain(values = real_values, errors = real_errors, length = constrain):
    answers = "-0(2)e+01 0.238404(0)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i],length) == answer

real_values = string2float("-0.04782128 0.23840357")
real_errors = string2float("20.025845908 0.0")
constrain = 13
def test_real_cases_11_constrain(values = real_values, errors = real_errors, length = constrain):
    answers = "-0(2)e+01 0.23840357(0)".split()
    for i,answer in enumerate(answers):
        assert round2significant_error(values[i],errors[i],length) == answer









#finish

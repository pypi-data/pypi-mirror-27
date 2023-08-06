import sys
"""adding path to look for modules"""
sys.path.append(r"C:\AU-PHD\General_Data\_Python\modules")
from prf_plot_tools import find_significant_figure

def test_int():
    values = [str(a) for a in range(0,20,3)] # [0, 3, 6, 9, 12, 15, 18]
    answers = [int(i) for i in "0 0 0 0 -1 -1 -1".split()]
    for value, answer in zip(values,answers):
        assert find_significant_figure(value) == answer

def test_float_above_unity():
    values = "11.1100 111.11100 1111.111100 1.0100 100.00100 1000.000100".split()
    answers = [int(a) for a in "-1 -2 -3 0 -2 -3".split()]
    for value, answer in zip(values,answers):
        assert find_significant_figure(value) == answer

def test_float_below_unity():
    values = "0.1100 0.11100 0.111100 0.0100 0.00100 0.000100".split()
    answers = [int(a) for a in "1 1 1 2 3 4".split()]
    for value, answer in zip(values,answers):
        assert find_significant_figure(value) == answer

def test_negative_mixed_floats():
    values = "-100.099 -0.11100 -0.101100 -1.0100 -0.00100 -30.000100".split()
    answers = [int(a) for a in "-2 1 1 0 3 -1".split()]
    for value, answer in zip(values,answers):
        assert find_significant_figure(value) == answer

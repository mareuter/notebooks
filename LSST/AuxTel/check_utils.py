__all__ = ["check_float", "check"]

import numpy as np


def check(values, truth, keyword):
    value = values[keyword]
    if truth == value:
        print(f"{keyword} OK")
    else:
        print(f"Problem with {keyword}: {truth} != {value}")

        
def check_float(values, truth, keyword, precision=1e-8):
    value = values[keyword]
    try:
        diff = np.fabs(truth - value)
        if diff < precision:
            print(f"{keyword} OK")
        else:
            print(f"Problem with {keyword}: {truth} != {value}")
    except TypeError:
        print(f"Problem with {keyword}: {truth} != {value}")

        
def check_near(values, keyword1, keyword2, precision=1.0):
    value1 = values[keyword1]
    value2 = values[keyword2]
    diff = np.fabs(value1 - value2)
    if diff < precision:
        print(f"{keyword1} near {keyword2}")
    else:
        print(f"{keyword1} NOT near {keyword2}: {value1}, {value2}")
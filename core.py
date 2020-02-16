import numpy
import matplotlib
import math
import pandas

def displayData(data):
    result = 0
    for p in data:
        result += p.id
    return result
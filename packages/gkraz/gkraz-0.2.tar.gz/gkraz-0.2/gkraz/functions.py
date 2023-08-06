import numpy as np
import matplotlib.pyplot as plt
from terminaltables import SingleTable

def g_plot(x,y):
    plt.plot(x,y)
    plt.show()

def g_table(*cols):
    lines = list(zip(*cols))
    tbl = SingleTable(lines)
    tbl.inner_heading_row_border = False;
    return tbl.table

CONSTS = {
    "pi": np.pi,
    "e": np.e,
    "i": 1j
}

FUNCS = {
    "sqrt": np.sqrt,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "arcsin": np.arcsin,
    "arccos": np.arccos,
    "arctan": np.arctan,
    "atan2": np.arctan2,
    "arctan2": np.arctan2,
    "exp": np.exp,
    "ln": np.log,
    "log": np.log,
    "log2": np.log2,
    "log10": np.log10,
    "logb": lambda x,b: np.log(x)/np.log(b),
    "sinh": np.sinh,
    "cosh": np.cosh,
    "tanh": np.tanh,
    "asinh": np.arcsinh,
    "acosh": np.arccosh,
    "atanh": np.arctanh,
    "arcsinh": np.arcsinh,
    "arccosh": np.arccosh,
    "arctanh": np.arctanh,
    "if": np.where,
    "step": lambda x: np.heaviside(x,0),
    "rect": lambda x: np.heaviside(0.5+x,0)*np.heaviside(0.5-x,0),

    "arg": np.angle,
    "real": np.real,
    "imag": np.imag,
    "re": np.real,
    "im": np.imag,
    "conj": np.conj,

    "range": np.arange,
    "linspace": np.linspace,

    "plot": g_plot,
    "table": g_table,

    "magn": lambda x: x.magnitude,
    "dim": lambda x: x.dimensionality,
    "unit": lambda x: x.units
}
def get_builtin_names():
    return list(FUNCS.keys()) + list(CONSTS.keys())

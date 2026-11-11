import numpy as np


def curva_s(n_dias):
    x = np.linspace(0, 1, n_dias + 1)

    acum = 1 / (1 + np.exp(-10 * (x - 0.5)))

    acum = (acum - acum[0]) / (acum[-1] - acum[0])

    return np.diff(acum)
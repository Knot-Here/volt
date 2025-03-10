import numpy as np


def relative_volatility(sigmaA, sigmaB, rhoAB):
    """
    V_rel = sqrt( sigmaA^2 + sigmaB^2 - 2 * rhoAB * sigmaA * sigmaB )
    """
    return np.sqrt(sigmaA**2 + sigmaB**2 - 2 * rhoAB * sigmaA * sigmaB)

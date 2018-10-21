from scipy import stats
import numpy as np

class Smart_gas_lm:

    def __init__(self):
        pass

    def _get_slope_and_intercept(self):
        x = np.random.random(10)
        y = np.random.random(10)
        return stats.linregress(x,y)

if __name__ == 'main':
    smart_gas_lm = Smart_gas_lm()

from scipy import stats
import numpy as np
from random import randint
import matplotlib.pyplot as plt

class Smart_gas_lm:

    def __init__(self):
        self.train_dataset = None

    def _get_dummy_data(self):
        return [(randint(0,9), randint(0,9)) for i in range(10)]

    def _get_linregress(self):
        x = [i[0] for i in self.train_dataset]
        y = [i[1] for i in self.train_dataset]
        # plt.plot(x, y, 'ro')
        # plt.show()
        return stats.linregress(x, y)

    def set_train_dataset(self, data):
        self.train_dataset = data

    def get_estiamte_value(self, x):
        linregress = self._get_linregress()
        slope = linregress[0]
        intercept = linregress[1]
        return slope * x + intercept

if __name__ == '__main__':
    lm = Smart_gas_lm()
    lm.set_train_dataset(lm._get_dummy_data())
    print(lm.get_estiamte_value(10))

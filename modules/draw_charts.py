import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from modules.query_database import QueryDatabase


class Draw:

    @classmethod
    def draw_k_data_period(self, data, index):
        plot_k_data = pd.Series(data, index)
        plot_k_data.plot(kind='line')
        plt.show()


if __name__ == '__main__':
    series, index = pd.Series(QueryDatabase.get_k_value_period("000001", "2018-01-22", "2018-01-25"))
    Draw.draw_k_data_period(series, index)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from modules.query_database import QueryDatabase


class Draw:

    @classmethod
    def draw_k_data_period(self, from_date, to_date, data, index):
        plt.figure(figsize=(14, 7))
        plt.title(from_date + ' to ' + to_date)
        plt.plot(index, data, ls='--', marker='o')
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.xticks(index)
        # plot_k_data = pd.Series(data, index)
        # plot_k_data.plot(kind='line')
        for a, b in zip(index, data):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
        plt.show()


if __name__ == '__main__':
    series, index = pd.Series(QueryDatabase.get_k_value_period("000001", "2018-07-02", "2018-07-31"))
    Draw.draw_k_data_period("2018-07-02", "2018-07-31", series, index)

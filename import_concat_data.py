import pandas as pd
import os
import glob
from get_data_from_cninfo import DownloadMultiStocks
from HelloWorld import Hello


class ImportConcat:
    def __init__(self):
        self.data_path = '.\data'

    def import_concat_stock_data(self, stock_id, sheet, from_year, to_year):
        fzb = dict().fromkeys((year for year in range(from_year, to_year+1, 1)), [])
        print(fzb[year] for year in range(from_year, to_year+1, 1))
        for y in fzb.keys():
            file = glob.glob(os.path.join(self.data_path, str(stock_id).zfill(6), '*%s*%d.csv' % (sheet, y)))
            fzb[y] = pd.DataFrame(pd.read_csv(file[0], encoding='gbk'))
        result = pd.concat(fzb)
        result.to_csv(os.path.join(self.data_path, str(stock_id).zfill(6),'./%s_%d_%d.csv' % (sheet, from_year, to_year)))
        print('# %s sheet concatenated and saved. ' % sheet)
        # print(result)

    @staticmethod
    def import_concat_by_list(path_stock_list):
        stocks = DownloadMultiStocks()
        list_stock = stocks.get_stock_list(path_stock_list)
        for s in iter(list_stock):
            concat_result.import_concat_stock_data(str(s).zfill(6), 'fzb')


if __name__ == "__main__":
    concat_result = ImportConcat()
    # concat_result.import_concat_stock_data("000001", 'fzb', 2015, 2016)
    # concat_result.import_concat_stock_data("000001", 'llb', 2015, 2016)
    # concat_result.import_concat_stock_data("000001", 'lrb', 2015, 2016)
    multi_stocks = DownloadMultiStocks()
    stock_list = multi_stocks.get_stock_list('./data/stock_basics/20170601.csv')

    print(stock_list)

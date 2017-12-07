'''
Description: For cninfo, to concat the result within data range by specific fund or list of fund.
'''

import pandas as pd
import os
import glob
from modules.get_data_from_cninfo import DownloadMultiStocks


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
        print('# %s %s sheet concatenated and saved. ' % (stock_id, sheet))

    @staticmethod
    def import_concat_by_list(path_stock_list, sheet, from_year, to_year):
        stocks = DownloadMultiStocks()
        list_stock = stocks.get_stock_list(path_stock_list)
        for s in iter(list_stock):
            concat_result.import_concat_stock_data(str(s).zfill(6), sheet, from_year, to_year)


if __name__ == "__main__":
    concat_result = ImportConcat()
    # concat_result.import_concat_by_list('./data/sse50/2017_2_Filtered.csv', 'fzb', 2015, 2016)
    # concat_result.import_concat_by_list('./data/sse50/2017_2_Filtered.csv', 'llb', 2015, 2016)
    # concat_result.import_concat_by_list('./data/sse50/2017_2_Filtered.csv', 'lrb', 2015, 2016)
    concat_result.import_concat_stock_data('000338','fzb',2014,2016)
    concat_result.import_concat_stock_data('000338','llb',2014,2016)
    concat_result.import_concat_stock_data('000338','lrb',2014,2016)

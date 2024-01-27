import pandas as pd
import zipfile


STOCK_QUOTATIONS_ARCHIVE_FILE_NAME = 'mstall.zip'
STOCK_NAMES_FILE_NAME = 'WIG20.txt'

with open(STOCK_NAMES_FILE_NAME) as f:
    _stock_names = list(map(lambda line: line.strip(), f))


def load_stock_quotations(stock_names=_stock_names, filename=STOCK_QUOTATIONS_ARCHIVE_FILE_NAME):
    s = {}
    with zipfile.ZipFile(filename) as z:
        for stock_name in stock_names:
            with z.open(stock_name + '.mst') as f:
                s[stock_name] = pd.read_csv(f, index_col='<DTYYYYMMDD>', parse_dates=True)[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
                s[stock_name].index.rename('time', inplace=True)
                s[stock_name].rename(columns={'<OPEN>':'open', '<HIGH>':'high', '<LOW>':'low', '<CLOSE>':'close', '<VOL>':'volume'}, inplace=True)
    result = pd.concat(s.values(), keys=s.keys(), axis=1)
    result.fillna(method='ffill', inplace=True)
    return result

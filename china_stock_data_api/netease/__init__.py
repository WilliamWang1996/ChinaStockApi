""" Read stock data from 163
"""
from six import iteritems
from six import string_types
from six import StringIO
from pandas import DataFrame
from china_stock_data_api.cn_stock_util import DAILY_K_LINE_COLUMNS, \
    NETEASE_STOCK_INFO_COLUMNS
from china_stock_data_api.cn_stock_base import CnStockBase
import json
import int_date
import re
import numpy as np
import pandas as pd

__author__ = 'WangHao'
__all__ = ["latest"]

def latest(*indices):
    return NeteaseStock.latest(indices)


class NeteaseStock(CnStockBase):
    _BASE = "http://quotes.money.163.com/service/chddata.html?code={}&\
    start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"

    @classmethod
    def _get_base(cls):
        return cls._BASE

    @classmethod
    def _parse_daily_data(cls,body,index):
        df = pd.read_csv(StringIO(body))
        df.columns=DAILY_K_LINE_COLUMNS
        df=df.drop(columns=['股票代码','名称'])
        df['日期'] = df.日期.apply(int_date.to_int_date)
        df.set_index('日期', inplace=True)
        df.columns.name = index
        return df


    @classmethod
    def _process_index(cls, index):
        return cls._trans_index(index)

    @classmethod
    def _trans_index(cls, index):
        ret = index
        if index.startswith('sh'):
            ret = index.replace('sh', '0')
        elif index.startswith('sz'):
            ret = index.replace('sz', '1')
        return ret


class NeteaseStockInfo(CnStockBase):
    """get stock info from netease html

    sample url looks like this:
    report data
    `http://quotes.money.163.com/f10/zycwzb_600010,report.html`

    season data
    `http://quotes.money.163.com/f10/zycwzb_600010,season.html`

    year data
    `http://quotes.money.163.com/f10/zycwzb_600010,year.html`

    season is the preferred source.
    """
    _BASE = "http://quotes.money.163.com/f10/zycwzb_{},report.html"

    @classmethod
    def _get_base(cls):
        return cls._BASE

    @classmethod
    def _get_batch_size(cls):
        return 1

    @classmethod
    def _join_indices(cls, indices):
        length = len(indices)
        if length != 1:
            raise ValueError('only accept one stock per request.')
        return cls._process_index(indices[0])

    @classmethod
    def _process_index(cls, index):
        if index.startswith(('sh', 'sz')):
            index = index[2:]
        return index

    @classmethod
    def _parse(cls, body):
        matched = re.search(r'<div class="col_r" style="">(.*?)</div>', body,
                            re.MULTILINE | re.DOTALL | re.UNICODE)
        if matched is None or len(matched.groups()) == 0:
            raise ValueError('no matched data found.')

        lines = matched.group(1).strip().split('\n')

        value_pattern = re.compile(r'>(.*?)<', re.UNICODE)
        data_array = []
        stock_name = cls._get_stock_name(body)
        for line in lines:
            if r'<tr' not in line:
                continue

            data = []
            line = line.strip()
            for value in re.findall(value_pattern, line):
                value = cls._normalize(value)
                if isinstance(value, string_types) and len(value) == 0:
                    continue
                data.append(value)
            if len(data) > 0:
                data_array.append(data)

        if data_array:
            data_array.insert(0, [stock_name] * len(data_array[0]))
            data_array = np.array(data_array).T
        df = DataFrame(data_array, columns=NETEASE_STOCK_INFO_COLUMNS)
        df.set_index('日期', inplace=True)
        return df

    @classmethod
    def _get_stock_name(cls, text):
        ret = ''
        name_pattern = re.compile(r"var STOCKNAME = '(.+)';", re.UNICODE)
        for value in re.findall(name_pattern, text):
            ret = value
            break
        return ret

    @classmethod
    def _normalize(cls, value):
        value = value.strip()
        if value == '--':
            value = None
        elif '-' in value and not value.startswith('-'):
            value = int_date.to_int_date(value)
        elif len(value) > 0:
            if ',' in value:
                value = value.replace(',', '')
            value = float(value)
        return value

    @classmethod
    def _trans_index(cls, index):
        ret = index
        if index.startswith('sh'):
            ret = index.replace('sh', '0')
        elif index.startswith('sz'):
            ret = index.replace('sz', '1')
        return ret

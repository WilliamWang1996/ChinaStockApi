import logging
import requests
from china_stock_data_api import CnStockHttpError

__author__ = 'WangHao'

log = logging.getLogger(__name__)


class CnStockBase(object):
    def __init__(self):
        pass

    @classmethod
    def _get_base(cls):
        raise NotImplementedError('get_base must be implemented')

    @classmethod
    def _parse(cls, body):
        raise NotImplementedError('parse not implemented.')

    @classmethod
    def _parse_daily_data(cls,body,index):
        raise NotImplementedError('parse_data not implemented.')

    @classmethod
    def _join_indices(cls, indices):
        raise NotImplementedError('join_indices not implemented.')

    @classmethod
    def _get_batch_size(cls):
        return 100

    @classmethod
    def _process_index(cls, index):
        return index

    @classmethod
    def latest(cls, indices, method=None):
        if method is None:
            method = requests.get
        data = cls._retrieve_data(indices, method)
        return cls._parse(data)

    @classmethod
    def daily_k_line(cls,index,startDate,endDate,method=None):
        if method is None:
            method = requests.get
        data=cls._retrieve_daily_trade_data(index,startDate,endDate,method)
        return cls._parse_daily_data(data,index)


    @classmethod
    def _retrieve_daily_trade_data(cls,indices,startDate,endDate,method=None):
        if isinstance(indices, tuple):
            index = cls._join_indices(indices)
        else:
            index = cls._process_index(indices)
        url = cls._get_base().format(index,startDate,endDate)
        log.info("GET: %s", url)
        if method is None:
            response = requests.get(url, timeout=30)
        else:
            response = method(url)
        if response.status_code != 200:
            raise CnStockHttpError(url, response.status_code)
        response.encoding = 'utf-8'
        return response.text


    @staticmethod
    def _is_valid_number(number):
        from math import isnan, isinf
        valid = True
        if number is None or isinf(number) or isnan(number):
            valid = False
        return valid

    @classmethod
    def _retrieve_data(cls, indices, method=None):
        if isinstance(indices,tuple):
            index = cls._join_indices(indices)
        # if hasattr(indices, '__iter__'):
        #      index = cls._join_indices(indices)
        else:
            index = cls._process_index(indices)
        url = cls._get_base().format(index)
        log.info("GET: %s", url)
        if method is None:
            response = requests.get(url, timeout=30)
        else:
            response = method(url)
        if response.status_code != 200:
            raise CnStockHttpError(url, response.status_code)
        response.encoding='utf-8'
        return response.text

# coding=utf-8
from china_stock_data_api.cn_stock_util import CnStockHttpError as CnStockHttpError

__author__ = 'WangHao'

__all__ = [
    'latest',
    'latest_company_info',
    'CnStockHttpError']


def latest(*indices):
    """ Get the latest stock data

    Check readme for sample and output.
    :param indices: stock indices
    :return: data frame containing the latest stock data
    """
    from china_stock_data_api import sina
    return sina.latest(*indices)


def latest_company_info(*indices):
    """ Get the basic company information for indices

    Check readme for sample output.
    :param indices: stock indices
    :return: data frame containing the basic information
    """
    from china_stock_data_api import sina
    return sina.latest_company_info(*indices)


def financial_info(index):
    """ get the company financial info for index

    :param index: stock index
    :return: data frame containing financial data by season
    """
    from china_stock_data_api import netease
    return netease.NeteaseStockInfo.latest(index)


def daily_k_line(index,startDate,endDate):
    """ Get the k line for stock

    Check readme for sample output.
    :param index: stock index
           startDate: date for starting
           endDate: date for ending
    :return: date frame containing daily_k_line data between a period
    """
    from china_stock_data_api import netease
    return netease.NeteaseStock.daily_k_line(index,startDate,endDate)



def tdx(install_root_folder):
    from china_stock_data_api.tdx import TdxDataSource
    return TdxDataSource(install_root_folder)

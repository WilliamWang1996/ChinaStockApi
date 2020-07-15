# coding=utf-8
from __future__ import unicode_literals
import logging.config
import os
from multiprocessing import Pool, cpu_count

__author__ = 'WangHao'

__all__ = ['CnStockHttpError']


def get_thread_count():
    return cpu_count() + 2


def multi_thread(func, items, call_back=None, thread_count=None):
    if thread_count is None:
        thread_count = get_thread_count()

    executor = Pool(thread_count)
    results = executor.map(func, items)
    if call_back is not None:
        results = executor.map(call_back, results)
    return results


def get_file_dir(f):
    return os.path.dirname(os.path.realpath(f))


def read_file_in_same_dir(source_file, filename):
    folder = get_file_dir(source_file)
    the_file = os.path.join(folder, filename)
    with open(the_file, 'r') as f:
        ret = f.read()
    return ret


def config_logger():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True
            }
        }
    })


class CnStockHttpError(Exception):
    def __init__(self, url, status_code):
        msg = ('request failed.  url: {}, response status code: {}'
               .format(url, status_code))
        super(CnStockHttpError, self).__init__(msg)


TRADE_DETAIL_COLUMNS = ['name', 'open', 'close', 'price',
                        'high', 'low', 'volume', 'amount',
                        'buy1_volume', 'buy1_price',
                        'buy2_volume', 'buy2_price',
                        'buy3_volume', 'buy3_price',
                        'buy4_volume', 'buy4_price',
                        'buy5_volume', 'buy5_price',
                        'sell1_volume', 'sell1_price',
                        'sell2_volume', 'sell2_price',
                        'sell3_volume', 'sell3_price',
                        'sell4_volume', 'sell4_price',
                        'sell5_volume', 'sell5_price',
                        'date', 'time']

DAILY_K_LINE_COLUMNS = ['日期', '股票代码', '名称', '收盘价','最高价','最低价','开盘价','前收盘','跌涨额','跌涨幅','成交量','成交金额']


SINA_STOCK_INFO_COLUMNS = [
    '股票类型',
    '拼音缩写',
    '最近年度每股收益',
    '最近四个季度每股收益和',
    '季度每股收益',
    '季度每股净资产',
    '总股本（万元)',
    '流通股（万元）',
    '流通A股（万元）',
    '流通B股（万元）',
    '货币',
    '最近年度净利润（亿元）',
    '最近四个季度净利润（亿元）',
    '发行价格',
    '净资产收益率',
    '季度主营业务收入（亿元）',
    '季度净利润（亿元)'
]


NETEASE_STOCK_INFO_COLUMNS = [
    # 股票中文名
    '股票名称',
    # 日期(季度或年)
    '日期',
    # 基本每股收益(元)
    '基本每股收益(元)',
    # 每股净资产(元)
    '每股净资产(元)',
    # 每股经营活动产生的现金流量净额(元)
    '每股经营活动产生的现金流量净额(元)',
    # 主营业务收入(万元)
    '主营业务收入(万元)',
    # 主营业务利润(万元)
    '主营业务利润(万元)',
    # 营业利润(万元)
    '营业利润(万元)',
    # 投资收益(万元)
    '投资收益(万元)',
    # 营业外收支净额(万元)
    '营业外收支净额(万元)',
    # 利润总额(万元)
    '利润总额(万元)',
    # 净利润(万元)
    '净利润(万元)',
    # 净利润(扣除非经常性损益后)(万元)
    '净利润(扣除非经常性损益后)(万元)',
    # 经营活动产生的现金流量净额(万元)
    '经营活动产生的现金流量净额(万元)',
    # 现金及现金等价物净增加额(万元)
    '现金及等价物净增加额(万元)',
    # 总资产(万元)
    '总资产(万元)',
    # 流动资产(万元)
    '流动资产(万元)',
    # 总负债(万元)
    ' 总负债(万元)',
    # 流动负债(万元)
    '流动负债(万元)',
    # 股东权益不含少数股东权益(万元)
    '股东权益【不含少数股东权益】(万元)',
    # 净资产收益率加权(%)
    '净资产收益率加权(%)'
]

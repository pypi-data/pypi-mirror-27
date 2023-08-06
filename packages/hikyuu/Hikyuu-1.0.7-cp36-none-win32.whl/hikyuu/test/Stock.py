#!/usr/bin/python
# -*- coding: utf8 -*-
# gb18030

#===============================================================================
# 作者：fasiondog
# 历史：1）20120928, Added by fasiondog
#===============================================================================

import unittest

from test_init import *

class StockTest(unittest.TestCase):
    def test_stock(self):
        stock = sm["Sh000001"]
        self.assertEqual(stock.market, "SH")
        self.assertEqual(stock.code, "000001")
        self.assertEqual(stock.market_code, "SH000001")
        self.assertEqual(unicodeFunc(stock.name), u"上证指数")
        self.assertEqual(stock.type, 2)
        self.assertEqual(stock.startDatetime, Datetime(199012190000))
        self.assertEqual(stock.lastDatetime, constant.null_datetime)
        self.assertEqual(stock.tick, 0.001)
        self.assertEqual(stock.tickValue, 0.001)
        self.assertEqual(stock.unit, 1.0)
        self.assertEqual(stock.precision, 3)
        self.assertEqual(stock.atom, 1)
        self.assertEqual(stock.minTradeNumber, 1)
        self.assertEqual(stock.maxTradeNumber, 1000000)
        self.assertEqual(stock.getCount(), 5121)
        self.assertEqual(stock.getCount(KQuery.KType.MIN), 682823)
        self.assertEqual(stock.getKRecord(0).datetime, Datetime(199012190000))
        self.assertEqual(stock.getKRecord(1, KQuery.KType.MIN).datetime, Datetime(200001040932))
        
        s1 = sm['sh000001']
        s2 = sm['sh000001']
        self.assert_(s1 == s2)
        self.assert_(not (s1 != s2))
        
        s2 = sm['sz000001']
        self.assert_(not (s1 == s2))
        self.assert_(s1 != s2)
        
    def test_pickle(self):
        if not constant.pickle_support:
            return
        
        import pickle as pl
        filename = sm.tmpdir() + '/Stock.plk'
        fh = open(filename, 'wb')
        stock = sm['sh000001']
        pl.dump(stock, fh)
        fh.close()
        fh = open(filename, 'rb')
        b = pl.load(fh)
        fh.close()
        self.assertEqual(stock.name, b.name)
        self.assertEqual(b.market_code, 'SH000001')        
        
        
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(StockTest)

#!/usr/bin/python
# -*- coding: utf8 -*-
# gb18030

#===============================================================================
# 作者：fasiondog
# 历史：1）20130316, Added by fasiondog
#===============================================================================

import unittest

from test_init import *
from hikyuu.trade_sys.moneymanager import *

class MoneyManagerPython(MoneyManagerBase):
    def __init__(self):
        super(MoneyManagerPython, self).__init__("MoneyManagerPython")
        self.setParam("n", 10)
        self._m_flag = False
        
    def getBuyNumber(self, datetime, stock, price, risk):
        if self._m_flag:
            return 10
        else:
            return 20
    
    def _reset(self):
        if self._m_flag:
            self._m_flag = False
        else:
            self._m_flag = True
            
    def _clone(self):
        p = MoneyManagerPython()
        p._m_flag = self._m_flag
        return p

class MoneyManagerTest(unittest.TestCase):
    def test_ConditionBase(self):
        stock = sm['sh000001']
        p = MoneyManagerPython()
        self.assertEqual(p.name, "MoneyManagerPython")
        self.assertEqual(p.getParam("n"), 10)
        p.setParam("n",20)
        self.assertEqual(p.getParam("n"), 20)
        self.assertEqual(p.getBuyNumber(Datetime(200101010000), stock, 10.0, 0.0), 20)
        p.reset()
        self.assertEqual(p.getBuyNumber(Datetime(200101010000), stock, 10.0, 0.0), 10)
        
        p_clone = p.clone()
        self.assertEqual(p_clone.name, "MoneyManagerPython")
        self.assertEqual(p_clone.getParam("n"), 20)
        self.assertEqual(p_clone.getBuyNumber(Datetime(200101010000), stock, 10, 0.0), 10)

        p.setParam("n", 1)
        p_clone.setParam("n", 3)
        self.assertEqual(p.getParam("n"), 1)
        self.assertEqual(p_clone.getParam("n"), 3)
        
def testCrtMM(self):
    pass

def testgetBuyNumber(self, datetime, stock, price, risk):
    return 10.0 if datetime == Datetime(200101010000) else 0.0

class TestCrtMM(unittest.TestCase):
    def test_crt_mm(self):
        p = crtMM(testCrtMM, params={'n':10}, name="TestMM")
        p.getBuyNumber = testgetBuyNumber
        self.assertEqual(p.name, "TestMM")
        stock = sm['sh000001']
        self.assertEqual(p.getBuyNumber(p, Datetime(200101010000), stock, 1.0, 1.0), 10.0)
        self.assertEqual(p.getBuyNumber(p, Datetime(200101020000), stock, 1.0, 1.0), 0.0)
       
        p_clone = p.clone()
        self.assertEqual(p_clone.name, "TestMM")        
                 
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(MoneyManagerTest)

def suiteTestCrtMM():
    return unittest.TestLoader().loadTestsFromTestCase(TestCrtMM)
#!/usr/bin/env python
import sys
sys.path.append('../../_')
from ghana_panel import food_expenditures
import numpy as np

t = '2017-18'

myvars = dict(fn='../Data/11a_foodconsumption_prod_purch.dta',item='foodname',HHID='FPrimary',
              purchased='purchasedcedis',
              produced='producedcedis',
              given='receivedgiftcedis')

x = food_expenditures(**myvars)


x.index.name = 'j'
x.columns.name = 'i'
x['t'] = t
x['m'] = 'Ghana'

x = x.reset_index().set_index(['j','t','m'])

x = x.replace(0.,np.nan)

x.to_parquet('food_expenditures.parquet')

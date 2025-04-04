#!/usr/bin/env python
"""
Compile data on reported labor earnings.
"""
import pandas as pd
import numpy as np
from uganda import Waves, id_walk
import json


x = {}

for t in list(Waves.keys()):
    print(t)
    x[t] = pd.read_parquet('../'+t+'/_/earnings.parquet')
    x[t] = x[t].stack().squeeze()

x = pd.DataFrame(x)
x.columns.names = ['t']
x = pd.DataFrame({'earnings':x.stack()})

x['m'] = 'Uganda'
x = x.reset_index().set_index(['j','t','m'])

updated_ids = json.load(open('updated_ids.json'))
x = id_walk(x,updated_ids)

x.to_parquet('../var/earnings.parquet')

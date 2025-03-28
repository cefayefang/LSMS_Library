#!/usr/bin/env python
"""
Concatenate data on other household features across rounds.
"""

import pandas as pd
from uganda import change_id, id_walk, Waves
import json

x = {}

for t in Waves.keys():
    print(t)
    x[t] = pd.read_parquet('../'+t+'/_/household_characteristics.parquet')
    x[t] = x[t].stack('k').dropna()
    x[t] = x[t].reset_index().set_index(['j','k']).squeeze()


z = pd.DataFrame(x)
z.columns.name = 't'

z = z.stack().unstack('k')

# with open('panel_ids.json','r') as f:
#     panel_id_json =json.load(f)
# z = id_walk(z, Waves, panel_id_json)

try:
    of = pd.read_parquet('../var/other_features.parquet')

    z = z.join(of.reset_index('m')['m'],on=['j','t'])

except FileNotFoundError:
    z['m'] ='Uganda'

z = z.reset_index().set_index(['j','t','m'])


z.to_parquet('../var/household_characteristics.parquet')

#!/usr/bin/env python
"""
Concatenate data on other household features across rounds.
"""

import pandas as pd
from uganda import change_id, Waves, id_walk
import json

    
x = {}

for t in Waves.keys():
    print(t)
    x[t] = pd.read_parquet('../'+t+'/_/other_features.parquet')
    if 't' in x[t].index.names:
        x[t] = x[t].droplevel('t')
    x[t] = x[t].stack('k').dropna()
    x[t] = x[t].reset_index().set_index(['j','m','k']).squeeze()

z = pd.DataFrame(x)
z.columns.name = 't'

z = z.stack().unstack('m')

#z['m'] = 'Uganda'

# Harmonize region labels
regions = {' kampala':'Central',
           'central':'Central',
           'central without kampala':'Central',
           'eastern':'Eastern',
           'kampala':'Central',
           'nan':'Central',
           'northern':'Northern',
           'western':'Western'}

z = z.rename(columns=regions)

z = z.stack().unstack('k')

z = z.reset_index().set_index(['j','t','m'])

# panel_id_json = json.load(open('panel_ids.json'))
# z = id_walk(z, Waves, panel_id_json)

z.to_parquet('../var/other_features.parquet')

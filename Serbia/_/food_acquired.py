"""Calculate food prices for different items across rounds; allow
different prices for different units.
"""

import pandas as pd
import numpy as np

fa = []
for t in ['2007']:
    df = pd.read_parquet('../'+t+'/_/food_acquired.parquet')
    df = df.reset_index()
    df['t'] = t
    df = df.set_index(['j', 't', 'i', 'units'])
    df.index = df.index.rename({'units': 'u'})
    fa.append(df)

fa = pd.concat(fa)

of = pd.read_parquet('../var/other_features.parquet')

fa = fa.reset_index().merge(of.reset_index(), how='left', on=['j','t'])
fa = fa.reset_index().set_index(['j','t','m','i','u'])

fa = fa.replace(0,np.nan)
fa = fa.groupby(['j','m','t','i','u']).sum()
fa = fa.replace(0,np.nan)

fa.to_parquet('../var/food_acquired.parquet')

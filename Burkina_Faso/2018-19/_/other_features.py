#!/usr/bin/env python

import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
import dvc.api
from lsms import from_dta

with dvc.api.open('../Data/s00_me_bfa2018.dta', mode='rb') as dta:
    df = from_dta(dta, convert_categoricals=True)

df['j'] =  df["grappe"].astype(int).astype(str) + df["menage"].astype(int).astype(str).str.rjust(3, '0')

df  = df.groupby('j').agg({'s00q01' : 'first', 's00q04': 'first'}).rename({'s00q01': 'm', 's00q04':'Rural'}, axis =1)

time = pd.read_parquet('household_characteristics.parquet').reset_index().groupby('j').agg({'t':'first'})

df = pd.merge(left = df, right = time, how = 'left', left_index = True, right_index = True)
df['Rural'] = df['Rural'].map({'Rural':1, 'Urbain':0})

df = df.set_index(['t','m'], append = True)

df.to_parquet('other_features.parquet')

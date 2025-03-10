#!/usr/bin/env python
import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
import json
import dvc.api
from lsms import from_dta
sys.path.append('../../../_/')
from lsms_library.local_tools import df_from_orgfile, format_id

with dvc.api.open('../Data/SEC0A.DTA', mode='rb') as dta:
    df = from_dta(dta, convert_categoricals=True)

of = df[['clust','nh','region','loc2']]

of['hhid'] = of.apply(lambda x:format_id(x.clust)+format_id(x.nh),axis=1)

of = of.rename(columns = {'hhid': 'j',
                          'region': 'm',
                          'loc2': 'Rural'})

#map numerical codes to categorical labels 
rural = df_from_orgfile('./categorical_mapping.org',name='rural',encoding='ISO-8859-1')
rurald = rural.set_index('Code').to_dict('dict')
region = df_from_orgfile('../../_/categorical_mapping.org',name='region',encoding='ISO-8859-1')
regiond = region.set_index('Code').to_dict('dict')

of['Rural'] = of['Rural'].replace(rurald['Label'])
of['m'] = of['m'].apply(format_id).replace(regiond['Label'])

of['j'] = of['j'].astype(str)
of['t'] = '1998-99'
of = of.set_index(['j','t','m'])
of = of[['Rural']]

of.to_parquet('other_features.parquet')

#!/usr/bin/env python3
import json
from tanzania import Waves
import sys
sys.path.append('../../_')
from local_tools import panel_ids

D = panel_ids(Waves)

with open('panel_ids.json','w') as f:
    json.dump(D.data,f)
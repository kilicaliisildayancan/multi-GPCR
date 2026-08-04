"""Defining the control (min, max, average) hydrophobicity of known GPCRs from GPCRdb.
Getting data from GPCRdb based on family and TM segment (1 to 7).
Data goes into /hydrophobicity/GPCRdb_control_sequences/"""


import pandas as pd
from package_mgpcrs import general, mapHydrophobic
import os
import numpy as np
import re
import json
from urllib.request import urlopen



file = "/home/kilicali/multi-domain_gpcr/util/hydrophobicity/GPCRfamilies.json"
with open(file, 'r') as handle:
    families = json.load(handle)

proteins = [x for x in families if (x['slug'].count('_') == 2 and x['slug'][:2] == '00')] #get 00X_00X_00X only

store_dict = {}
for protein in proteins:
    family = protein['slug']
    name = protein['name']

    store_dict[name] = {}
    
    for segment in [f"TM{x}" for x in range(1,8)]: #iterate through all the TMs
        fetch_url = f"https://gpcrdb.org/services/alignment/family/{family}/{segment}/"
        response = urlopen(fetch_url)
        seq_data = json.loads(response.read().decode('utf-8'))

        store_dict[name][segment] = seq_data


out = "/home/kilicali/multi-domain_gpcr/util/hydrophobicity/GPCRfamily_sequences.json"

with open(out, 'w+') as handle:
    json.dump(store_dict, handle, indent=4)
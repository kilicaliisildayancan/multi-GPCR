"""
Parse HMMSCAN output using BioPython
"""

#BioPython imports
from Bio import SearchIO


#Other imports
import numpy as np
import json
import os
import sys

#define directories here
HMMSEARCH_FILE_DIR=str(sys.argv[1]) 
OUT_DIR=str(sys.argv[2])


#define global variables here
GOOD_CANDIDATES=[]
CHEMOKINE_TM_INDICES={1: (0, 35), 2: (39, 69), 3: (73, 109), 4: (117, 144), 5: (161, 198), 6: (201, 237), 7: (239, 272)}

TM_START_INDICES=np.array([x[0] for x in CHEMOKINE_TM_INDICES.values()])
TM_END_INDICES=np.array([x[1] for x in CHEMOKINE_TM_INDICES.values()])

tolerance=15

### RUNNING SCRIPT ###

#There is no way I could find to parse it in a for loop slowly, we have to load everything to the records object
for records in SearchIO.parse(HMMSEARCH_FILE_DIR,'hmmer3-text'):
    records

#Here iterating through all the hits
#Check here again if records.hsps go through the hits and not through the hsps!
for candidate in records.hits:
    #first check if there are multiple hits
    if len(candidate.hsps)>1:
        #we will count the number of helices based on profile (hmmfrom and hmmto)
        new_candidate={}
        e_values=[]

        hsp_range_pairs=[]
        for hsp in candidate.hsps:
            hsp_range_pairs.append(hsp.query_range)
            e_values.append(hsp.evalue)

        tm_counter=0
        for query_range in hsp_range_pairs:
            h=query_range[0]
            k=query_range[1]

            condition1=TM_END_INDICES-h>tolerance
            condition2=k-TM_START_INDICES>tolerance

            tm_hit_bool_vector=np.logical_and(condition1, condition2)
            tm_counter+=int(np.sum(tm_hit_bool_vector))

        new_candidate['name']=candidate.description_all[0]
        new_candidate['accession']=candidate.id
        new_candidate['e-values']=e_values
        new_candidate['tm_count']=tm_counter
        GOOD_CANDIDATES.append(new_candidate)

with open(OUT_DIR,'w+') as out_handle:
    json.dump(GOOD_CANDIDATES,out_handle)

#####################

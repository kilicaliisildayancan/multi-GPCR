"""
Collect the matches of a single search query into a parse-able TSV format. Arguments need to be passed from system:
	1. hmmer3 search output file path
	2. tsv file path

"""
    

#BioPython imports
from Bio import SearchIO


#Other imports
import numpy as np
import os
import sys

#define directories here
hmmout_file=str(sys.argv[1])
out_dir=str(sys.argv[2])

#define global variables here
master_list=[]

### RUNNING SCRIPT ###

records=SearchIO.read(hmmout_file,'hmmer3-text')
    
for hit in records:
    for hsp in hit.hsps:
        q_id=hsp.query.id
        q_st,q_end=hsp.query_range

        h_id=hsp.hit.id
        h_st,h_end=hsp.hit_range
       
        hitInfo=f'{h_id}\t{q_id}\t{q_st}\t{q_end}\t{h_st}\t{h_end}\n'
        
        constraint1=(q_end-q_st)>150
        constraint2=(h_end-h_st)>150
        constraint3=hsp.evalue<10e-4
        
        if constraint1 and constraint2 and constraint3:
        	master_list.append(hitInfo)

with open(out_dir, 'w+') as out:
    for hit in master_list:
        out.write(hit)

#####################

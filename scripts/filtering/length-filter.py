"""
This collects all seeds associated with a protein hit, and filters accoring to first (lowest index) and last hit (highest index).


"""

#BioPython imports
from Bio import SearchIO


#Other imports
import numpy as np
import os
import sys

#define directories here
infile=str(sys.argv[1])
outfile=str(sys.argv[2])

#define global variables here
master_dict={}
filtered=[]

### RUNNING SCRIPT ###

with open(infile, 'r') as inf:
    for line in inf:
        line=line.strip('\n').split('\t')

        prot=line[0]
        hitinfo=f'{line[1]};{line[2]};{line[3]};{line[4]};{line[5]}'
        if prot not in master_dict.keys():
            master_dict[prot]=[]
        master_dict[prot].append(hitinfo)

for key,value in master_dict.items():
    qhit=[]
    thit=[]
    for hitinfo in value:
        hitinfo=hitinfo.split(';')
        thit.append(int(hitinfo[3]))
        thit.append(int(hitinfo[4]))


    constraint=(max(thit)-min(thit))>550
    
    if constraint:
        filtered.append(key)



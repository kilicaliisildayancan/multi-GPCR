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


### RUNNING SCRIPT ###
def prefilter_hmmout(hmmout_file, out_dir, length_constraint):
    records=SearchIO.read(hmmout_file,'hmmer3-text')

    master_list = []

    for hit in records:
        for hsp in hit.hsps:
            q_id=hsp.query.id
            q_st,q_end=hsp.query_range

            h_id=hsp.hit.id
            h_st,h_end=hsp.hit_range
        
            hitInfo=f'{h_id}\t{q_id}\t{q_st}\t{q_end}\t{h_st}\t{h_end}\n'
            
            constraint1=(q_end-q_st) > length_constraint
            constraint2=(h_end-h_st) > length_constraint
            constraint3=hsp.evalue<10e-4
            
            if constraint1 and constraint2 and constraint3:
                master_list.append(hitInfo)

    with open(out_dir, 'w+') as out:
        for hit in master_list:
            out.write(hit)

    #####################

def lengthfilter_hmmout(infile, outfile, length_constraint):

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


        constraint=(max(thit)-min(thit))>length_constraint
        
        if constraint:
            filtered.append(key)

    with open(outfile, 'w+') as outf:
        outf.write('\n'.join(filtered))

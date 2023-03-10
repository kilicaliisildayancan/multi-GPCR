"""
Fetch sequences from UniRef90 database (not flexible currently)

"""
    
#BioPython imports
from Bio import SeqIO


#Other imports
import numpy as np
import os
import sys

#define directories here
infile=sys.argv[1]
DB='/bioseq/FASTA/uniprot/uniref90.fa'
outfile=sys.argv[2]

#define global variables here
sequence_list=[]
out_list=[]



### RUNNING SCRIPT ###

with open(infile, 'r') as inf:
	for line in inf:
		sequence_list.append(line.strip('\n'))

print(f'Got the sequences {sequence_list}')

for record in SeqIO.parse(DB,'fasta'):
	if record.id in sequence_list:
		out_list.append(record)
		print(f'found {record.id}')

with open(outfile, 'w+') as out:
	SeqIO.write(out_list,out,'fasta')

#####################

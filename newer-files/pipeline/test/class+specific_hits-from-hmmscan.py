"""
Parse HMMSCAN output using BioPython

"""
    

#BioPython imports
from Bio import SearchIO
from Bio import SeqIO


#Other imports
import numpy as np
import json
import os
import sys


#define directories here
hmmscan_file='/home/kilicali/multi-domain_gpcr/pipeline/test/gpcrdb-test_hmmscan.out' #str(sys.argv[1])
out_dir='/home/kilicali/multi-domain_gpcr/pipeline/test/paper-class+sp_hits-dict.json'  #str(sys.argv[2])

#define global variables here
master_dict={}

with open('/home/kilicali/multi-domain_gpcr/datafiles/primary_data/paper-mgpcrs.fasta','r') as handle:
	paperGPCRs=SeqIO.to_dict(SeqIO.parse(handle,'fasta'))

### RUNNING SCRIPT ###

for record in SearchIO.parse(hmmscan_file,'hmmer3-text'):
	protName=record.id
	protName=protName.split('_')[-1]
	if protName in list(paperGPCRs.keys()):
		seq_hit_vec=np.zeros(record.seq_len)

		master_dict[protName]={'A':0,'B1':0,'B2':0,'C':0,'D1':0,'F':0,'T':0,'ORPH':0}
		for hsp in record.hsps:
			family=hsp.hit_id.split('_')[0].split('+')[-1]
			if hsp.evalue_cond<=0.001:
			#couldn't figure out how to parse the matches using the match line, so here I'm just counting from the range of hits 
			#^EXCLUDING THE GAPS (LOWER LETTERS IN THE TARGET SEQUENCE (QUERY FOR HMMSCAN)
				gpcr=hsp.query.seq
				hit_range=hsp.query_range

				#clean up gpcr variable
				gpcr=gpcr.replace('-','')

				#fancy looking np code to do vectorized operation on the hsp sequence 
				#converting uppercase into True (1) and lowercase into False (0). 
				#This can be added back to seq_hit_vec defined above.
				hit_vec=np.char.isupper(np.array(gpcr, dtype='string_'))


				#finally add the hits without gaps into the main sequence vector
				seq_hit_vec[hit_range[0]:hit_range[1]]=seq_hit_vec[hit_range[0]:hit_range[1]]+hit_vec 

		#when one iter is finished, collect protName and appropriate vector into a dictionary
		master_dict[protName][family]=seq_hit_vec.tolist()	

with open(out_dir, 'w+') as out:
	#sort_keys and indent is not touched here as I couldn't get it to make it human-readable (there would be SO MANY LINES for lists of hits under the keys, which would be a problem all by itself. Due to this, I chose to remain as compact as possible.
	json.dump(master_dict,out)

#####################

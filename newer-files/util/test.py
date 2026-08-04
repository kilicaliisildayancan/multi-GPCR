from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
import json
from package_mgpcrs import count_tms_from_hmmout, general

verbose = True

##directories
hmmout_base = "/home/kilicali/multi-domain_gpcr/pipeline/hmmouts/"
for hmmout_file in os.listdir(hmmout_base): 

    hmmout_dir = hmmout_base + hmmout_file  

    base_addr = "/home/kilicali/multi-domain_gpcr/pipeline/clustered_taxonomy"
    gpcr_family_addr = os.path.join(general.HOME, "GPCRfamilies_with_indices.json")


    ##pipeline variables
    TM_START=8
    TM_END=22
    TM_COUNT=f"{TM_START}-{TM_END}"
    FAMILY_NAME = " ".join(hmmout_file.split('_')[2:]).split('.')[0] ### look into GPCRfamilies_with_indices.json for family name information

    print(f"\n{FAMILY_NAME} is being processed!")
    data_dir = os.path.join(base_addr, FAMILY_NAME.replace(' ','_'))
    out_file = os.path.join(data_dir, 'TM_counts.json')
    if os.path.exists(out_file):
        continue
    
    print(data_dir)

    # PIPELINE

    ##Counting TMs
    if verbose:
        print(f"Parsing the HMMOUT file!")
    with open(gpcr_family_addr, 'r') as infile:
        TM_indices_from_GPCRdb = [x['TM_index'] for x in json.load(infile) if x['name'].lower().replace('/', '-') == FAMILY_NAME.lower()][0] #fix issue with naming

    full_prot_data = count_tms_from_hmmout.count_TMs(HMMSEARCH_FILE_DIR=hmmout_dir, TM_INDICES=TM_indices_from_GPCRdb)


    ##filter TMs based on TM_START and TM_END
    good_proteins = [x for x in full_prot_data if (TM_START<x['tm_count']<TM_END and ( sum([y<1e-3 for y in x['e-values']])>0 )  )  ]

    cleaned = []
    for item in good_proteins:
        cleaned.append({'accession':item['accession'].split('_')[-1] , 'tm_count': int(item['tm_count'])})



    with open(out_file,'w+') as out:
        json.dump(cleaned, out)

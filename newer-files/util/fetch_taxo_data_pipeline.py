from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
import json
from package_mgpcrs import uniprotREST, count_tms_from_hmmout, general, cluster


# GLOBAL VARIABLES
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
    CLSTR_PERCENT_STR = "FORTY"
    CLSTR_PERCENT = "0.4"
    CLSTR_WORDSIZE = "2"

    print(f"\n{FAMILY_NAME} is being processed!")
    data_dir = os.path.join(base_addr, FAMILY_NAME.replace(' ','_'))

    if os.path.exists(data_dir):
        continue
    
    if not os.path.exists(data_dir):
        general.run_cmd(f"mkdir '{data_dir}'")
    print(data_dir)

    # PIPELINE

    ##Counting TMs
    if verbose:
        print(f"Parsing the HMMOUT file!")
    with open(gpcr_family_addr, 'r') as infile:
        TM_indices_from_GPCRdb = [x['TM_index'] for x in json.load(infile) if x['name'].lower().replace('/', '-') == FAMILY_NAME.lower()][0] #fix issue with naming

    full_prot_data = count_tms_from_hmmout.count_TMs(HMMSEARCH_FILE_DIR=hmmout_dir, TM_INDICES=TM_indices_from_GPCRdb)


    ##filter TMs based on TM_START and TM_END
    protein_acc_ids = [x['accession'].split('_')[-1] for x in full_prot_data if (TM_START<x['tm_count']<TM_END and ( sum([y<1e-3 for y in x['e-values']])>0 )  )  ]

    if verbose:
        print(f"{FAMILY_NAME} from hmmout file had {len(protein_acc_ids)} proteins that had {TM_COUNT} TM helices!")
    ##split into UPKB and UPI
    unikb_proteins = [x for x in protein_acc_ids if "UPI" not in x[:3]]
    uniparc_proteins = [x for x in protein_acc_ids if "UPI" in x[:3]]

    ##fetch responses
    if verbose:
        print("Fetching taxids and sequences from UPKB database!")
    UParc_responses = uniprotREST.request_UNIPARC(uniparc_proteins)
    UKB_responses = uniprotREST.request_UNIPROT(unikb_proteins)

    ##getting taxonomy info and writing to json
    if verbose:
        print("Parsing the taxids and writing to json!")
    accession_and_taxid = {}

    for entry in UParc_responses:
        accession = entry['uniParcId']
        if entry['uniParcCrossReferences'][0]['active'] == False:
            continue
        taxid = entry['uniParcCrossReferences'][0]['organism']['taxonId'] #this (hopefully) gets the taxonid of the protein
        accession_and_taxid[accession] = taxid


    for entry in UKB_responses:
        accession = entry['primaryAccession']
        taxid = entry['organism']['taxonId']
        accession_and_taxid[accession] = taxid


    write_json_directory = os.path.join(data_dir, "cluster_taxids.json")
    with open(write_json_directory, 'w+') as out:
        json.dump(accession_and_taxid, out)

    ##writing to fasta
    if verbose:
        print("Writing the sequences to a fasta file!")
    for element in UParc_responses:
        element['primaryAccession'] = element['uniParcId']

    UP_responses = UKB_responses + UParc_responses
    accession_and_sequences = []

    for response in UP_responses:
        accession_and_sequences.append(SeqRecord(seq=Seq(response['sequence']['value']), id=response['primaryAccession'],description=""))

    fasta_path = os.path.join(data_dir, f'ur100_{FAMILY_NAME.replace(" ", "_")}_{TM_COUNT}TM.fasta')
    SeqIO.write(sequences=accession_and_sequences, handle=fasta_path, format='fasta')

    ##clustering
    if verbose:
        print("Clustering the fasta file!\n")

    clstr_path = os.path.join(data_dir, f'ur100_{FAMILY_NAME.replace(" ", "_")}_{TM_COUNT}TM_clustered{CLSTR_PERCENT_STR}')
    clstr_command = f"cd-hit -i '{fasta_path}' -o '{clstr_path}' -c {CLSTR_PERCENT} -n {CLSTR_WORDSIZE}"
    general.run_cmd(clstr_command)


    ##parsing clusters into json
    other_clstr_path = f"{clstr_path}.clstr"

    cluster_data = cluster.cdhit_cluster(other_clstr_path,fasta_path)
    cluster_data.filter_cluster_by_length(5)

    clstr_json_out=os.path.join(data_dir, f'clusters.json')
    with open(clstr_json_out,'w+') as out_handle:
        json.dump(cluster_data.clusters, out_handle)


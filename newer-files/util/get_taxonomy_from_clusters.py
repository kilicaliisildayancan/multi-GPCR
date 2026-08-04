
import os
import json
from package_mgpcrs import uniprotREST, general

ACCESSION_TAXONID = {}
#get protein acc IDs from cluster file
clustered_directory = "/home/kilicali/multi-domain_gpcr/datafiles/clusters/chemokine_receptors/8-22TM/clusters.json"
with open(clustered_directory,'r') as infile:
    clusters_ids = json.load(infile)
all_ids = [x for l in clusters_ids.values() for x in l] #flatten the list

#split into upkb and uniparc ids
unikb_proteins = [x for x in all_ids if "UPI" not in x[:3]]
uniparc_proteins = [x for x in all_ids if "UPI" in x[:3]]

uniparc_responses = uniprotREST.request_UNIPARC(uniparc_proteins)
for entry in uniparc_responses:
    accession = entry['uniParcId']
    taxid = entry['uniParcCrossReferences'][0]['organism']['taxonId'] #this (hopefully) gets the taxonid of the protein
    ACCESSION_TAXONID[accession] = taxid

unikb_responses = uniprotREST.request_UNIPROT(unikb_proteins)
for entry in unikb_responses:
    accession = entry['primaryAccession']
    taxid = entry['organism']['taxonId']
    ACCESSION_TAXONID[accession] = taxid

write_directory = os.path.join(general.HOME, "clusters/chemokine_receptors/8-22TM/cluster_taxids.json")
with open(write_directory, 'w+') as out:
    json.dump(ACCESSION_TAXONID, out)



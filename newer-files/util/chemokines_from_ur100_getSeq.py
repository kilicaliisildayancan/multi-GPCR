from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
import json
from package_mgpcrs import uniprotREST, count_tms_from_hmmout, general

# count_tms_from_hmmout.count_TMs() <- already done
TM_COUNT="8-22"
with open('/home/kilicali/multi-domain_gpcr/focus_chemokines/chemokine_from_ur100_TM-counted.json','r') as handle:
    full_prot_data = json.load(handle)

protein_acc_ids = [x['accession'].split('_')[-1] for x in full_prot_data if (8<x['tm_count']<22 and ( sum([y<1e-3 for y in x['e-values']])>0 )  )  ]
print(len(protein_acc_ids))
print([x for x in protein_acc_ids if "UPI" in x[:3]][1])

#split uniparc IDs from uniprotkb IDs
unikb_proteins = [x for x in protein_acc_ids if "UPI" not in x[:3]]
uniparc_proteins = [x for x in protein_acc_ids if "UPI" in x[:3]]


UParc_responses = uniprotREST.request_UNIPARC(uniparc_proteins)
UKB_responses = uniprotREST.request_UNIPROT(unikb_proteins)

for element in UParc_responses:
    element['primaryAccession'] = element['uniParcId'] #fixing keys here for UPI entries

UP_responses = UKB_responses + UParc_responses # we can only request sequence values, and nothing else!

chemokine_sequences = []


for response in UP_responses:
    chemokine_sequences.append(SeqRecord(seq=Seq(response['sequence']['value']), id=response['primaryAccession'],description=""))

json_path= os.path.join(general.HOME, f'clusters/ur100_chemokines_{TM_COUNT}TM.json')
with open(json_path,'w+') as out_handle:
    json.dump(UP_responses,out_handle)

fasta_path = os.path.join(general.HOME, f'clusters/chemokine_receptors/{TM_COUNT}TM/ur100_chemokines_{TM_COUNT}TM.fasta')
SeqIO.write(sequences=chemokine_sequences, handle=fasta_path, format='fasta')

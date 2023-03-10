from urllib.request import urlopen
import json
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from Bio import AlignIO

# Define directories
outdir='/home/bental/multi-domain_gpcr/datafiles/primary_data/GPCRdb_aln'
familyInfo='/home/bental/multi-domain_gpcr/datafiles/GPCRfamilies.json'

# Define API base URL
baseUrl='https://gpcrdb.org/services/alignment/family'


familyName='naber'

# Get all subfamilies and their names from familyInfo json file
with open(familyInfo,'r') as handle:
    familyJSON=json.load(handle)

familyNames={}
for family in familyJSON:
    if family['slug']=='008':
        familyNames[family['slug']]='ORPH'
    
    elif len(family['slug'])==3 and family['slug'][:2]=='00':
        familyNames[family['slug']]=family['name'].split(' ')[1]

print(familyNames)

for family in familyJSON:
    # filter for only subfamilies (00N_00N)
    if len(family['slug'])==11 and family['slug'][:2]=='00': # latter removes G-protein and Arrestins (100_00N,200_00N)
        familySlug=family['slug']
        familyName=familyNames[familySlug.split('_')[0]]+'_'+family['parent']['name'].split(' ')[0].lower()+'_'+family['name'].lower().replace(' ','_').replace('/','-')  # re-formatting family names to fit file name formats

        print(familySlug)
        url=f'{baseUrl}/{familySlug}/'
        response=urlopen(url)
        alignment_seqs=json.loads(response.read().decode('utf-8'))

        # Create for loop to convert dictionary to a list of SeqRecord objects
        seq_records = []
        for name, sequence in alignment_seqs.items():
            seq_record = SeqRecord(Seq(sequence), id=name)
            seq_records.append(seq_record)

        # Create a MultipleSeqAlignment object from the list of SeqRecord objects
        alignment = MultipleSeqAlignment(seq_records)

        # Write the alignment to an out file

        with open(f'{outdir}/{familyName}.sto', 'w+') as handle:
            AlignIO.write(alignment, handle, 'stockholm')
    


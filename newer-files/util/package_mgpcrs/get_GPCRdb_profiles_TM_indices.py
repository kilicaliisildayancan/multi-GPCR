from urllib.request import urlopen
import json

#updating GPCRfamilies.json file
familyInfo='/home/kilicali/multi-domain_gpcr/datafiles/GPCRfamilies.json'
with open(familyInfo,'r') as handle:
    familyJSON=json.load(handle)

familyNames={}
for family in familyJSON:
    familySlug=family['slug']
    
    if not (family['slug'][:2]=='00' and len(family['slug'])==11):
        continue

    print(len(family['slug']), family['slug'])
    # #part for chemokines: slug = 001_003_002
    # chemokine_slug='001_003_002'

    #defining API URLs
    baseUrl='https://gpcrdb.org/services/alignment/family'

    #defining start and end index lists
    TM_INDICES={}


    #getting full 7TM alignment
    url=f'{baseUrl}/{familySlug}/TM1,ICL1,TM2,ECL1,TM3,ICL2,TM4,ECL2,TM5,ICL3,TM6,ECL3,TM7/'
    response=urlopen(url)
    alignment_seqs=json.loads(response.read().decode('utf-8'))
    main_seq=alignment_seqs['CONSENSUS'].replace('-','') #last alignment, common in all different family slugs !!! I'm removing gaps because of HMM profile stuff, more info in count_TM*.py


    #iterate through 1-7 and get the indices by finding it in main_seq
    for i in range(1,8):
        tm_name=f'TM{i}'
        tm_url=f'{baseUrl}/{familySlug}/{tm_name}/'
        tm_response=urlopen(tm_url)
        tm_alignment_seqs=json.loads(tm_response.read().decode('utf-8'))
        tm_seq=tm_alignment_seqs['CONSENSUS'].replace('-','') #!!! I'm removing gaps because of HMM profile stuff, more info in count_TM*.py
        start_index=main_seq.find(tm_seq)
        end_index=start_index+len(tm_seq)
        TM_INDICES[i]=(start_index,end_index)

    print(familySlug,TM_INDICES)
    family['TM_index']=TM_INDICES



family_with_TM_indices='/home/kilicali/multi-domain_gpcr/datafiles/GPCRfamilies_with_indices.json'

with open(family_with_TM_indices,'w+') as out_handle:
    json.dump(familyJSON, out_handle)
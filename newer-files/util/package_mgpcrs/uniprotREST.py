import time
import requests
import json



#define directories and constants





def request_UNIPROT(protein_accession_list: list, filter_for_existence: bool = False) -> list:
    """Requesting Uniprot information from the REST API. No filtering done on the output.
    protein_accession_list must be accession IDs without the first part (UniRefNNN_)"""

    baseURL='https://rest.uniprot.org/uniprotkb/search?query=accession:'
    query_builder='+OR+accession:'
    condition='+AND+(existence:1+OR+existence:2)'

    json_responses = []
    
    timedelay=5 #to not get banned from UniProt API xD
    counter=0
    window=20 #REST API doesn't respond more than 25 (it seems)

    while counter<len(protein_accession_list):
        subIDs=protein_accession_list[counter:counter+window]
        counter+=window
        url_prots=query_builder.join(subIDs)

        url=baseURL+'('+url_prots+')'
        if filter_for_existence:
            url = url+condition

        response=requests.get(url).text
        response_all=json.loads(response)['results']
        if len(response_all) != 0:
            json_responses+=response_all

        time.sleep(timedelay)
    return json_responses

def request_UNIPARC(protein_accession_list: list) -> list:
    """Requesting Uniprot information from the REST API. No filtering done on the output.
    protein_accession_list must be accession IDs without the first part (UniRefNNN_)"""

    baseURL='https://rest.uniprot.org/uniparc/search?query='
    query_builder='+OR+'
    

    json_responses = []
    
    timedelay=5 #to not get banned from UniProt API xD
    counter=0
    window=20 #REST API doesn't respond more than 25 (it seems)

    while counter<len(protein_accession_list):
        subIDs=protein_accession_list[counter:counter+window]

        counter+=window
        url_prots=query_builder.join(subIDs)

        url=baseURL+url_prots

        response=requests.get(url).text
        response_all=json.loads(response)['results']
        if len(response_all) != 0:
            json_responses+=response_all

        time.sleep(timedelay)
    return json_responses



def parse_uniprot_response(response_item:dict, desired_feature: list = ['primaryAccession','proteinExistence','proteinDescription','features', 'organism']):
    """This can parse the response of uniprot REST API responses based on desired keys. 
    response_item must be a dictionary (not the whole responses list of dicts!)"""
    collection={}
    
    for key in desired_feature:
        if key in list(response_item.keys()):
            collection[key]=response_item[key]
    return collection
    




#Imports
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import sys

#Directories and files
hitsIn="/home/kilicali/multi-domain_gpcr/datafiles/sequence_vectors/ecod92/hits_dict.json"

#Functions

def moving_average(npVector, window):
    mAvgVec=[]
    # line below adds spacers of zeros in front and at the end of vector to keep
    # track of initial indexes and make everything more fluent. window should be kept an uneven
    # number to go along with this.
    assert window%2==1

    npVector=np.array(list(np.zeros(window//2))+list(npVector)+list(np.zeros(window//2)))

    for i in range(len(npVector)):
        mAvg=np.average(npVector[i:i+window])
        mAvgVec.append(mAvg)
    return np.array(mAvgVec)

def filter_vector(npVector, hit_threshold):
    boolVec=[]
    for i in npVector:
        check=i>hit_threshold
        boolVec.append(check)
    return boolVec

def find_domains(boolVector,span_threshold):
    
    ### compressing boolVector ###
    ctr=0
    cmprVec=[]
    for i in boolVector:
        ctr+=i
        if i==0:
            cmprVec.append(ctr)
            ctr=0
    ### evaluating for span threshold ###
    # if a domain is longer/bigger than the threshold, the indexes of this domain are preserved for later use
    
    # convert zeros into ones for indexing
    for i in range(len(cmprVec)):
        if cmprVec[i]==0:
            cmprVec[i]=1


    dmn_indx_dict={}
    for i in range(len(cmprVec)):
        if cmprVec[i] >= span_threshold:
            st_indx=sum(cmprVec[:i]) #adds all the compressed domains before it
            end_indx=sum(cmprVec[:i+1]) #adds the length of this domain on top of the start index
            
            dmn_indx_dict[f'{len(dmn_indx_dict)}']=[st_indx,end_indx]
        else:
            pass


    return dmn_indx_dict


#Running stuff

with open(hitsIn, 'r') as inJ:
    hits_dict=json.load(inJ)

print(len(hits_dict))

mGPCRs2={}
mGPCRs3={}
mGPCRs4={}
mGPCRsLOT={}
falsePos={}

for key,value in hits_dict.items():
    mAvgVec=moving_average(value,15)
    boolVec=filter_vector(mAvgVec,10)
    domain_info=find_domains(boolVec,230)
    if len(domain_info)==2:
        mGPCRs2[key]=value
    elif len(domain_info)==3:
        mGPCRs3[key]=value
    elif len(domain_info)==4:
        mGPCRs4[key]=value
    elif len(domain_info)<2:
        falsePos[key]=value
    else:
        mGPCRsLOT[key]=value
# for key,value in mGPCRs.items():
#     mAvgVec=moving_average(value,15)
#     boolVec=filter_vector(mAvgVec,10)
#     domain_info=find_domains(boolVec,230)
#     plt.plot(value)
#     for i in domain_info.values():
#         plt.axvspan(i[0],i[1], alpha=0.2,facecolor='green')
#     plt.show()

# for key,value in falsePos.items():
#     mAvgVec=moving_average(value,15)
#     boolVec=filter_vector(mAvgVec,10)
#     domain_info=find_domains(boolVec,230)
#     plt.plot(value)
#     print(key,domain_info)
#     for i in domain_info.values():
#         plt.axvspan(i[0],i[1], alpha=0.2,facecolor='green')
#     plt.show()


with open('diGPCRs_hits.json','w+') as out:
    json.dump(mGPCRs2,out)

with open('triGPCRs_hits.json','w+') as out:
    json.dump(mGPCRs3,out)
with open('tetraGPCRs_hits.json','w+') as out:
    json.dump(mGPCRs4,out)
with open('polyGPCRs_hits.json','w+') as out:
    json.dump(mGPCRsLOT,out)

with open('falsePos_hits.json','w+') as out:
    json.dump(falsePos,out)


#Testing stuff

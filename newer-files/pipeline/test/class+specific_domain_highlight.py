#Imports
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np
import os
import sys
import json

#directories
# in_json=str(sys.argv[1])
# out_pdf=str(sys.argv[2])

in_json='/home/kilicali/multi-domain_gpcr/pipeline/test/paper-class+sp_hits-dict.json'
out_pdf='/home/kilicali/multi-domain_gpcr/pipeline/test/paper/out_pdf'

#constants
class_specifics={'A': {'color': '#808000', 'n_factor':62}, #Olive
'B1':{'color': '#800000', 'n_factor':5},                   #Maroon
'B2':{'color': '#9A6324', 'n_factor':9},                   #Brown
'C':{'color': '#42d4f4', 'n_factor':5},                    #Cyan
'D1':{'color': '#dcbeff', 'n_factor':1},                   #Lavender
'F':{'color': '#911eb4', 'n_factor':1},                    #Purple
'T':{'color': '#f58231', 'n_factor':1},                    #Orange
'ORPH':{'color': '#a9a9a9', 'n_factor':1}}                 #Gray


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

def plotM2PDF(plotDict, out, layout):
    ''' plotDict format: [proteinName]: [family]: y(sequenceVector) 
    ## y=(np.zeros(len(seq)) + np.ones(hits)), x would be (np.arange(len(seq)))
    layout is str(rowcolumn): example "61" for 6 plots in a column, and only one column PER PAGE!'''
    noPlots = len(plotDict.keys())
    pdf = matplotlib.backends.backend_pdf.PdfPages(out)
    figs=plt.figure()
    
    noFigs = int([*layout][0])*int([*layout][1])

    for i in range(int(np.ceil(noPlots/noFigs))):
        plot_num = int(f'{layout}1')
        fig = plt.figure(figsize=(10, 10)) # inches
        proNames = list(plotDict.keys())[i*noFigs:(i*noFigs)+noFigs]
        for proName in proNames:
            plt.subplot(plot_num)
            if len(list(plotDict[proName]))>1:
                print(proName)
            for family in plotDict[proName].keys():
                y = plotDict[proName][family]

                mAvgVec=moving_average(y,15)
                boolVec=filter_vector(mAvgVec,10)
                domain_info=find_domains(boolVec,230)
                plt.plot(y, color=class_specifics[family]['color'])
                for i in domain_info.values():
                    plt.axvspan(i[0],i[1],alpha=0.1,facecolor='green')

            plt.ylabel('% of Hits')
            plt.title(proName)

            plot_num += 1

        pdf.savefig()
        plt.close()

    pdf.close()


with open(in_json, 'r') as inJ:
	master_dict=json.load(inJ)


plot_dict={}



for key,value in master_dict.items():
    key=key.split('_')[-1]
    plot_dict[key]={}
    for family in value.keys():
        if value[family]!=0:
            yaxis=np.array(value[family])*(1/class_specifics[family]['n_factor'])*100
            plot_dict[key][family]=yaxis

A_dict={}
B1_dict={}
B2_dict={}
C_dict={}
D1_dict={}
F_dict={}
T_dict={}
ORPH_dict={}

for key in plot_dict.keys():
    if list(plot_dict[key].keys())[0]=='A':
        A_dict[key]={}
        A_dict[key]['A']=plot_dict[key]['A']
    elif list(plot_dict[key].keys())[0]=='B1':
        B1_dict[key]={}
        B1_dict[key]['B1']=plot_dict[key]['B1']
    elif list(plot_dict[key].keys())[0]=='B2':
        B2_dict[key]={}
        B2_dict[key]['B2']=plot_dict[key]['B2']
    elif list(plot_dict[key].keys())[0]=='C':
        C_dict[key]={}
        C_dict[key]['C']=plot_dict[key]['C']
    elif list(plot_dict[key].keys())[0]=='D1':
        D1_dict[key]={}
        D1_dict[key]['D1']=plot_dict[key]['D1']
    elif list(plot_dict[key].keys())[0]=='F':
        F_dict[key]={}
        F_dict[key]['F']=plot_dict[key]['F']
    elif list(plot_dict[key].keys())[0]=='T':
        T_dict[key]={}
        T_dict[key]['T']=plot_dict[key]['T']
    elif list(plot_dict[key].keys())[0]=='ORPH':
        ORPH_dict[key]={}
        ORPH_dict[key]['ORPH']=plot_dict[key]['ORPH']


if len(list(A_dict.keys()))!=0:
    plotM2PDF(plotDict=A_dict,out=f'{out_pdf}_A.pdf',layout='31')
if len(list(B1_dict.keys()))!=0:
    plotM2PDF(plotDict=B1_dict,out=f'{out_pdf}_B1.pdf',layout='31')
if len(list(B2_dict.keys()))!=0:
    plotM2PDF(plotDict=B2_dict,out=f'{out_pdf}_B2.pdf',layout='31')
if len(list(C_dict.keys()))!=0:
    plotM2PDF(plotDict=C_dict,out=f'{out_pdf}_C.pdf',layout='31')
if len(list(D1_dict.keys()))!=0:
    plotM2PDF(plotDict=D1_dict,out=f'{out_pdf}_D1.pdf',layout='31')
if len(list(T_dict.keys()))!=0:
    plotM2PDF(plotDict=T_dict,out=f'{out_pdf}_T.pdf',layout='31')
if len(list(F_dict.keys()))!=0:
    plotM2PDF(plotDict=F_dict,out=f'{out_pdf}_F.pdf',layout='31')
if len(list(ORPH_dict.keys()))!=0:
    plotM2PDF(plotDict=ORPH_dict,out=f'{out_pdf}_ORPH.pdf',layout='31')

        

#Imports
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np
import os
import sys
import json

#directories
in_json=str(sys.argv[1])
out_pdf=str(sys.argv[2])


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
    ''' plotDict format: [proteinName]: [x(np.arange(len(seq))), y(sequenceVector)] (np.zeros(len(seq)) + np.ones(hits))
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
            
            x = plotDict[proName][0]
            y = plotDict[proName][1]

            plt.subplot(plot_num)
            
            mAvgVec=moving_average(y,15)
            boolVec=filter_vector(mAvgVec,10)
            domain_info=find_domains(boolVec,230)
            plt.plot(y)
            for i in domain_info.values():
                plt.axvspan(i[0],i[1],alpha=0.2,facecolor='green')

            plt.ylabel('# of Hits')
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
    value=np.array(value)
    xaxis=np.arange(len(value))
    yaxis=value
    plot_dict[key]=[xaxis,yaxis]

plotM2PDF(plotDict=plot_dict,out=out_pdf,layout='31')


        

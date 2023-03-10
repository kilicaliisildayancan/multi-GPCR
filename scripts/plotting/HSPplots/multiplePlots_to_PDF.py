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


            plt.plot(y)
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
	value=np.array(value)
	xaxis=np.arange(len(value))
	yaxis=value
	plot_dict[key]=[xaxis,yaxis]

plotM2PDF(plotDict=plot_dict,out=out_pdf,layout='31')


        

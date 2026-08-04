"""
Parse HMMSCAN output using BioPython

"""
#BioPython imports
from Bio import SearchIO


#Other imports
import itertools
import numpy as np
import json
import os
import sys

#define directories here
hmmsearch_file=str(sys.argv[1])
out_dir=str(sys.argv[2])

#define global variables here
master_dict={}


### RUNNING SCRIPT ###

#There is no way I could find to parse it in a for loop slowly, we have to load everything to the records object
for records in SearchIO.parse(hmmsearch_file,'hmmer3-text'):
    records

tsvdata=[]
#Here iterating through all the hits
for candidate in records.hsps:
    
    #first check if there are multiple hits
    if len(candidate.hsps)>1:

        #domains have to be non-overlapping!
        #only thing I can think of is to deal with this in a combinatorial manner
        #I thought of a weird method to decide if the lines overlap, by using line equations (y=(-end/start)x+(end)). If the two line intersections overlap in the first quadran, the two line segments are overlapping

        #Currently, I will not throw away anything, but just print stuff out and see if anything is overlapping. I have tried dealing with it in the past but combinatorial stuff seemed too mixed to work with.
        segments=[] #list of tuples
        for hsp in candidate.hsps:
            if hsp.hit_span>150:
                segments.append(hsp.hit_range)
        #looking for each hit segment against each other
        lines=[]
        for segment in segments:
            a=segment[0]#start
            b=segment[1]#end
            m=-(b/a)#slope (when (start=x intersection),(end=y interx)
            assert m<-1 #this has to happen if b>a
            lines.append((m,b))
        
        for pair in itertools.combinations(range(len(lines)),2):
            fline,sline=lines[pair[0]],lines[pair[1]]
            x=(sline[1]-fline[1])/(sline[0]-fline[0])
            y=sline[0]*x+sline[1]
            if x>0 and y>0:
                print(f'These segments overlap in {candidate.id}! {segments[pair[0]]} and {segments[pair[1]]}') #report name
            else:
                tsvdata.append([candidate.id,str(len(segments))]) #store name if any pair is non-overlapping
        
with open(out_dir,'w+') as handle:
    handle.write('Name\tHitCount\tTaxID')
    for item in tsvdata:
        line='\t'.join(item)
        handle.write(line)            
#####################

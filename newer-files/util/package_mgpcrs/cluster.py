""" 
A class for handling cluster cd-hit files
"""
from package_mgpcrs.general import HOME, DATABASE_HOME
from Bio import SeqIO
import os
import json

class cdhit_cluster():

    def __init__(self, clstr_path, seq_path):
        """
        Valid arguments are:
        - Address of a .cluster file
        """
        self.sequences={}
        self.clusters={}
        self._parse_cluster_file(clstr_address = clstr_path, seq_address = seq_path)


    def _parse_cluster_file(self, clstr_address, seq_address):
        """
        Initializes the dictionary from a file,
        adding the clusters and their respective sequences
        Format:
        {[name]: "sequence",
        [cluster]: [name]}
        """
        suffix = clstr_address.split(".")
        if len(suffix) == 1:
            raise NotImplementedError(f"Has to be a .clstr file!")
        suffix = suffix[-1]

        with open(seq_address, "r") as sequence_handle:
            self.sequences=list(SeqIO.parse(sequence_handle,format='fasta'))
                

        with open(clstr_address, "r") as data_file:
            for line in data_file:
                line = line.strip()
                if line[:8] == ">Cluster":
                    name = line[1:]
                    if name and (name not in list(self.clusters.keys())):
                        self.clusters[name] = []
                else:
                    seqName = line[line.index(">")+1:line.index("...")] 
                    #deal with the shortening in cd-hit
                    for seq in self.sequences:
                        if seqName in seq.id:
                            seqName = seq.id
                    if "*" in line:
                        #insert to the first index the representative sequence
                        self.clusters[name].insert(0, seqName)    
                    elif "%" in line:
                        self.clusters[name].append(seqName)
                    

    def filter_cluster_by_length(self, min_cluster_length: int = 5):       
        filtered_clusters={key:value for key,value in zip(self.clusters.keys(),self.clusters.values()) if len(value) >= min_cluster_length}
        self.clusters=filtered_clusters
                    

    def write(self, out_address, cut_off = 1):
        print("not writing to file")



def run_tests():
    cluster_path= os.path.join(HOME, 'clusters/chemokine_receptors/8-22TM/ur100_chemokines_8-22TM_clusteredFORTY.clstr')
    sequence_path= os.path.join(HOME, 'clusters/chemokine_receptors/8-22TM/ur100_chemokines_8-22TM.fasta')
    ur100cluster = cdhit_cluster(cluster_path,sequence_path)
    ur100cluster.filter_cluster_by_length(5)
    
    write_path=os.path.join(HOME, f'clusters/chemokine_receptors/8-22TM/clusters.json')
    with open(write_path,'w+') as out_handle:
        json.dump(ur100cluster.clusters, out_handle)
    
if __name__ == "__main__":
    run_tests()


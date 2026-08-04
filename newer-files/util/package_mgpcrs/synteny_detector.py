#Using sorted genes (initial data from UCSC genome browser), this scripts outputs pairs of genes that are in the same orientation and closer than a given threshold

#imports
import os
import csv
import itertools


# global variables

INTER_DISTANCE_THRESHOLD = 200 * 1e3 #200k bp between end of one and the start of the other

# memory class

class geneMemory(list):
    
    def __init__(self, save_path, strand):
        self.path = save_path
        self.strand = strand



    def get_names(self):
        #get all the gene names from the memory (e.g. CCR2, CCR5, CCR7, etc. -- not unique identifiers)
        return [x['name'] for x in self]
    
    def intergenic_distance_handler(self, new_gene: dict):
        comparing_gene = self[0]

        if self.strand == "+":
            
            beg = comparing_gene['txEnd']
            end = new_gene['txStart']

        elif self.strand == "-":
            beg = comparing_gene['txStart']
            end = new_gene['txEnd']
        
        else:
            raise Exception(f"Strand is defined as {self.strand}, which is neither + or -.")
        

        inter_genic_range = abs(end-beg)

        if inter_genic_range > INTER_DISTANCE_THRESHOLD:
            return True
        else:
            return False


        
    

    def step_load(self, new_gene: dict):
        gene_name = new_gene['name']

        #check if gene name is unique
        if gene_name in self.get_names() and len(self) > 0:

            #check txStart and txEnd, update if new is smaller in txStart / bigger in txEnd
            mem_gene = [x for x in self if x['name'] == gene_name]
            assert len(mem_gene) == 1
            mem_gene = mem_gene[0]

            self[self.index(mem_gene)]['identifier'].append(new_gene['identifier'][0])

            if new_gene['txEnd'] > mem_gene['txEnd']:
                self[self.index(mem_gene)]['txEnd'] = new_gene['txEnd'] #indexing and updating the non-unique gene

            if new_gene['txStart'] < mem_gene['txStart']:
                self[self.index(mem_gene)]['txStart'] = new_gene['txStart']

        else:
            self.append(new_gene)

        if self.intergenic_distance_handler(new_gene):
            self.step_unload()
        

    def step_unload(self):
        assert len(self) > 0

        retain = self.pop()
        #pairing and appending
        if len(self) <= 1:
            pass
        else:
            self.append_gene_pair()

        
        self.clear()
        self.append(retain)


    def append_gene_pair(self):

        gene_pairs = list(itertools.combinations(self, 2)) #here the two-gene combinations of all the list

        with open(self.path, 'a') as append_out:
            for pair in gene_pairs:
                if pair[0]['strand'] == '+':
                    info = [pair[0]['name'], pair[1]['name'], str(abs(pair[1]['txStart']-pair[0]['txEnd']))]
                else:
                    info = [pair[0]['name'], pair[1]['name'], str(abs(pair[0]['txStart']-pair[1]['txEnd']))]
                line = '\t'.join(info)
                append_out.write(f'{line}\n')
            

    def eof(self):
        #handling when file is finished (end of file)
        if len(self) <= 1:
            self.clear()
        else:
            self.append_gene_pair()
            self.clear()


# functions

def genome_reader(file_path):
    with open(file_path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')

        next(tsv_reader) #here to skip the header
        for row in tsv_reader:
            yield row


def get_gene_attributes(geneAttrList: list):
    name = geneAttrList[12].upper()
    chrom = geneAttrList[2]
    strand = geneAttrList[3]
    txStart = int(geneAttrList[4])
    txEnd = int(geneAttrList[5])
    identifier = geneAttrList[1]
    return {
        "name": name,
        "chrom": chrom,
        "strand": strand,
        "txStart": txStart,
        "txEnd": txEnd,
        "identifier": [identifier]
    }


def find_syntenic_pairs(sorted_genes_path, paired_genes_path):
    species = sorted_genes_path.split('/')[-1]
    with open(paired_genes_path, 'w+') as init_f:
        line = f"Gene1\tGene2\tIG_distance_{species}\n"
        init_f.write(line)
    
    for file in os.listdir(sorted_genes_path):
        genome_path = os.path.join(sorted_genes_path, file)
        direction = file.split(',')[1]
        mem = geneMemory(paired_genes_path, strand=direction)
        
        genome_generator = genome_reader(genome_path)

        try:
            while True:
                gene = get_gene_attributes(next(genome_generator))
                if gene['name'] == 'SNAP91':
                    pass
                mem.step_load(gene)


        except StopIteration:
            mem.eof()
            print(f'done with {file}')




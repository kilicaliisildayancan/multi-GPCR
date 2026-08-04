import requests
import json
import csv

def read_loci_data(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            for key, value in row.items():
                row[key] = value.strip().replace('\n', '')
            data.append(dict(row))
    return data


class GenomicLocus():

    def __init__(self, locus_dict):
        self.organism = locus_dict['organism']
        self.locus = locus_dict
    
        self.baseAPI = f"https://api.genome.ucsc.edu/getData/sequence?genome={self.locus['genome']};chrom={self.locus['chromosome']};start={self.locus['start']};end={self.locus['end']}"
    
    def reverse_complement(self, dna_sequence):
        complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'a': 't', 't': 'a', 'g': 'c', 'c': 'g', 'n': 'n', 'N': 'N'}
        reverse_sequence = dna_sequence[::-1]
        reverse_complement_sequence = ''.join(complement_map[base] for base in reverse_sequence)
        return reverse_complement_sequence

    def fetch_sequence(self):
        locus_response = requests.get(self.baseAPI).text
        self.dna_sequence = json.loads(locus_response)['dna']

        if self.locus['orientation'] == '-':
            self.dna_sequence = self.reverse_complement(self.dna_sequence)
    
    def print(self, base_address):
        
        with open(f"{base_address}/{self.organism}_CCR2-CCR5.fasta", "w+") as out:
            out.write(f">{self.organism}_genome-{self.locus['genome']}_chr-{self.locus['chromosome']}_start-{self.locus['start']}_end-{self.locus['end']}\n")
            out.write(f"{self.dna_sequence}\n")

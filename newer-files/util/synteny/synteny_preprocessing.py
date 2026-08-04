#Pre-processing for chromosome data acquired from UCSC genome browser Table (?) tool.
#We will be separating the whole file into separate chromosomes, and then sorting each dataframe by the "txStart" variable

import pandas as pd
import os


#functions

def separate_genome_by_attr(df: pd.DataFrame, attr): #takes in a panda df from pd.read_csv()
    grouped = df.groupby(attr)
    return grouped




#running

if __name__ == "__main__":

    base_name = "zebrafish_GRCz11-danRer11_ncbiRefSeq"
    species = base_name.split('_')[0]

    input_path = f"/home/kilicali/multi-domain_gpcr/datafiles/synteny_analysis/UCSC_data/raw_data_genomes/{base_name}.tsv"
    output_path = f"/home/kilicali/multi-domain_gpcr/datafiles/synteny_analysis/UCSC_data/sorted/running/{species}/"
    
    df = pd.read_csv(input_path, sep = '\t')
    



    sep_chroms = separate_genome_by_attr(df, 'chrom')
    for chrom, chrom_group in sep_chroms:
        
        sep_strands = separate_genome_by_attr(chrom_group, 'strand')

        for strand, strand_group in sep_strands:
            if strand == "+":
                sorted_group = strand_group.sort_values(by="txStart", ascending=True)
            else:
                sorted_group = strand_group.sort_values(by="txStart", ascending=False)
            
            print(chrom, strand)
            print(sorted_group)
            out_path = os.path.join(output_path, f'{chrom},{strand},{base_name}.tsv')
            sorted_group.to_csv(out_path, sep = '\t', index=False)

"""Here, we compare two files that have gene pairs (tsv format) from two different species.
If we find the same pair, this might be indicative of a multi-domain protein isoform.
Basically, looking at the intersection of two sets of gene pairs.


Additionally, before discarding a pair that was not found, we check if both of these genes
in the pair existed in the genome of the compared species in the first place.
The order is done relative to CROSS_SPECIES[0].
This is done to assert a true negative on the eliminated list, because maybe this gene pair is just not
annotated properly in the target species genome data.
"""
import pandas as pd
from package_mgpcrs import general
import os
import numpy as np
import re

CROSS_SPECIES = ["human-mouse-cat-chicken", "zebrafish"]

#this definition requires a specific syntax: first element has one or more (written like this: species1-species2-...-speciesN) and the second is a single species!
if "-" in CROSS_SPECIES[0]:
    ALL_SPECIES = CROSS_SPECIES[0].split('-') + [CROSS_SPECIES[1]]
else:
    ALL_SPECIES = CROSS_SPECIES

genome_genes_path = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/raw_data_genomes/stats/gene_sets.tsv")

first_species_path = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/conservation/main_seeds/{CROSS_SPECIES[0]}_syntenic_gene-pairs.tsv")
second_species_path = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/sorted/{CROSS_SPECIES[1]}_syntenic_gene-pairs.tsv")

out_path = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/conservation/eliminative/{CROSS_SPECIES[0]}-{CROSS_SPECIES[1]}_syntenic_gene-pairs.tsv")
non_elim_path = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/conservation/non_eliminative/{CROSS_SPECIES[0]}-{CROSS_SPECIES[1]}-missing-gene-pairs-in-{CROSS_SPECIES[1]}.tsv")
joined_path = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/conservation/main_seeds/{CROSS_SPECIES[0]}-{CROSS_SPECIES[1]}_syntenic_gene-pairs.tsv")

first_gene_pairs = pd.read_csv(first_species_path, sep = '\t')
second_gene_pairs = pd.read_csv(second_species_path, sep = '\t')
full_pool = pd.read_csv(genome_genes_path, sep = '\t')

second_species_genome = re.sub('[{ \'}]','',full_pool[full_pool['species'] == f"{CROSS_SPECIES[1]}"]['gene_set'].values[0]).split(',')
syn_columns = ['Gene1', 'Gene2'] + [f"IG_distance_{x}" for x in ALL_SPECIES]
syn_columns2 = ['Gene1', 'Gene2'] + [f"IG_distance_{x}" for x in ALL_SPECIES[:-1]]
syntenic_pairs = pd.DataFrame(columns=syn_columns)
cant_eliminate = pd.DataFrame(columns=syn_columns2)


for row in first_gene_pairs.itertuples():
    index = row[0]
    gene1 = row[1]
    gene2 = row[2]

    if (gene1 in second_species_genome) and (gene2 in second_species_genome):
            
        condition = f"('{gene1}' in Gene1) and ('{gene2}' in Gene2)"

        syntenic_match = second_gene_pairs.query(condition)

        
        if not syntenic_match.empty:
            first_species_ig_dist = [a for a in row[3:]]
            second_species_ig_dist = syntenic_match.drop(columns=["Gene1", "Gene2"]).values[0].tolist()

            two_genes = syntenic_match[["Gene1", "Gene2"]].values[0].tolist()
                
            full_row = pd.DataFrame([two_genes + first_species_ig_dist + second_species_ig_dist], columns=syn_columns)
                
                

            syntenic_pairs = pd.concat([syntenic_pairs, full_row], axis=0, ignore_index=True)
            print(full_row)
    else:

        new_row = pd.DataFrame([row[1:]], columns=syn_columns2)        
        cant_eliminate = pd.concat([cant_eliminate, new_row], axis=0, ignore_index=True)

    
non_eliminative = pd.concat([syntenic_pairs, cant_eliminate], ignore_index=True)

syntenic_pairs.to_csv(out_path, sep='\t', index=False)
cant_eliminate.to_csv(non_elim_path, sep='\t', index=False)

non_eliminative.to_csv(joined_path, sep='\t', index=False)
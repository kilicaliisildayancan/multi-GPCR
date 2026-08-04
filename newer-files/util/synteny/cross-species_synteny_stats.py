"""Looking at how many genes are found in the intersection in pairs
relative to how many genes could have been found"""

import pandas as pd
import os
from package_mgpcrs import general
import re

SPECIES1 = 'human-mouse'
SPECIES2 = 'cow'

paired_dir = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/sorted/{SPECIES1}-{SPECIES2}_syntenic_gene-pairs.tsv")
full_dir = os.path.join(f"{general.HOME}/synteny_analysis/UCSC_data/raw_data_genomes/stats/gene_set_combinations.tsv")

paired_pool = pd.read_csv(paired_dir, sep = '\t')
full_pool = pd.read_csv(full_dir, sep = '\t')




paired_genes = set(paired_pool[["Gene1", "Gene2"]].values.flatten().tolist())

all_genes = set(re.sub('[{ \'}]','',full_pool[full_pool['species'] == f"{SPECIES1}+{SPECIES2}"]['gene_set'].values[0]).split(','))

print(f'{len(set.intersection(paired_genes, all_genes))} out of {len(all_genes)}')
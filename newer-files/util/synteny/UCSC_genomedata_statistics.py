"""Investigating genome data from UCSC tables, used in our syntenic gene pair analysis.
Here, we will benchmark genomic information across multiple species (how many genes are in common
between species we use to detect conservation of synteny) to understand the pool of possible positive results."""
from package_mgpcrs import general
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

writing = False

gene_sets = pd.DataFrame(columns = ["species","gene_counter","gene_set"])
combinations = pd.DataFrame(columns=["species", "gene_counter", "gene_set"])
mcombinations = pd.DataFrame(columns=["species", "gene_counter", "gene_set"])

all_data_dir = ['rhesus_rheMac10_ncbiRefSeq',
                'cat_felCat9_ncbiRefSeq',
                 'chicken_GRCg6a-galGal6_ncbiRefSeq',
                 'chimp_panTro6_ncbiRefSeq',
                 'cow_bosTau9_ncbiRefSeq',
                 'gorilla_gorGor6_ncbiRefSeq',
                 'human_GRCh38-hg38_allGencodeV43-comprehensive',
                 'mouse_GRCm38-mm10_allGencodeVM25-comprehensive',
                 'rhesus_rheMac10_ncbiRefSeq',
                 'zebrafish_GRCz11-danRer11_ncbiRefSeq',
                 'drosophila_droMel_ncbiRefSeq']

for data in all_data_dir:
    species = data.split('_')[0]
    input_path = f"/home/kilicali/multi-domain_gpcr/datafiles/synteny_analysis/UCSC_data/raw_data_genomes/{data}.tsv"

    df = pd.read_csv(input_path, sep = '\t')
    gene_set = set(df['name2'].apply(str).apply(str.upper))
    gene_sets = gene_sets.append({"species": species,"gene_counter": len(gene_set),"gene_set": list(gene_set)}, ignore_index=True)
if writing:
    gene_sets.to_csv(f"{general.HOME}/synteny_analysis/UCSC_data/raw_data_genomes/stats/gene_sets.tsv", sep='\t')

for first_sp in gene_sets.iterrows():
    for second_sp in gene_sets.iterrows():
        if first_sp[1]['species'] == second_sp[1]['species']:
            continue
        genes1 = set(first_sp[1]['gene_set'])
        genes2 = set(second_sp[1]['gene_set'])
        combination = genes1.intersection(genes2)
        combinations = combinations.append({"species": f"{first_sp[1]['species']}+{second_sp[1]['species']}",
                                            "gene_counter": len(combination),
                                            "gene_set": list(combination)}, ignore_index=True)

if writing:
    combinations.to_csv(f"{general.HOME}/synteny_analysis/UCSC_data/raw_data_genomes/stats/gene_set_combinations.tsv", sep='\t')

#doing combinations with multiple gene sets

human_genes = gene_sets[gene_sets['species']=='human']['gene_set'].values[0]
mouse_genes = gene_sets[gene_sets['species']=='mouse']['gene_set'].values[0]

addon_species = ['mouse', 'cat', 'cow', 'zebrafish']

init_gset = set(human_genes)
for index in range(len(addon_species)):
    gset = set(gene_sets[gene_sets['species']==addon_species[index]]['gene_set'].values[0])
    new_set = set.intersection(init_gset, gset)
    mcombinations =  mcombinations.append({"species": 'human+'+'+'.join(addon_species[:index+1]),"gene_counter": len(new_set),"gene_set": list(new_set)}, ignore_index=True)
    
if True:
    mcombinations.to_csv(f"{general.HOME}/synteny_analysis/UCSC_data/raw_data_genomes/stats/gene_set_multiple_combinations.tsv", sep='\t')
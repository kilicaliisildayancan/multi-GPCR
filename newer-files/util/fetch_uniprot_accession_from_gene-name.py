from package_mgpcrs import functional_gene_relationships
import os

tsv_data_dir = "/home/kilicali/multi-domain_gpcr/datafiles/synteny_analysis/UCSC_data/sorted/human-mouse_syntenic_gene-pairs.tsv"
base_tsv_out_dir = "/home/kilicali/multi-domain_gpcr/datafiles/synteny_analysis/functional_pairing/human-mouse_interacting/"
base_tsv_in_dir = "/home/kilicali/multi-domain_gpcr/datafiles/synteny_analysis/functional_pairing/human-mouse_FULL/"

for file in os.listdir(base_tsv_in_dir):
    int_pairs = functional_gene_relationships.KI_proteins()


#for online scrape

# genelist = []
# with open(tsv_data_dir, 'r') as tsv_data:
#     tsv_data.readline()
#     for line in tsv_data:
#         line = line.split('\t')
#         genelist.append([line[0], line[1]])

# for pair1, pair2 in genelist:
#     int_pairs = functional_gene_relationships.KI_proteins()
#     int_pairs.from_online(prot1 = pair1, prot2 = pair2)
#     if int_pairs.check_similar_attributes():
#         int_pairs.tsv_out(out_dir= f"{base_tsv_out_dir}{pair1}_{pair2}.tsv")
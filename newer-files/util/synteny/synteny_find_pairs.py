"""For a given genome (data from UCSC) of a species, we pair 
proximal and same-orientation genes under a given threshold."""


from package_mgpcrs import synteny_detector, general

import os

#paths
species = "zebrafish"
sorted_genome_dir = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/sorted/running/{species}")
paired_out = os.path.join(general.HOME, f"synteny_analysis/UCSC_data/sorted/{species}_syntenic_gene-pairs.tsv")

#running

synteny_detector.find_syntenic_pairs(sorted_genes_path=sorted_genome_dir, paired_genes_path=paired_out)

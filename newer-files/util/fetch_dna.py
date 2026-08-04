from package_mgpcrs import genomic_dna


loci_data_address = "/home/kilicali/multi-domain_gpcr/focus_chemokines/CCR2-CCR5/loci.csv"



loci_data = genomic_dna.read_loci_data(loci_data_address)

for locus in loci_data:
    loci_dna = genomic_dna.GenomicLocus(locus)
    loci_dna.fetch_sequence()
    loci_dna.print("/home/kilicali/multi-domain_gpcr/focus_chemokines/CCR2-CCR5/genomic_dna/loci_sequences")

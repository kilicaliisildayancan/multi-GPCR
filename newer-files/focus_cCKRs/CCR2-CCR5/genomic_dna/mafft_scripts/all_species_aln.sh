#! /bin/bash

DIR="/home/kilicali/multi-domain_gpcr/focus_chemokines/CCR2-CCR5/genomic_dna/non-primates/non-primate_loci_sequences"
MAINALN="/home/kilicali/multi-domain_gpcr/focus_chemokines/CCR2-CCR5/genomic_dna/non-primates/main.aln"
TEMPALN="/home/kilicali/multi-domain_gpcr/focus_chemokines/CCR2-CCR5/genomic_dna/non-primates/temp.aln"


for i in $DIR/*;
    do
    mafft --6merpair --addfragments $i $MAINALN > $TEMPALN
    cp $TEMPALN $MAINALN
    done

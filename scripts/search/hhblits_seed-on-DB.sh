#!/bin/bash

###  PBS LINES HERE ARE RELEVANT TO THE HPC CLUSTER IN OUR UNIVERSITY, PLEASE REFER TO WIKI PAGE FOR DOCUMENTATION

#PBS -e /scratch200/kilicali/LOG/hhblits_err.log
#PBS -o /scratch200/kilicali/LOG/hhblits_out.log
#PBS -l select=1:ncpus=8:mem=64g
#PBS -q bentalweb

cd /a/home/cc/lifesci/kilicali/pipe_ecod92/
module load hh-suite  #loading relevant programs


INDIR='/scratch200/kilicali/ECOD/sequences'
DB='/bioseq/FASTA/uniprot/UniRef30/UniRef30_2022_02'
OUT='/scratch200/kilicali/ECOD/msas'

for FILE in $INDIR/*.fasta;
	do
	FASTA=${FILE##*/}
	NAME=${FASTA/.fasta/.a3m}
	hhblits -cpu 7 -i $FILE -d $DB -oa3m $OUT/$NAME -cov 90 -qid 30;
	done



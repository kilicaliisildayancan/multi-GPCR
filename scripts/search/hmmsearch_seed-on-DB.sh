#!/bin/bash
#PBS -e /scratch200/kilicali/LOG/hmmsearch-ecod92_err.log
#PBS -o /scratch200/kilicali/LOG/hmmsearch-ecod92_out.log
#PBS -l select=1:ncpus=5:mem=64g
#PBS -q bentalweb

cd /a/home/cc/lifesci/kilicali/pipe_ecod92/
module load hmmer/hmmer-3.2.1 

UNIREF='/bioseq/FASTA/uniprot/uniref90.fa'
HMMPROFILEDIR='/scratch200/kilicali/ECOD/hmmprofiles_trachel' 
RESDIR='/scratch200/kilicali/ECOD/hmmouts'


for FILE in $HMMPROFILEDIR/*;
	do
	HMMNAME=${FILE##*/}
	HMMOUT=${HMMNAME/.hmm/.out}
	hmmsearch -E 0.001 --cpu 4 -o $RESDIR/$HMMOUT $FILE $UNIREF;
	done

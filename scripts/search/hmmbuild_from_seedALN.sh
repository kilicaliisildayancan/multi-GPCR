#!/bin/bash
#PBS -e /scratch200/kilicali/LOG/hmmbuild_err.log
#PBS -o /scratch200/kilicali/LOG/hmmbuild_out.log
#PBS -l select=1:ncpus=1:mem=32g
#PBS -q bentalweb

cd /a/home/cc/lifesci/kilicali/pipe_ecod92/
module load hmmer/hmmer-3.2.1 

MSADIR='/scratch200/kilicali/ECOD/msas'
HMMDIR='/scratch200/kilicali/ECOD/hmmprofiles'

for FILE in $MSADIR/*.sto;
	do
	
	STO=${FILE##*/}
	HMM=${STO/.sto/.hmm}
	echo "hmmfile: $HMMDIR/$HMM; msafile: $FILE"
	hmmbuild $HMMDIR/$HMM $FILE;
	done


#!/bin/bash
#PBS -e /scratch200/kilicali/LOG/hmmscan_err.log
#PBS -o /scratch200/kilicali/LOG/hmmscan_out.log
#PBS -l select=1:ncpus=1:mem=32g
#PBS -q bentalweb

cd /a/home/cc/lifesci/kilicali/pipe_ecod92/
module load hmmer/hmmer-3.2.1 

TOSCAN='/scratch200/kilicali/ECOD/length-filter/candidates.fasta'
PRESSEDDIR='/scratch200/kilicali/ECOD/pressedhmms' 
RESDIR='/scratch200/kilicali/ECOD/scanouts'

hmmscan  --tblout $RESDIR/ecod92-on-candidates_hmmscan.tblout -o $RESDIR/ecod92-on-candidates_hmmscan.out $PRESSEDDIR/ecod92.hmms $TOSCAN


#!/bin/bash
#PBS -e /scratch200/kilicali/LOG/hmmpress_err.log
#PBS -o /scratch200/kilicali/LOG/hmmpress_out.log
#PBS -l select=1:ncpus=1:mem=32g
#PBS -q bentalweb

cd /a/home/cc/lifesci/kilicali/pipe_ecod92/
module load hmmer/hmmer-3.2.1 

OUTDIR='/scratch200/kilicali/ECOD/pressedhmms'

hmmpress $OUTDIR/ecod92.hmms 


#!/bin/bash
#PBS -e /scratch200/kilicali/LOG/clstr_err.log
#PBS -o /scratch200/kilicali/LOG/clstr_out.log
#PBS -l select=1:ncpus=2:mem=32g
#PBS -q bentalweb

cd /a/home/cc/lifesci/kilicali/util/
module load cdhit

cd-hit -i /scratch200/kilicali/ECOD/length-filter/candidates.fasta -o /scratch200/kilicali/ECOD/length-filter/clustered-candidates -c 0.5 -T 0 -n 3

#!/bin/bash
#PBS -e /scratch200/kilicali/LOG/reformat_err.log
#PBS -o /scratch200/kilicali/LOG/reformat_out.log
#PBS -l select=1:ncpus=1:mem=32g
#PBS -q bentalweb

MSADIR='/scratch200/kilicali/ECOD/msas'



cd /a/home/cc/lifesci/kilicali/pipe_ecod92/

for FILE in $MSADIR/*;
        do 
        STO=${FILE/.a3m/.sto}
        perl reformat.pl $FILE $STO;
        done


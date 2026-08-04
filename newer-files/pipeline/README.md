This is the current pipeline in order. In paranthese is the name of the file
that represents that step.

*N represents each sequence, $N represents one file with all info in it.
>>> Starting with N sequences as seeds and a target database to search for
>>> mGPCRs against!

1. *N.fasta -[UniRef30]-> *N.a3m
(hhblits): Create an alignment to increase the power of the hmm profile. 


2. *N.a3m -> *N.sto
(reformat.pl): reformat .a3m to .sto to be suitable for hmmbuild command.


3. *N.sto -> *N.hmm
(hmmbuild): Build hmm profiles from alignments


4. *N.hmm -[target DB]-> *N.out
(hmmsearch): Search the target database using the hmmprofiles.
Use an e-value cutoff appropriate to the database (10e-3 for
small, 10e-6 for big).


5. *N.out -> $N.db
(filter1.py): The search in 4. will also hit single GPCRs. Filter according to
a very lenient/lax parameter these single GPCRs and add the sequences to a db.


6. *N.hmm (from 3.) -> $N.hmms 
(cat): Concatenate all ECOD domains into one hmm file! It is cruical that it
is only ECODs, because they contain solely the TM part!


7. $N.hmms -> $N.pressd
(hmmpress): Press ecod hmm profiles into a hmm profile db.


8. $N.pressd -[$N.db]-> $N.scanned
(hmmscan): Use the ECOD pressed hmm profile db to search against the potential
mGPCR candidates sequence database. Save the output in both .out and .tbl
format.


9. $N.scanned -> mGPCRs.db
(filter2.py): BioPython to filter false hits and finding multiple ECOD92 TM
matches.


10. mGPCRs.db analysis
(multiple): CD-HIT to cluster them into 70% seq identity. Use data from
$N.scanned to look at multiple non-overlapping full 7TM helices!

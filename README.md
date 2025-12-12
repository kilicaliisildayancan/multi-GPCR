# multi-GPCRs

Research project repositofy for identifying and analyzing multi-domain GPCRs.

## Important note for oncomers (weird, but OK):

Due to the attack on October, my research was abruptly interrupted (as well as my master's degree haha). For anyone who wants to pursue this idea, here are a list of things we did not get to publish on the arxiv, and is not here, all summarized up:

* CCR2-CCR5 chemokine receptors likely have an evolutionary force keeping their **orientation** (direction which it is transcribed) and **intergenic distance** (base pair count between two genes) constant, and does not allow for these two to change. A quick check on animals (that have this receptor obviously) should show that this is indeed the case. Their intergenic distance, if I remember correctly, is strictly around 10k bp, which is very unusual, (we can statistically benchmark this using random pairs, random pairs from similar families, functionally relevant pairs etc.).
* This evolutionary force is not unique to CCR2-CCR5 pair, but it's rare. For this, I looked for which gene pairs are generally conserved throughout animals that have (1) same transcription direction, and (2) have a very tight intergenic distance (e.g. less than 100k bp). The latter could be extended based on transcription elongation research, I don't remember what my threshold was when doing this part. There weren't many genes like this, because common genes across a lot of animals are rare (and most animals are not at all well-studied, and data quality was a big part of the below research hitting a wall, and most of our discussions with Nir), and it's very hard to keep two genes in the same orientation and very close together. This is the main rationale behind:
* There might be some alternative splicing events happening at those locations. CCR2-CCR5 are functionally very relevant, in some specific cells they are expressed together (my wetlab experiments focused on this, but apparently wet labs are tedious and I also suck at it). Whether they are expressed as a ~fusion protein~ remains an open question, but there might be some splicing sorcery going on at these locations.
* If not, this conservation has to be explained some other way (either bad data, which is fair, bad analysis, which is also fair, or just by pure luck, which I don't buy in biology).
* *If the above interests you even the slightest bit, I'd be happy to look over my latest files and go over them with you, it is a little complicated but it shouldn't be more than a days work. Just contact me at kilic dot isildayancan \[the cool sign we use for these things\] try all the popular mail domains for US dot com, e.g. hotmail, (sorry for righting it that way, I just hate spam so so much, hint: it's the very big number).*

## Identifying proteins with multiple G-protein Coupled Receptor Domains

#### Outline

To identify proteins with multiple GPCR domains, we will be searching protein databases (e.g. UniRef90, Reference Proteomes, TremBL, Swissprot*) to find these proteins on the sequence level. To search the contents of these sequence databases, we use the [HMMER](http://eddylab.org/software/hmmer/Userguide.pdf) search tool since it is superior in many ways to other searching algorithms. To use HMMER, we need a model (hidden markovnikov model profile) of states. For a concrete GPCR example, this model would have statistical probabilities on transition states of amino acids: between TM1 and TM2 (ICL1), the probability of an insertion of 5 amino acids are much more "allowed" than to insert *intra*-TM. The ideal way to build the model is to have an alignment of proteins that are homologues, and this would tell HMMER to build a profile that reflects what is allowed and what is not allowed.

Here, we face a different problem of sequence conservation in GPCRs. Although they share this common "7 transmembrane helix", there is no obvious "strong" sequence conservation between all classses of GPCRs (albeit there are some highly-conserved motifs, but we find that the amount of them is not satisfactory). This is why we have to have separate "seeds" that represent different sets of GPCRs that have higher sequence conservation among them. If we tried to group all of them together and align them, we suspected that the signal would be averaged out and lost in the averaging process. This is why seed selection was important in the first step, and is mentioned in the following chapter. When seeds are selected, they are used to create a HMMER profile to be searched against a sequence database.

Later, a target database must be chosen for the seed profiles to be searched against. Here, we currently consider all protein databases to be good candidates for searching. In the end, our goal is to not do exhaustive search procedures as the lack of curation and other supporting data makes me believe that much of them can be false positives. As of the current procedure, we have run against UniRef90 because it is not too big (UniRef100) but still covers enough for our aims. We are thinking of searching the Reference Proteomes for taxonomic anlayses, but we will touch upon that later on.

When we have results (referred to here on out as hmmouts), we will want to parse out bad hits. These would be single GPCRs, and other proteins that are not GPCRs. We do this filtering very loosely, and only by length of a single hit, and the length of the coverage of all hits. I tried more elaborate methods on how to do this, but in the end when we focus on analyzing the outputs after grouping and clustering, filtering possible good hits out here does not make sense. Each output is first filtered for a query- and target-hit span of bigger than 150 (individual seed hits), which would be a minimal 7TM domain. Then filtered proteins get joined in a single TSV file and we look for the span of all hits, and filter out if this length is smaller than 550 (minimal diGPCR). This leaves us with candidates of multi-GPCRs that we can analyze further.

Now with the sub-database we have (candidate multi-GPCRs), we want to group and analyze them. In the initial search procedure, we decided to cluster them at 50%, and pick clusters that have more than five members. The resulting clusters didn't seem to be taxonomically consistent (proteins in clusters were sometimes too far apart in taxonomy), and I am currently omitting this clustering step but might get back to it later. Maybe a more exhaustive search would be more responsive to the clustering part. Nevertheless, we have decided to plot high-scoring pairs between seeds and the target candidate sequence to visualize the domains. On the x-axis we index the protein sequence (e.g. 900 amino acis), and we plot on the y-axis the hits between each seed and a respective amino acid in the target sequence. It looks like this.

![Figure 1](https://raw.github.com/kilicaliisildayancan/multi-GPCR/master/images/hitplot.png "Hit plots")

With some ICLs or ECLs being too long, some single GPCRs can survive through the filters and make it to the end results. These hit plots allow us to differentiate between them, and we can see an example of two false positives that passed through the filters here:

![Figure 2](https://raw.github.com/kilicaliisildayancan/multi-GPCR/master/images/falsepos-hitplot.png "False positives")

When we have finished with identifying multi-GPCR candidates, meaningful groupings must be done. For now, we are thinking of functionality (e.g. class, similarity to other known receptors), taxonomy (present in a taxonomical cluster), and GPCR count (di, tri, tetra, and poly). After this, we can analyze them further, which we can get into in another section.

Overall, My aim is to find a cluster of mGPCR proteins that are taxonomically consistent in a cluster, have high sequence similarity and have evolved to be funcitonal physiologically. And then, by proof of induction, we can say that they exist out there, and anyone interested in other possible multi-GPCRs can look back here and do what we did for their mGPCR of interest.

\*Swissprot: I personally did not expect to find a mGPCR in Swissprot since it is manually curated (also did not find any after searching). If it was there, we would have known about its existence before this project. With this in mind, we hope to find sequences in relatives of model organisms and trace them back to organisms that are represented in Swissprot and build a link between them. An important double-edged sword is the abundance and lack of data. With highly-curated organisms, we don't expect due to above-mentioned reasons, and with other organisms, there is so little experimental data that it is hard to build a convincing case that they exist.

## Emergence of Synteny: Looking at genomes for multi-domain proteins

#### CCR2-CCR5 example

#### General case; how to search for these syntenic proteins

## Verifying CCR2-CCR5 bi-chemokine GPCR in immune cells: in vitro assays

#### Plan, etc.

### Future aspects, notes, opinions

#### Caveats and limitations in methods used

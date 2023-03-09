# multi-GPCRs

Research project repositofy for identifying and analyzing multi-domain GPCRs.

## Format

#### I have written this file in a style so that everyone can read through and understand the logic and reasoning behind every step. I have written the associated/mentioned scripts next to the sub-headers so that every script is explained and contained in a title. More elaborate explanations could be in their respective directories.

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


### Searching for GPCRs using seeds

#### Seed selection

#### Strenghtening seeds (hhblits_seed-on-DB.sh)

#### Profile building (a3m-to-sto.sh, hmmbuild.sh)

#### Searching databases (hmmsearch_profiles-on-DB.sh)

### Applying "loose" filters on results

#### Pre-filtering (prefilter.py)

#### Filtering by length of span (length-filter.py)

### Identifying high-scoring hits

#### Hmmpress and hmmscan (hmmpress.sh, hmmscan_prstSeed-on-subDB.sh)

#### Parsing hits into hit vectors (hits-from-hmmscan.py)


### Visualizing the results

#### Plotting hits versus sequence indices (multiplePlots-to-PDF.py)

#### Identifying GPCR domains by hit vectors (movingAvg_hitVector.py)


### Future aspects, notes, opinions

#### Caveats and limitations in methods used

#### Communication in science

With my close-to-little experience in science and the scientific method, I am developing a very naive idea of the philosophy of science on my own. I have realized that one of the biggest pillars in science is communication. Whatever being tested is, it should be communicated well enough to be understandable and reproducable (other than being relevant and important). As a thought experiment, when discoveries are taken to the extreme, Fermat's Last Theorem comes to mind. In his "lab notebook", he stated, near his death, that he had found the proof of the conjecture "[...] I have discovered a truly marvelous proof of this, which this margin is too narrow to contain". If he ever formulated a correct proof is debated still today, while being very unlikely, this shows that communication is the most important part of scientific discoveries to not lose humanity centuries of time due to lack of pages.

This is why in my first serious scientific research, I will be extensively documenting over-arching thoughts and concepts, as well as minute details of the research procedure. Moreover, I will be going out of my way to produce understandable, interpretable, intriguing and aesthetically pleasing visuals to communicate as best what is found and what is known. This might be sub-par for other people's expectations, but I find that over the long haul the "going out of my way" part will make me one of the better communicators in science and I believe at least this thought process will be crucial for my contribution to science and human knowledge.

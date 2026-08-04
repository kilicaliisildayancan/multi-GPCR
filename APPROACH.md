# Approach and Methods

### Overview

To find multi-domain GPCR proteins computationally, we need a search pipeline. For this, we need a query, a search method, and a target (database) to search against.

The query is the protein sequence alignment of GPCRs. The search method is HMMER. The database is UniProt (very large and mostly unannotated protein databases).

We go for the low quality databases, because higher quality databases have an obvious dilemma: if it was to be found in those, they would be annotated. Thus, this "search" wouldn't be a hypothesis, but more of a confirmed case.
This dilemma is the crux of the problem of this research project. Reason being, it is very hard to prove if a protein from a low quality source exists computationally. To reason against them is easy, and this is why we are changing the approach. See [this file](./README.md).

### Steps


#### Get sequence "signature" of GPCRs (query)

GPCRs have convergent structures, although the protein sequences are not conserved across different GPCR families. If we were to use all GPCRs together, the sequence signal would disappear. This is why we use some type of clustering/grouping before the signal is extracted.
We use sequence alignment to get the conserved parts. This is the query for the search pipeline.

For this, I used the family notation as a starting point from [GPCRdb](https://gpcrdb.org).

##### Relevant files

- [GPCR families data](./scripts/search/GPCRfamilies.json)
- [Align GPCR families script](./scripts/search/family_alignment_GPCRdb.py)

#### Search against a large protein database with HMMER (search method + database)

HMMER builds statistical profiles based on states and their transitions, using "Hidden Markovnikov Models" and the sequence alignement as chains. So, once a profile is built, we can use the query (profile) to look for matches in a target database.
We build one for each family, and then search against UniRef90 (UniRef100 is huge with no cut for redundancy, 90% cut is good enough to find candidates).

##### Relevant files

- [Seeding from alignment](./scripts/search/hmmbuild_from_seedALN.sh)
- [Searching DB with HMM seed](./scripts/search/hmmsearch_profiles-on-DB.sh)

#### Filter the search result

Due to the loose approach in searching, we need to filter the results down to be able to look at "representative candidates", to show that a multi-domain GPCR exists. This candidate, with different analyses (structural, evolutionary, etc.) it is possible to build a case for the existence of these class of proteins.

The filtering is done in three discrete steps, the pre-filtering, the TM count filtering, and length filtering.
The filtering is done by counting the amount of TM domains (using a sliding window average for hyrdophobicity, since they are transmembrane), and the span of the TM domain to encompass the whole membrane (expected length is between )

##### Relevant files

- [Pre-filtering](./scripts/filtering/prefilter.py)
- [Counting transmembrane domains](./scripts/filtering/count_tms_from_hmmout.py)
- [Filtering based on length](./scripts/filtering/length-filter.py)

#### Analyze the search result

We cluster the resulting list after filtering, and look at each representative sequence of the cluster.

The look here starts with sequence, and could be anything. I didn't write scripts/documentation on this. Sorry xD.

##### Relevant files

- [CD-HIT clustering](./scripts/analysis/clustering/cluster.sh)



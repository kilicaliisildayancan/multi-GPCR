claudele did work on this, she concluded it was not a thing in high likelihood.
directory for me to go over her stuff.

email thread:

Fwd: GPCR genomic sequence
7 messages
Claudèle Lemay-St-Denis <claudele.lemay-st-denis@umontreal.ca>	Sun, Oct 13, 2024 at 10:58 AM
To: Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>


> Début du message transféré :
>
> De: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
> Objet: Rép : GPCR genomic sequence
> Date: 13 octobre 2024 à 10:20:35 UTC+3
> À: Nir Ben-Tal <bental@tauex.tau.ac.il>
> Cc: Rachel Kolodny <trachel@gmail.com>
>
> Hi Nir and Rachel,
>
> I agree that focusing on members from the most populated clusters is a valuable approach to gather more data on the genomic regions encoding mGPCR. Below is a summary of this analysis.
>
> For the five mGPCR members with the highest species diversity, I retrieved their homologues previously identified by Rachel. These members were from clusters 2 and 3, as outlined in Table S1 of the 2022 manuscript. Additionally, I retrieved homologues from one member of cluster 1, which contains chemokine receptors and is therefore of particular scientific importance. I organized these homologues into clusters for ease of reference and to examine potential conservation of the intron/exon structure within each cluster. In total, I was able to retrieve genomic sequences for 22 of the 23 homologues from cluster 1, 139 of the 243 from cluster 2, and 138 of the 258 from cluster 3. Given that some homologues are shared between clusters 2 and 3, 231 unique genomic contexts were ultimately analyzed.
>
> I’ve attached PDFs with the same exon/intron presentation format as before. Notably, none of the mGPCRs are encoded by a single exon; they all result from splicing between distant exons. The shortest intron length observed was 157 bp (UPI0018790F19), while most introns were well over 2 kb. One notable case (UPI0015528699) had an intron exceeding 100 kb, which is a thousand times longer than the typical intron length. There also doesn’t appear to be any consistent conservation in the genomic coding regions within each cluster, as both the number of exons and intron lengths vary between homologues.
>
> The variability/randomness in splicing predicted by the gene prediction algorithm could help explain the lack of conservation observed in the interdomain regions of the mGPCR data set. This variability and the prediction of long introns may point to a limitation in the gene prediction algorithm used by NCBI. It could be worthwhile for the team responsible for the prediction pipeline to investigate whether an adjustment—such as imposing an intron length limit or introducing a cost factor for excessively long introns—might improve accuracy of predicted proteins.
>
> On a separate note, I was wondering if I could do some daily visits at TAU, given that the University of Haifa is temporarily closed. I heard there were office renovations due to asbestos removal—are things back to normal?
>
> Looking forward to your thoughts,
> Claudèle
>



>
>> Le 9 oct. 2024 à 10:33, Nir Ben-Tal <bental@tauex.tau.ac.il> a écrit :
>>
>> Hi Claudele,
>>  
>> Thank you for this meticulous and insightful analysis. Maybe what we found is an artefact. Perhaps all we found was just pairs of GPCRs that should interact with each other and are therefore in close vicinity in the genome.
>>  
>> Each of the 57 representatives should correspond to at least 5 different instances. Rachel has this data. It would be helpful to look at the genomic context of the other instances. Maybe you could start with the largest cluster. That is, the representative that was observed most frequently. Maybe at least one of the instances will have a reasonably short intron?
>>  
>> Best,
>>  
>> Nir
>>  
>> From: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
>> Sent: יום ג 08 אוקטובר 2024 15:12
>> To: Nir Ben-Tal <bental@tauex.tau.ac.il>; Rachel Kolodny <trachel@gmail.com>
>> Subject: GPCR genomic sequence
>>  
>> Hi Nir and Rachel,
>>  
>> I’ve been reviewing the multi-GPCR dataset to better understand its structure, particularly the genomic context of the multi-GPCR gene predictions. I wanted to briefly share my findings regarding the coding regions of the multi-GPCRs.
>>  
>> It appears that the multi-GPCRs consist of at least two exons with inter-exon distances (intron lengths) ranging from 3 kb to 49 kb. Gene prediction algorithms have grouped separate GPCR chains—encoded by distinct exons—into a single protein. However, the unusually long intron lengths of these genes (several thousand base pairs, whereas most introns reported in the literature are in the range of dozens to hundreds of base pairs) raise questions about the validity of these gene predictions. It seems that distinct GPCR genes, which are often found in clusters, may have been mistakenly predicted as a single chain.
>>  
>> For the 57 multi-GPCRs reported in the 2022 preprint, I’ve extracted their genomic regions and mapped the context. Notably, 15 proteins have been removed from UniProt, and three others are no longer associated with proteins in NCBI. I’ve attached a PDF with the coding sequences for the remaining 39 multi-GPCRs. At least two of these have been reannotated and no longer contain multiple GPCR domains.
>>  
>> In the PDF, each multi-GPCR’s exons are highlighted in different colors for clarity. The number of exons and their genomic lengths are shown at the top right of each graph. Exons coding for more than 100 amino acids are marked in green, and intron lengths greater than 2 kb are highlighted in red.
>>  
>> Perhaps we could discuss these observations further? I’m pretty flexible, so just let me know when would be a good time for you.
>>  
>> Best regards and stay safe,
>> Claudèle
>



3 attachments
		cluster1_ids2.pdf
40K
		cluster2_id2.pdf
120K
		cluster3_id2.pdf
112K
Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>	Wed, Oct 16, 2024 at 3:34 PM
To: Nir Ben-Tal <bental@tauex.tau.ac.il>
Cc: Rachel Kolodny <trachel@gmail.com>, Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>
Hi Nir,

I agree that the species is an important aspect. When I looked at the accessible genomic information for the species in the dataset, many only had a reference genome on NCBI from which the mGPCR was predicted. This means that many are species for which we have no or limited information on their intron organization or splicing characteristics, which further limits us. 

For L9KKE8: that's also possible!

I think it's a good idea, I'm adding Kilic here. I've discussed these results with him, so he's up to date. It is an exciting hypothesis, that would welcome data at the transcript level to investigate further. Kilic, maybe you have other relevant things to add to what we are discussing here?

Sounds good, I'll see with them! I think David might be home - he asked me to tell him when I'm going to the lab, he'll try to join us.

Cheers,
Claudèle

> Le 16 oct. 2024 à 15:06, Nir Ben-Tal <bental@tauex.tau.ac.il> a écrit :
>
> Hi Claudele,
>  
> Thank you for the quite and very informative reply. Based on your literature survey it looks like we should calibrate the results to the species. I mean, maybe a 2 KBP intron is acceptable (with low likelihood) in one species but virtually impossible in another species. Again, the easiest solution is that all we see are artefacts, even though we see them multiple times. We should discuss it further.
>  
> The excessively high similarity in L9KKE8: Maybe it means sequencing error?...
>  
> At the time, Kilic was trying to make a case for alternative splicing. In particular, for the chemokine receptor he focused on, that maybe the dominant version is of two separated receptors 2 and 5. But that a low fraction comes with a splice variant with 2 and 5 combined into a single chain.
>  
> Would you like to get him involved in the exchange?
>  
> And yes, do talk with Mazy about a visit. Maybe Amit would like to also join. I think that David is in the army. But maybe he is back by now.  
>  
> Best,
>  
> Nir
>  
> From: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
> Sent: יום ד 16 אוקטובר 2024 13:58
> To: Nir Ben-Tal <bental@tauex.tau.ac.il>
> Cc: Rachel Kolodny <trachel@gmail.com>
> Subject: Re: GPCR genomic sequence
>  
> Hi Nir,
>  
> Great! I’ll coordinate with Mazi and David so that we can meet at the lab!
>  
> To address your questions:
> - The distance between the two exons in L9KKE8 is 528 bp, which is noticeably shorter than most of the introns in the dataset.
>  
> - Regarding UPI00094E866C, yes, the predicted structure does show two domains. I’m attaching the predicted AF3 structure along with the error graph. It seems that the splicing of the two exons in the first domain could explain the lower confidence score in the middle of that domain. The intron between the two domains is 1518 bp long.
>  
>  - UPI0010A3B28B is a four-domain GPCR, and the intron lengths between the four exons are 2945 bp, 1853 bp, and 1436 bp, from left to right according to the exon plot.
>  
> I’ve also taken a closer look at intron lengths in the literature. While most introns tend to be short (40-125 bp, as mentioned in this paper), some can be exceptionally long. For example, in one study, they discuss a human gene where five of the exons are over 100 kb in length. Intron length and presence/absence seem to vary significantly by species. For instance, the median intron length is reported here to be 68 bp in Drosophila, but 1334 bp in humans. In short, long introns (dozens of thousands of base pairs) are certainly documented, though they’re less common.
>  
> As a quick test, I used Augustus to predict the genes corresponding to UPI0010A3B28B (the four-domain GPCR), and it predicted four distinct proteins, each with a single GPCR domain per chain. For L9KKE8, it also predicted a two-domain GPCR, with a slightly longer interdomain region. Interestingly, the two domains in L9KKE8 share 100% identity over 309 residues, possibly suggesting recent gene duplication?
>  
> Perhaps it would be worth discussing this further?
>  
> Best,
> Claudèle
>  
> image001.png
>
>
>     Le 16 oct. 2024 à 00:33, Nir Ben-Tal <bental@tauex.tau.ac.il> a écrit :
>      
>     Hi Claudele,
>      
>     I’m curious about L9KKE8 in cluster 1. The two GPCRs seem rather close to each other. Right? Maybe 100 base pairs?
>      
>     And UPI00094E866C in cluster 2. Does it have 2 complete GPCRs? The right one seem to combine 2 exons, right? If so, the distance between the 2 GPCRs is a little over 1000 base pairs, right? Too much for translation as a single chain?
>      
>     UPI0010A3B28B in cluster 2 is also interesting. The right-most GPCRs seem to be about 1000 base pairs away from each other.
>      
>     Do you happen to know what is the length of longest recorded intron within a properly translated protein? We need this for calibration.
>      
>     I didn’t go over cluster 3 thoroughly yet.
>      
>     Best,
>      
>     Nir
>      
>      
>      
>     From: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
>     Sent: יום א 13 אוקטובר 2024 10:21
>     To: Nir Ben-Tal <bental@tauex.tau.ac.il>
>     Cc: Rachel Kolodny <trachel@gmail.com>
>     Subject: Re: GPCR genomic sequence
>      
>     Hi Nir and Rachel,
>      
>     I agree that focusing on members from the most populated clusters is a valuable approach to gather more data on the genomic regions encoding mGPCR. Below is a summary of this analysis.
>      
>     For the five mGPCR members with the highest species diversity, I retrieved their homologues previously identified by Rachel. These members were from clusters 2 and 3, as outlined in Table S1 of the 2022 manuscript. Additionally, I retrieved homologues from one member of cluster 1, which contains chemokine receptors and is therefore of particular scientific importance. I organized these homologues into clusters for ease of reference and to examine potential conservation of the intron/exon structure within each cluster. In total, I was able to retrieve genomic sequences for 22 of the 23 homologues from cluster 1, 139 of the 243 from cluster 2, and 138 of the 258 from cluster 3. Given that some homologues are shared between clusters 2 and 3, 231 unique genomic contexts were ultimately analyzed.
>      
>     I’ve attached PDFs with the same exon/intron presentation format as before. Notably, none of the mGPCRs are encoded by a single exon; they all result from splicing between distant exons. The shortest intron length observed was 157 bp (UPI0018790F19), while most introns were well over 2 kb. One notable case (UPI0015528699) had an intron exceeding 100 kb, which is a thousand times longer than the typical intron length. There also doesn’t appear to be any consistent conservation in the genomic coding regions within each cluster, as both the number of exons and intron lengths vary between homologues.
>      
>     The variability/randomness in splicing predicted by the gene prediction algorithm could help explain the lack of conservation observed in the interdomain regions of the mGPCR data set. This variability and the prediction of long introns may point to a limitation in the gene prediction algorithm used by NCBI. It could be worthwhile for the team responsible for the prediction pipeline to investigate whether an adjustment—such as imposing an intron length limit or introducing a cost factor for excessively long introns—might improve accuracy of predicted proteins.
>      
>     On a separate note, I was wondering if I could do some daily visits at TAU, given that the University of Haifa is temporarily closed. I heard there were office renovations due to asbestos removal—are things back to normal?
>      
>     Looking forward to your thoughts,
>     Claudèle
>      
>
>
>
>         Le 9 oct. 2024 à 10:33, Nir Ben-Tal <bental@tauex.tau.ac.il> a écrit :
>          
>         Hi Claudele,
>          
>         Thank you for this meticulous and insightful analysis. Maybe what we found is an artefact. Perhaps all we found was just pairs of GPCRs that should interact with each other and are therefore in close vicinity in the genome.
>          
>         Each of the 57 representatives should correspond to at least 5 different instances. Rachel has this data. It would be helpful to look at the genomic context of the other instances. Maybe you could start with the largest cluster. That is, the representative that was observed most frequently. Maybe at least one of the instances will have a reasonably short intron?
>          
>         Best,
>          
>         Nir
>          
>         From: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
>         Sent: יום ג 08 אוקטובר 2024 15:12
>         To: Nir Ben-Tal <bental@tauex.tau.ac.il>; Rachel Kolodny <trachel@gmail.com>
>         Subject: GPCR genomic sequence
>          
>         Hi Nir and Rachel,
>          
>         I’ve been reviewing the multi-GPCR dataset to better understand its structure, particularly the genomic context of the multi-GPCR gene predictions. I wanted to briefly share my findings regarding the coding regions of the multi-GPCRs.
>          
>         It appears that the multi-GPCRs consist of at least two exons with inter-exon distances (intron lengths) ranging from 3 kb to 49 kb. Gene prediction algorithms have grouped separate GPCR chains—encoded by distinct exons—into a single protein. However, the unusually long intron lengths of these genes (several thousand base pairs, whereas most introns reported in the literature are in the range of dozens to hundreds of base pairs) raise questions about the validity of these gene predictions. It seems that distinct GPCR genes, which are often found in clusters, may have been mistakenly predicted as a single chain.
>          
>         For the 57 multi-GPCRs reported in the 2022 preprint, I’ve extracted their genomic regions and mapped the context. Notably, 15 proteins have been removed from UniProt, and three others are no longer associated with proteins in NCBI. I’ve attached a PDF with the coding sequences for the remaining 39 multi-GPCRs. At least two of these have been reannotated and no longer contain multiple GPCR domains.
>          
>         In the PDF, each multi-GPCR’s exons are highlighted in different colors for clarity. The number of exons and their genomic lengths are shown at the top right of each graph. Exons coding for more than 100 amino acids are marked in green, and intron lengths greater than 2 kb are highlighted in red.
>          
>         Perhaps we could discuss these observations further? I’m pretty flexible, so just let me know when would be a good time for you.
>          
>         Best regards and stay safe,
>         Claudèle
>
>  

Nir Ben-Tal <bental@tauex.tau.ac.il>	Wed, Oct 16, 2024 at 3:46 PM
To: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
Cc: Rachel Kolodny <trachel@gmail.com>, Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>

Hi Claudele,

 

Thank you for getting Kilic also involved.

 

Kilic, how are you?
[Quoted text hidden]



    [Quoted text hidden]
    [Quoted text hidden]

    [Quoted text hidden]

 
Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>	Fri, Oct 18, 2024 at 7:06 PM
To: Nir Ben-Tal <bental@tauex.tau.ac.il>, Claudèle Lemay-St-Denis <claudele.lemay-st-denis@umontreal.ca>
Hi Nir (and Claudèle),

I'm all good, and from looking at the news recently I hope you both are also doing well and you don't get affected too too much.

How are you doing? How is everything going with the war? I hope you don't get arrested anymore and science takes your mind off of everything.

Best,
Kilic
[Quoted text hidden]
Nir Ben-Tal <bental@tauex.tau.ac.il>	Fri, Oct 18, 2024 at 8:05 PM
To: Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>, Claudèle Lemay-St-Denis <claudele.lemay-st-denis@umontreal.ca>

Hi Kilic,

 

Currently Lilach and I are on vacation in a particularly beautiful boutique hotel in the dolomite mountains. But when I’m in Israel I protest a lot. And get arrested every now and then😊.

 

I hope that the war and excessive killing on both sides will end soon and hostages returned. At least those who are still alive.

 

Best,

 

Nir
[Quoted text hidden]
Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>	Wed, Aug 5, 2026 at 8:12 AM
To: Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>

Envoyé de mon iPhone

Début du message transféré :

> De: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
> Date: 16 octobre 2024 à 13:57:48 UTC+3
> À: Nir Ben-Tal <bental@tauex.tau.ac.il>
> Cc: Rachel Kolodny <trachel@gmail.com>
> Objet: Rép : GPCR genomic sequence
>
> ﻿
> Hi Nir,
>
> Great! I’ll coordinate with Mazi and David so that we can meet at the lab!
>
> To address your questions:
> - The distance between the two exons in L9KKE8 is 528 bp, which is noticeably shorter than most of the introns in the dataset.
>
> - Regarding UPI00094E866C, yes, the predicted structure does show two domains. I’m attaching the predicted AF3 structure along with the error graph. It seems that the splicing of the two exons in the first domain could explain the lower confidence score in the middle of that domain. The intron between the two domains is 1518 bp long.
>
>  - UPI0010A3B28B is a four-domain GPCR, and the intron lengths between the four exons are 2945 bp, 1853 bp, and 1436 bp, from left to right according to the exon plot.
>
> I’ve also taken a closer look at intron lengths in the literature. While most introns tend to be short (40-125 bp, as mentioned in this paper), some can be exceptionally long. For example, in one study, they discuss a human gene where five of the exons are over 100 kb in length. Intron length and presence/absence seem to vary significantly by species. For instance, the median intron length is reported here to be 68 bp in Drosophila, but 1334 bp in humans. In short, long introns (dozens of thousands of base pairs) are certainly documented, though they’re less common.
>
> As a quick test, I used Augustus to predict the genes corresponding to UPI0010A3B28B (the four-domain GPCR), and it predicted four distinct proteins, each with a single GPCR domain per chain. For L9KKE8, it also predicted a two-domain GPCR, with a slightly longer interdomain region. Interestingly, the two domains in L9KKE8 share 100% identity over 309 residues, possibly suggesting recent gene duplication?
>
> Perhaps it would be worth discussing this further?
>
> Best,
> Claudèle
>
> Capture d’écran, le 2024-10-16 à 09.56.15.png
> [Quoted text hidden]
Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>	Wed, Aug 5, 2026 at 8:13 AM
To: Kilicali ISILDAYANCAN <kilic.isildayancan@gmail.com>
With the files
Envoyé de mon iPhone

Début du message transféré :

> De: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
> Date: 13 octobre 2024 à 10:20:48 UTC+3
> À: Nir Ben-Tal <bental@tauex.tau.ac.il>
> Cc: Rachel Kolodny <trachel@gmail.com>
> Objet: Rép : GPCR genomic sequence
>
> ﻿
> [Quoted text hidden]



>
>> Le 9 oct. 2024 à 10:33, Nir Ben-Tal <bental@tauex.tau.ac.il> a écrit :
>>
>> Hi Claudele,
>>  
>> Thank you for this meticulous and insightful analysis. Maybe what we found is an artefact. Perhaps all we found was just pairs of GPCRs that should interact with each other and are therefore in close vicinity in the genome.
>>  
>> Each of the 57 representatives should correspond to at least 5 different instances. Rachel has this data. It would be helpful to look at the genomic context of the other instances. Maybe you could start with the largest cluster. That is, the representative that was observed most frequently. Maybe at least one of the instances will have a reasonably short intron?
>>  
>> Best,
>>  
>> Nir
>>  
>> From: Claudèle Lemay-St-Denis <claudele.lemaystdenis@gmail.com>
>> Sent: יום ג 08 אוקטובר 2024 15:12
>> To: Nir Ben-Tal <bental@tauex.tau.ac.il>; Rachel Kolodny <trachel@gmail.com>
>> Subject: GPCR genomic sequence
>>  
>> Hi Nir and Rachel,
>>  
>> I’ve been reviewing the multi-GPCR dataset to better understand its structure, particularly the genomic context of the multi-GPCR gene predictions. I wanted to briefly share my findings regarding the coding regions of the multi-GPCRs.
>>  
>> It appears that the multi-GPCRs consist of at least two exons with inter-exon distances (intron lengths) ranging from 3 kb to 49 kb. Gene prediction algorithms have grouped separate GPCR chains—encoded by distinct exons—into a single protein. However, the unusually long intron lengths of these genes (several thousand base pairs, whereas most introns reported in the literature are in the range of dozens to hundreds of base pairs) raise questions about the validity of these gene predictions. It seems that distinct GPCR genes, which are often found in clusters, may have been mistakenly predicted as a single chain.
>>  
>> For the 57 multi-GPCRs reported in the 2022 preprint, I’ve extracted their genomic regions and mapped the context. Notably, 15 proteins have been removed from UniProt, and three others are no longer associated with proteins in NCBI. I’ve attached a PDF with the coding sequences for the remaining 39 multi-GPCRs. At least two of these have been reannotated and no longer contain multiple GPCR domains.
>>  
>> In the PDF, each multi-GPCR’s exons are highlighted in different colors for clarity. The number of exons and their genomic lengths are shown at the top right of each graph. Exons coding for more than 100 amino acids are marked in green, and intron lengths greater than 2 kb are highlighted in red.
>>  
>> Perhaps we could discuss these observations further? I’m pretty flexible, so just let me know when would be a good time for you.
>>  
>> Best regards and stay safe,
>> Claudèle

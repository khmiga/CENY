# CENY

This repository contains the scripts used for the CENY paper. The steps for generating full-length consensus sequences for the BACs are:

1. Extract fastq sequences using poretools (http://poretools.readthedocs.io/en/latest/). Poretools can be used to extract reads between a certain length range (e.g. between 150 kb and 200 kb length). These reads represent full-length BAC seqeunces.

2. Align these full-length reads to the vector sequence using BLASR (https://github.com/ylipacbio/blasrbinary) and parameters (-sdpTupleSize 8 -bestn 1 -nproc 8 -m 0). This will produce alignments to the vector sequence in text format.

3. You can filter the blasr alignment file to a new text file that contains just the basic metadat on every alignment (e.g. start and end coordinates, etc.). To do this, a simple grep would work (e.g. grep -A 8 -B 6 "Query:" reads.blasr).

4. Using the blasr_output.py script, reorient these reads such that all of them start with the vector sequence. Additionally, this script ensures that all reads are in one orientation (since multiple sequence alignment cares about read orientation). Lastly, the default settings in the script look for a > 3 kb long alignment to the vector sequence at  either end. This is our way of ensuring a second time that the reads being fed to an MSA are all full-length. (python blasr_output.py reads.blasr reads.fasta > reoriented.fa)

5. Now randomly sample 60 reads from the reoriented reads, and do an MSA using kalign (http://msa.sbc.su.se/cgi-bin/msa.cgi).

6. Next, we compute the consensus using a custom script (kaln2CNS.pl)

7. Repeat steps 5 and 6, 10 times (10 iterations). This will generate 10 consensus sequences.

8. Now perform a final MSA on these 10 consensus sequences using kalign and generate a final consensus. This is the consensus sequence for the BAC to be used downstream.

9. We then performed an alignment of all the reoriented reads against the final consensus and then parsed the alignments using pysamstats (https://github.com/alimanfoo/pysamstats). This allowed us to perform a sequence-level polishing, thus reducing alignment-artifcats in the consensus sequence that would have arisen from single-base insertions.

This repository will be updated in the days to come with cleaner scripts, and a streamlined pipeline. 

The work we present here is described in the following bioRxiv: http://www.biorxiv.org/content/early/2017/07/31/170373


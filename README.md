# Bioinformatics Algorithms

Set of three commands, each with applications to DNA sequence analysis

- [FASTQ Percent Nucleotides Greater than Length](#fastq-percent-nucleotides-greater-than-length)
- [FASTA Top-Occurring Sequences](#fasta-top-occurring-sequences)
- [Annotate Gene Names](#annotate-gene-names)

## Installing

- Clone repository
- `cd my_cloned_dir`

## Run Tests
- `python -m unittest tests.annotation_tests tests.fastq_nt_len_tests tests.seq_mode_tests`

## Commands

### FASTQ Percent Nucleotides Greater than Length

Takes as input base directory and optional nucleotide length (`-l` or `--length`), default is 30 if not specified. Returns list of FASTQ files recursively found from base directory and the percent of nucleotide sequences greater than the requested length in each successive file.

Example command:
- `./commands/fastq_nt_gt_len.py ./sample_files/` matches on sequences > 30
- `./commands/fastq_nt_gt_len.py ./sample_files/ --length=35` matches on sequences > 35
- `./commands/fastq_nt_gt_len.py --help` for command line help text

Example output:

`./sample_files/fastq/read1/Sample_R1.fastq	79.4590025359`

`./sample_files/fastq/read2/Sample_R2.fastq	82.8402366864`

### FASTA Top-Occurring Sequences

Takes as input path to FASTA file and optional specification for how many of the top-occurring sequences to return, default is 10 if not specified (or however many results exist if fewer). Returns the top-occurring sequences along with the number of occurrences. Handles single sequences split across multiple lines.

Example command:
- `./commands/seq_mode.py ./sample_files/fasta/sample.fasta` returns top 10
- `./commands/seq_mode.py ./sample_files/fasta_sample.fasta -n 15`  returns top 15
- `./commands/seq_mode.py --help` for command line help text

Example output:

`CGCGCAGGCTGAAGTAGTTACGCCCCTGTAAAGGAATCTATGGACAATGGAACGAACA	28`

`TGTTCTGAGTCAAATGATATTAACTATGCTTATCACATATTATAAAAGACCGTGGACATTCATCTTTAGTGTGTCTCCCTCTTCCTACT	27`

`CTCAATCTGCCAAGACCATAGATCCTCTCTTACTGTCAGCTCATCCGGTGAGGCC	22`

`CCTGTTGCTGACTCAAGACATTAGTGAGAAATAAGACTTCTGCGATGCTCACCACTGCAATTGCTCATGCAAAATTGCGTTTAACAGG	21`

`TTTCAGCTGTCTTTTAAGCAGAAGCGATTTGTCCAACAAAAACAACGCTGTTTACGAA	17`

`ATTGCGAATTCCGCCTGTGTCCCCCACACGAGCGTGAATCGTGGCTAGAAGTTCAGCCCCTCTTAGCACAGAGTGAG	17`

`GACACAAACACCGTGGCTCAACCTAATCCTATTAGAGCCGAAAAGGCGAGGATGCTGATTGAGTAGGTATCTGGA	8`

`TCACGCAGACAACGAACTGTGTCTGGATCAAAGACATCCGATAAGGCGATTCGTCTAGAAGGGTTACACAGTTGGGACCGGTAG	8`

`TGCTTAAACTCATGATAGTCCCTGAGTAAACTGGTTGCGACACGGCTCCCG	5`

`TGTGCAGAATATAATGTAAAAAAAACAGGACCCGGCTCTGTGCCGTTGGCCTGCGCGGTACTCATGTTAGTTTTCCGACTCCGACTTAT	5`

### Annotate Gene Names

Takes as input both a path to file listing chromosome/coordinate pairs and a path to GTF annotation file. Returns tab-separated list of chromosome. coordinate, and annotated gene name if found.

Example command:
- `./commands/get_annotations.py ./sample_files/annotate/coordinates_to_annotate.txt ./sample_files/gtf/hg19_annotations_shortened.gtf`
- `./commands/get_annotations.py --help` for command line help text

Example output:

- Note: using the command above will not yield these results below, as `hg_annotations_shortened.gtf` has been significantly reduced from the original `hg_annotations.gtf` due to GitHub file size restrictions

`chr12	20704380	PDE3A`

`chr12	20704379	PDE3A`

`chr21	9827238	NO-ANNOTATION`

`chr5	71146882	NO-ANNOTATION`

`chr8	38283717	FGFR1`

`chr12	20704371	PDE3A`

`chr12	20704377	PDE3A`

`chr21	9827364	NO-ANNOTATION`

`chr4	184083607	WWC2`

`chr11	85195011	DLG2`

`...`

### Coding Time

Completed in 11 hours between hours of Friday at 4:09pm and Saturday at 5:00pm

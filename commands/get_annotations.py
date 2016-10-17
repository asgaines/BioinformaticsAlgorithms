#!/usr/bin/env python

import argparse
from structures.tree import GeneTree

task = '''
Annotate Gene Names.

Given a chromosome and coordinates, return the gene name
annotated alongside coordinates.

Input: 
Tab-delimited file: Chr<tab>Position. 
GTF formatted file with genome annotations.

Output: 
Annotated file of gene name that input position overlaps.
'''

# I am taking the directions to indicate a requested 1:1 response 
# to the coordinate input file, returning the original 
# chromosome and coordinate for convenience, with only 
# the name of the gene as annotation.

# If this is incorrect and more information is required for the 
# annotation, I would be happy to modify the code

# It first creates a cache of chromosomes loaded with
# genes of introns/exons linked together into a single
# continuous gene, dropping all data except for the gene name,
# and the start/stop coordinates. It then finds the gene name
# of the overlap region or returns an indication
# of the gene not being found

# Returned when a chromosome|coordinate pair does not match records
NOT_FOUND_MESSAGE = 'NO-ANNOTATION'

def cache_chromosomes(filename):
    '''
    Iterates through GTF file and splits data hierarchically according to 
    chromosome, then gene name within chromosome
    '''

    chromosomes = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                data = line.split()

                chromosome = data[0]
                gene_start_pos = int(data[3])
                gene_stop_pos = int(data[4])
                gene_name = data[9].rstrip(';').strip('"')

                if chromosomes.get(chromosome):
                    if chromosomes.get(chromosome).get(gene_name):
                        # This gene has been encountered previously
                        # Extend gene's former start/stop coordinates with the newly 
                        # encountered additional section.
                        # Handles case where single gene broken across lines with
                        # other gene interspersed, and out of order
                        former_start_pos, former_stop_pos = chromosomes[chromosome][gene_name]
                        chromosomes[chromosome][gene_name][0] = min(gene_start_pos, former_start_pos)
                        chromosomes[chromosome][gene_name][1] = max(gene_stop_pos, former_stop_pos)
                    else:
                        chromosomes[chromosome][gene_name] = [gene_start_pos, gene_stop_pos]
                else:
                    chromosomes[chromosome] = {gene_name: [gene_start_pos, gene_stop_pos]}
        # Convert genes into balanced binary tree
        # Performed now, tree will be balanced; not
        # guaranteed if genes loaded individually
        return convert_binary_tree(chromosomes)
    except IOError:
        exit('Please provide a valid file')

def convert_binary_tree(chromosomes):
    '''
    Takes chromosome hash table, converting list of genes into binary tree
    '''
    for chromosome in chromosomes.keys():
        genes_sorted = sorted([[gene, chromosomes[chromosome][gene][0], chromosomes[chromosome][gene][1]] for gene in chromosomes[chromosome].keys()], key=lambda g: g[1])
        chromosomes[chromosome] = GeneTree.init_from_sorted_genes(genes_sorted)
    return chromosomes

def find_overlap(chromosome, coordinate, chromosomes):
    '''
    Takes chromosome|coordinate pair and returns gene name
    if coordinate located in binary tree
    '''

    if chromosome in chromosomes.keys():
        gene = chromosomes[chromosome].find(coordinate)
        if gene:
            return gene.get_name()

def match_coords(coord_filename, chromosomes):
    '''
    Iterates through coordinate file, handing data to `find_overlap`
    and returning the results
    '''

    with open(coord_filename, 'r') as f:
        for line in f:
            chromosome, coordinate = line.split()
            coordinate = int(coordinate)
            overlap = find_overlap(chromosome, coordinate, chromosomes)
            annotation = overlap if overlap else NOT_FOUND_MESSAGE
            yield '\t'.join(map(str, [chromosome, coordinate, annotation]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=task)
    parser.add_argument('coord_file', help='Path to coordinate file')
    parser.add_argument('anno_file', help='Path to annotation file, GTF formatted')
    args = parser.parse_args()

    # Create cache of chromosomes from annotation file
    chromosomes = cache_chromosomes(args.anno_file)
    
    for result in match_coords(args.coord_file, chromosomes):
        print(result)


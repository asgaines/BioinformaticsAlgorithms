#!/usr/bin/env python

import sys
import argparse

DEFAULT_NUM_SEQS = 10

task = '''
FASTA Top Occurring Sequences.

Given a FASTA file with DNA sequences, find `num_seqs` most frequent 
sequences (the sequence modes) and return the sequence and their 
counts in the file. Default top sequences is {num_seqs}
'''.format(num_seqs=DEFAULT_NUM_SEQS)

def hash_file(filename):
    '''
    Returns a newly created hash table of the sequences with
    the number of occurrences
    '''

    seq = ''
    seq_hash = {}

    try:
        with open(filename, 'r') as f:
            for line in f:
                if line[0] == '>':  # Beginning of new sequence
                    if seq:
                        if seq_hash.get(seq):
                            seq_hash[seq] += 1
                        else:
                            seq_hash[seq] = 1
                    # Start of new sequence, reset accumulator
                    seq = ''
                else:
                    # In case sequences broken apart multiple lines,
                    # accumulate raw sequence until next new sequence begins
                    seq += line.strip()

        # Add final sequence at end of file
        if seq_hash.get(seq):
            seq_hash[seq] += 1
        else:
            seq_hash[seq] = 1
    except IOError:
        exit('Please specify a valid FASTA file')

    return seq_hash

def get_top_sequences(seq_hash, num_seqs):
    '''
    Returns the top-occurring sequences from the sequence hash table
    '''

    # Loop through a sorted list of the otherwise unsorted hashed data
    for seq in sorted(seq_hash, key=seq_hash.get, reverse=True)[:num_seqs]:
        yield '\t'.join(map(str, [seq, seq_hash[seq]]))


if __name__ == '__main__':
    # There is a nice Biopython parser I would use if third-party
    # libraries were not out-of-bounds
    parser = argparse.ArgumentParser(description=task)
    parser.add_argument('filename', help='Path to FASTA file')
    parser.add_argument('-n', '--num_seqs', type=int,
        help='Number of top results to return. Defaults to {num_seqs}'.format(num_seqs=DEFAULT_NUM_SEQS)
    )
    args = parser.parse_args()

    seqs_hashed = hash_file(args.filename)
    for seq in get_top_sequences(seqs_hashed, args.num_seqs or DEFAULT_NUM_SEQS):
        print(seq)

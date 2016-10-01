#!/usr/bin/env python

import sys
import os
import fnmatch
import argparse

NT_DEFAULT_LENGTH = 30

task = '''
FASTQ Percent Nucleotides Greater than Length.

Recursively find all FASTQ files starting from `base_dir` and 
report each file name and the percent of sequences in that file 
that are greater than `length` nucleotides long (default={default_len}).
'''.format(default_len=NT_DEFAULT_LENGTH)

def get_files(base_dir):
    '''
    Recursively walk deeper into the directory.
    I was unsure of the status of this being third-party
    I would be happy to implement the logic for this 
    recursive search upon request
    '''

    for root, dirnames, filenames in os.walk(base_dir):
        for filename in fnmatch.filter(filenames, '*.fastq'):
            yield os.path.join(root, filename)

def get_perc_gt_len(filename, nt_len):
    '''
    Calculate and return the percent of sequences greater
    than the requested nucleotide length
    '''

    seq_total = 0  # Accumulator for all sequences
    seq_gt_len = 0  # Accumulator for sequences greater than `nt_len`

    with open(filename, 'r') as f:
        while True:
            # Read 4 lines at a time, as per FASTQ specifications
            seq_identifier = f.readline()
            raw_seq = f.readline()
            quality_identifier = f.readline()
            quality_scores = f.readline()

            if not seq_identifier:
                # End of file reached
                if not seq_total:
                    return 0.0
                return float(seq_gt_len) / seq_total * 100

            if len(raw_seq) > nt_len:
                seq_gt_len += 1
            seq_total += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=task)
    parser.add_argument('base_dir', help='Base directory from which recursive search begins')
    parser.add_argument('-l', '--length', type=int, 
        help='Filter nucleotides greater than length. Defaults to {default_len}'.format(default_len=NT_DEFAULT_LENGTH)
    )

    args = parser.parse_args()

    nt_len = args.length or NT_DEFAULT_LENGTH

    for filename in get_files(args.base_dir):
        print('\t'.join(map(str, [filename, get_perc_gt_len(filename, nt_len)])))


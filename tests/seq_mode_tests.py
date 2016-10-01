import unittest

from commands import seq_mode

class TestSequenceMode(unittest.TestCase):
    def setUp(self):
        self.fasta_files = [
            './tests/test_files/fasta/test_1.fasta',  # Top sequence = 5 count
            './tests/test_files/fasta/test_2.fasta',  # Sequences split across multiple lines
            './tests/test_files/fasta/test_3.fasta',  # Only 2 distinct sequences
        ]

    def test_get_top_sequences_returns_correct_num_seqs(self):
        # Default 10
        num_results = 10
        hashed_seqs = seq_mode.hash_file(self.fasta_files[0])
        results = seq_mode.get_top_sequences(hashed_seqs, num_results)
        self.assertEqual(sum(1 for r in results), num_results)

        # Altered amount
        num_results = 5
        hashed_seqs = seq_mode.hash_file(self.fasta_files[0])
        results = seq_mode.get_top_sequences(hashed_seqs, num_results)
        self.assertEqual(sum(1 for r in results), num_results)

    def test_get_top_sequences_returns_max_num_sequences_fewer_than_requested(self):
        hashed_seqs = seq_mode.hash_file(self.fasta_files[2])
        results = seq_mode.get_top_sequences(hashed_seqs, 10)
        self.assertEqual(sum(1 for r in results), 2)

    def test_get_top_sequences_returns_top_result_first(self):
        hashed_seqs = seq_mode.hash_file(self.fasta_files[0])
        results = seq_mode.get_top_sequences(hashed_seqs, 10)
        self.assertEqual(int(next(results).split()[1]), 5)

    def test_hash_file_joins_split_data(self):
        hashed_seqs = seq_mode.hash_file(self.fasta_files[1])
        self.assertEqual(len(hashed_seqs), 1)

    def test_hash_file_has_proper_count(self):
        hashed_seqs = seq_mode.hash_file(self.fasta_files[1])
        self.assertEqual(hashed_seqs.get(hashed_seqs.keys()[0]), 2)

    def test_fails_on_incorrect_file(self):
        with self.assertRaises(SystemExit):
            hashed_seqs = seq_mode.hash_file('./tests/wrong_filename.fastb')

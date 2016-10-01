import unittest

from commands import fastq_nt_gt_len as fastq

class TestFastqNtLen(unittest.TestCase):
    def setUp(self):
        self.fastq_files = [
            './tests/test_files/fastq_other/test_4.fastq',
            './tests/test_files/fastq/test_1.fastq',
            './tests/test_files/fastq/test_2.fastq',
            './tests/test_files/fastq/test_3.fastq',
        ]

    def test_get_files_correct_num_files(self):
        files = fastq.get_files('./tests')
        self.assertEqual(sum(1 for f in files), len(self.fastq_files))

    def test_get_files_correct_filenames(self):
        returned_files = fastq.get_files('./tests')

        for f1, f2 in zip(returned_files, self.fastq_files):
            self.assertEqual(f1, f2)
    
    def test_get_perc_gt_len_correct_value(self):
        # Sequences with greater than 30 length(default)
        result = fastq.get_perc_gt_len(self.fastq_files[0], 30)
        self.assertEqual(result, 60.0)

        # Sequences with greater than modified length
        result = fastq.get_perc_gt_len(self.fastq_files[0], 80)
        self.assertEqual(result, 20.0)

    def test_get_perc_gt_len_handles_zero(self):
        # Sequences no sequences longer than absurd number
        result = fastq.get_perc_gt_len(self.fastq_files[0], 3000000)
        self.assertEqual(result, 0.0)

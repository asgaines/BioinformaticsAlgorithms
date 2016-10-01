import unittest

from commands import get_annotations as annot

class TestGetAnnotations(unittest.TestCase):
    def setUp(self):
        self.gtf_files = [
            './tests/test_files/gtf/test_1.gtf',  # Only 1 chromosome
            './tests/test_files/gtf/test_2.gtf',  # 2 chromosomes
            './tests/test_files/gtf/test_3.gtf',  # Multiple chromosomes
            './tests/test_files/gtf/test_4.gtf',  # Reversed test_1.gtf
        ]
        self.coord_files = [
            # 3 Chromosomes
            './tests/test_files/annotate/coordinates_to_annotate.txt',
        ]

    def test_cache_chromosomes_sorts_by_chromosome(self):
        # Grab data from file with only 1 chromosome
        chromosomes = annot.cache_chromosomes(self.gtf_files[0])
        self.assertEqual(len(chromosomes), 1)

        # Grab data from file with only 2 chromosomes
        chromosomes = annot.cache_chromosomes(self.gtf_files[1])
        self.assertEqual(len(chromosomes), 2)

    def test_cache_chromosomes_joins_gene(self):
        # Assert gene introns/exons are joined into a single
        # gene for improved performance
        # Single chromosome:
        chromosomes = annot.cache_chromosomes(self.gtf_files[0])
        start, stop = chromosomes.get('chr3').get('ANAPC13')
        self.assertEqual(start, 134196546)
        self.assertEqual(stop, 134204162)

        # 2 chromosomes:
        chromosomes = annot.cache_chromosomes(self.gtf_files[1])
        start, stop = chromosomes.get('chr9').get('CACFD1')
        self.assertEqual(start, 136333462)
        self.assertEqual(stop, 136335910)
        start, stop = chromosomes.get('chrX').get('MAGED4B')
        self.assertEqual(start, 51804923)
        self.assertEqual(stop, 51805761)

    def test_cache_chromosomes_joins_out_of_order_gene(self):
        chromosomes = annot.cache_chromosomes(self.gtf_files[0])
        start, stop = chromosomes.get('chr3').get('ANAPC13')
        self.assertEqual(start, 134196546)
        self.assertEqual(stop, 134204162)
        
    def test_find_overlap_finds_gene_coord_in_middle(self):
        gene_name = 'SUPERSTRENGTH'
        chromosome = 'chr3'
        start = 134196546
        stop = 134204162
        middle = (start + stop) / 2

        chromosomes = {chromosome: {gene_name: [start, stop]}}
        result = annot.find_overlap(chromosome, middle, chromosomes)
        self.assertEqual(result, gene_name)

    def test_find_overlap_finds_gene_coord_at_beginning(self):
        gene_name = 'SHAPESHIFTER'
        chromosome = 'chrX'
        start = 134196546
        stop = 134204162

        chromosomes = {chromosome: {gene_name: [start, stop]}}
        result = annot.find_overlap(chromosome, start, chromosomes)
        self.assertEqual(result, gene_name)

    def test_find_overlap_finds_gene_coord_at_end(self):
        gene_name = 'LASERVISION'
        chromosome = 'chrZ'
        start = 134196546
        stop = 134204162

        chromosomes = {chromosome: {gene_name: [start, stop]}}
        result = annot.find_overlap(chromosome, stop, chromosomes)
        self.assertEqual(result, gene_name)

    def test_find_overlap_does_not_find_gene_coord_before_gene(self):
        gene_name = 'MYSTERY'
        chromosome = 'chrQ'
        start = 134196546
        stop = 134204162
        before = start - 1000

        chromosomes = {chromosome: {gene_name: [start, stop]}}
        result = annot.find_overlap(chromosome, before, chromosomes)
        self.assertNotEqual(result, gene_name)

    def test_find_overlap_does_not_find_gene_coord_after_gene(self):
        gene_name = 'INVISIBILITY'
        chromosome = 'chrA'
        start = 134196546
        stop = 134204162
        after = stop + 1000

        chromosomes = {chromosome: {gene_name: [start, stop]}}
        result = annot.find_overlap(chromosome, after, chromosomes)
        self.assertNotEqual(result, gene_name)
    
    def test_match_coords_finds_correct_genes(self):
        CHR_12_GENE = 'FRUGAL'
        CHR_5_GENE = 'CRUCIAL'
        CHR_8_GENE = 'REDUNDANT'

        chromosomes = {
            'chr12': {
                CHR_12_GENE: [
                    20000000,
                    30000000
                ],
            },
            'chr5': {
                CHR_5_GENE: [
                    70000000,
                    80000000
                ],
            },
            'chr8': {
                CHR_8_GENE: [
                    20000000,
                    30000000
                ],
            },
        }

        # All match except chr8
        for match in annot.match_coords(self.coord_files[0], chromosomes):
            chromosome, coord, gene_name = match.split()
            
            if chromosome == 'chr8':
                self.assertNotEqual(gene_name, CHR_8_GENE)
            else:
                self.assertIn(gene_name, [CHR_12_GENE, CHR_5_GENE])


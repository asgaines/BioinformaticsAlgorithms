import unittest

from commands.structures.tree import GeneNode, GeneTree

class TestBinaryTree(unittest.TestCase):
    def setUp(self):
        # Genes are preconfigured to be loaded into tree
        # in this order to automatically create balance
        self.genes = [
            # GENE_NAME, start_pos, stop_pos
            ['OP', 50, 53],  # Root node
            ['GH', 25, 28],  # Begin left branch
            ['CD', 10, 13],
            ['KL', 40, 43],
            ['AB',  5,  8],
            ['EF', 15, 18],
            ['IJ', 30, 33],
            ['MN', 45, 48],
            ['WX', 75, 78],  # Begin right branch
            ['ST', 65, 68],
            ['ZY', 90, 93],
            ['QR', 60, 63],
            ['UV', 70, 73],
            ['YZ', 80, 83],
            ['ZZ', 95, 98],
        ]

    def assert_tree_balanced(self, tree):
        # Test root
        self.assertEqual(tree.root.get_name(), 'OP')

        # Test left branch
        self.assertEqual(tree.root.left.get_name(), 'GH')
        # Left branch, first sub-layer
        self.assertEqual(tree.root.left.left.get_name(), 'CD')
        self.assertEqual(tree.root.left.right.get_name(), 'KL')
        # Left branch, second sub-layer
        self.assertEqual(tree.root.left.left.left.get_name(), 'AB')
        self.assertEqual(tree.root.left.left.right.get_name(), 'EF')
        self.assertEqual(tree.root.left.right.left.get_name(), 'IJ')
        self.assertEqual(tree.root.left.right.right.get_name(), 'MN')

        # Test right branch
        self.assertEqual(tree.root.right.get_name(), 'WX')
        # Right branch, first sub-layer
        self.assertEqual(tree.root.right.left.get_name(), 'ST')
        self.assertEqual(tree.root.right.right.get_name(), 'ZY')
        # Right branch, second sub-layer
        self.assertEqual(tree.root.right.left.left.get_name(), 'QR')
        self.assertEqual(tree.root.right.left.right.get_name(), 'UV')
        self.assertEqual(tree.root.right.right.left.get_name(), 'YZ')
        self.assertEqual(tree.root.right.right.right.get_name(), 'ZZ')

    def test_added_root_gene_node_has_correct_values(self):
        gt = GeneTree()

        gene_name = 'XXX'
        gene_start = 150000
        gene_stop = 200000

        gt.add(gene_name, [gene_start, gene_stop])
        
        self.assertEqual(gt.root.get_name(), gene_name)
        self.assertEqual(gt.root.get_start(), gene_start)
        self.assertEqual(gt.root.get_stop(), gene_stop)

    def test_tree_loads_proper_structure_from_preconfigured_gene_order(self):
        gt = GeneTree()
        
        for gene in self.genes:
            name, start, stop = gene
            gt.add(name, [start, stop])

        self.assert_tree_balanced(gt)

    def test_tree_loads_single_gene(self):
        genes = [
            ['AB', 10, 20],
        ]

        gt = GeneTree.init_from_sorted_genes(genes)

        self.assertEqual(gt.num_genes, 1)
        self.assertEqual(gt.root.get_name(), 'AB')

    def test_tree_loads_two_genes(self):
        genes = [
            ['AB', 10, 20],
            ['CD', 30, 40],
        ]

        gt = GeneTree.init_from_sorted_genes(genes)

        self.assertEqual(gt.num_genes, 2)
        self.assertEqual(gt.root.get_name(), 'AB')
        self.assertEqual(gt.root.right.get_name(), 'CD')

    def test_tree_loads_three_genes(self):
        genes = [
            ['AB', 10, 20],
            ['CD', 30, 40],
            ['EF', 40, 50],
        ]

        gt = GeneTree.init_from_sorted_genes(genes)

        self.assertEqual(gt.num_genes, 3)
        self.assertEqual(gt.root.get_name(), 'CD')
        self.assertEqual(gt.root.left.get_name(), 'AB')
        self.assertEqual(gt.root.right.get_name(), 'EF')

    def test_tree_loads_five_genes(self):
        genes = [
            ['AB', 10, 20],
            ['CD', 30, 40],
            ['EF', 50, 60],
            ['GH', 70, 80],
            ['IJ', 90, 100],
        ]

        gt = GeneTree.init_from_sorted_genes(genes)

        self.assertEqual(gt.num_genes, len(genes))

        self.assertEqual(gt.root.get_name(), 'EF')

        self.assertEqual(gt.root.left.get_name(), 'AB')
        self.assertEqual(gt.root.left.right.get_name(), 'CD')

        self.assertEqual(gt.root.right.get_name(), 'GH')
        self.assertEqual(gt.root.right.right.get_name(), 'IJ')

    def test_tree_loads_proper_structure_from_sorted_genes(self):
        # Sort the array based on the start location of the gene
        genes_sorted = sorted(self.genes, key=lambda gene: gene[1])

        gt = GeneTree.init_from_sorted_genes(genes_sorted)

        self.assert_tree_balanced(gt)

    def test_tree_find_correct_node(self):
        gt = GeneTree()

        for gene in self.genes:
            name, start, stop = gene
            gt.add(name, [start, stop])
        
        # Finds gene when given start position
        gene_node = gt.find(5)
        self.assertEqual(gene_node.get_name(), 'AB')

        # Finds gene when given stop position
        gene_node = gt.find(8)
        self.assertEqual(gene_node.get_name(), 'AB')

        # Finds gene when given position in middle of gene
        gene_node = gt.find(7)
        self.assertEqual(gene_node.get_name(), 'AB')

        # Finds nothing when coordinate between genes
        gene_node = gt.find(9)
        self.assertEqual(gene_node, None)

        # Finds nothing when coordinate outside domain of all coordinates
        gene_node = gt.find(999)
        self.assertEqual(gene_node, None)
        gene_node = gt.find(0)
        self.assertEqual(gene_node, None)

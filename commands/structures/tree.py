class Coordinates(object):
    '''
    Handles retrieving the start/stop positions of a gene
    '''

    def __init__(self, coordinates):
        self.start_pos = coordinates[0]
        self.stop_pos = coordinates[1]


class GeneNode(object):
    '''
    Node class which has gene name, coordinates, left/right nodes
    of other genes
    '''

    def __init__(self, name, coordinates):
        self.coordinates = Coordinates(coordinates)
        self.name = name
        self.left = None
        self.right = None

    def get_name(self):
        return self.name

    def get_start(self):
        return self.coordinates.start_pos

    def get_stop(self):
        return self.coordinates.stop_pos


class GeneTree(object):
    '''
    Binary search tree with genes as nodes.
    Loaded from top-down order.
    Tree is balanced if fed a sorted array to
    `create_from_sorted_list`
    Builds on top of add/find functionality taken from
    http://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree-in-python
    '''

    def __init__(self):
        self.root = None
        self.num_genes = 0

    @classmethod
    def init_from_sorted_genes(cls, sorted_genes):
        gt = cls()

        def add_middle(first_index, last_index):
            # Flooring division redundant for Python 2,
            # useful if ported to Python 3
            middle_index = (last_index + first_index) // 2

            gene_middle = sorted_genes[middle_index]
            name = gene_middle[0]
            coordinates = [
                gene_middle[1],
                gene_middle[2],
            ]

            gt.add(name, coordinates)
            
            # Recursively build left branch
            if first_index != middle_index:
                add_middle(first_index, middle_index - 1)
            # Recursively build right branch
            if middle_index != last_index:
                add_middle(middle_index + 1, last_index)

        add_middle(0, len(sorted_genes) - 1)
        return gt

    def add(self, name, coordinates):
        if self.root is None:
            self.root = GeneNode(name, coordinates)
        else:
            self._add(name, coordinates, self.root)
        self.num_genes += 1
    
    def _add(self, name, coordinates, gene_node):
        if coordinates[0] < gene_node.get_start():
            if gene_node.left is not None:
                self._add(name, coordinates, gene_node.left)
            else:
                gene_node.left = GeneNode(name, coordinates)
        else:
            if gene_node.right is not None:
                self._add(name, coordinates, gene_node.right)
            else:
                gene_node.right = GeneNode(name, coordinates)

    def find(self, coordinate):
        if self.root is not None:
            return self._find(coordinate, self.root)

    def _find(self, coordinate, gene_node):
        if coordinate >= gene_node.get_start() and coordinate <= gene_node.get_stop():
            # The gene was found
            return gene_node
        elif coordinate < gene_node.get_start() and gene_node.left is not None:
            return self._find(coordinate, gene_node.left)
        elif coordinate > gene_node.get_stop() and gene_node.right is not None:
            return self._find(coordinate, gene_node.right)

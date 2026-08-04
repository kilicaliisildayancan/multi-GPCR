import dendropy
import os
from alignment import alignment
from mafft import mafft
from general import HOME, run_cmd, AMINO_ACIDS
from functools import lru_cache
from typing import Tuple


def iqtree(source_address: str, model: str = None, verb: bool = False, bootstrap: int = None) -> dendropy.Tree:
    """
    Calculates from the alignment a tree with probabilities for every amino acid in every position.
    Performs:
    1) MAFFT to get the MSA.
    2) Dropping positions with a lot of gaps from the alignment. (TODO: Consider whether this is important. Perhaps when there are gaps, sequences should just be ignored.)
    3) Using IQ-Tree to find the tree and the ancestral tree.
    """
    alignment_address = source_address.split('.', 1)[0] + '.afa'
    tree_address = alignment_address + '.treefile'

    if not os.path.exists(alignment_address):
        if verb:
            print('Creating alignment with MAFFT')
        # Running MAFFT to get the MSA.
        assert os.path.exists(source_address), f"Source address doesn't exist: {source_address}"

        mafft(source_address, alignment_address)

    # Running IQ-Tree to get the tree files.
    if model:
        cmd = ['iqtree', '-s', alignment_address, '-m', model, '-asr', '-nt', 'AUTO']
    else:
        cmd = ['iqtree', '-s', alignment_address, '-asr', '-nt', 'AUTO']

    if bootstrap:
        if type(bootstrap) is not int:
            bootstrap = 1000
        cmd += ['-bb', str(bootstrap)]

    if verb:
        print('Calling IQ-Tree with {}'.format(' '.join(cmd)))
    out, err = run_cmd(cmd)

    if verb:
        print(out)
        print(err)
        print('Parsing the tree.')
    # Parsing the tree.

    tree = dendropy.Tree.get(path=tree_address, schema='newick')

    return tree


def fasttree(source_address: str, /, verb=False, lazy=True) -> dendropy.Tree:
    """
    Calculates from the alignment a tree with probabilities for every amino acid in every position.
    Performs:
    1) MAFFT to get the MSA.
    2) Using IQ-Tree to find the tree and the ancestral tree.
    :param source_address: The address of the alignment for which to calculate the tree.
    :param verb: Whether to print debug information.
    :param lazy: Whether to calculate the tree if it already exists.
    :return: The phylogenetic tree calculated.
    """
    alignment_address = source_address.split('.', 1)[0] + '.afa'
    tree_address = alignment_address + '.treefile'

    if not os.path.exists(alignment_address):
        if verb:
            print('Creating alignment with MAFFT')
        # Running MAFFT to get the MSA.
        assert os.path.exists(source_address), f"Source address doesn't exist: {source_address}"

        mafft(source_address, alignment_address)

    if not os.path.exists(tree_address) or not lazy:
        # Running IQ-Tree to get the tree files.
        cmd = ['fasttreeMP', alignment_address, '>', tree_address]

        if verb:
            print('Calling FASTTREE with {}'.format(' '.join(cmd)))
        out, err = run_cmd(cmd)

        if verb:
            print(out)
            print(err)
            print('Parsing the tree.')
    # Parsing the tree.

    tree = dendropy.Tree.get(path=tree_address, schema='newick')

    return tree


@lru_cache
def get_subtree_size(node: dendropy.Node) -> float:
    """
    Returns the horizontal space that will be required by the subtree rooted by the node.
    """
    if node.is_leaf():
        return 1

    return sum(get_subtree_size(child_node) for child_node in node.child_nodes())


def get_node_annotations(node: dendropy.Node) -> str:
    """
    Gets the node's annotations in a format readable to PhyloSketch.
    """
    res = f"id={node.annotations.get_value('id')}"

    for annotation in node.annotations:
        res += f' {annotation.name}={repr(annotation.value)}'

    return res


def get_edge_annotations(edge: dendropy.Edge) -> str:
    """
    Gets the edge's annotations in a format readable to PhyloSketch.
    """
    res = f"id={edge.annotations.get_value('id')} sid={edge.tail_node.annotations.get_value('id')} tid={edge.head_node.annotations.get_value('id')}"

    for annotation in edge.annotations:
        res += f' {annotation.name}={repr(annotation.value)}'

    return res


def main():
    """
    Testing IQ-TREE.
    """
    print('Testing IQ-Tree.')
    tree = iqtree(f'{HOME}/tests/cluster_021.fa', model='Dayhoff')


if __name__ == '__main__':
    main()

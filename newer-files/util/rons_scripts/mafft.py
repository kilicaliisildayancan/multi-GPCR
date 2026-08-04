import subprocess
import tempfile
import os

from alignment import alignment
from general import HOME, run_cmd, read_fasta, OS


def mafft(input_file: str, output_file: str, tree_out: str = None, verb=False, reorder=True, auto=True, less_gaps = False):
    """
    Creates an MSA for the input file using MAFFT.
    The tree_out option is used to indicate if the phylogenetic tree should be saved.
    """
    # input_file = input_file.replace('\\', '/')
    # output_file = output_file.replace('\\', '/')
    assert os.path.exists(input_file), f'Input file does not exist: {input_file}'

    # MAFFT fails quietly for single-sequence files, so we need to handle it explicitly.
    if sum(1 for seq in read_fasta(input_file)) == 1:
        alignment(input_file).print_to_file(output_file)
        return

    flags = ["--anysymbol"]

    # Handling getting the tree file.
    # A temporary file to store the file in the address where the tree would be saved.
    tree_temp_file = None
    # The default address where the tree would be saved.
    tree_default_address = input_file + '.tree'

    if auto:
        flags.append('--auto')
    if less_gaps:
        flags.append('--leavegappyregion')
    if reorder:
        flags.append('--reorder')

    if tree_out:
        flags.append('--treeout')

        # Preventing MAFFT default output from overwriting files.
        if os.path.exists(tree_default_address):
            tree_temp_file = tempfile.TemporaryFile('w+')
            with open(tree_default_address, 'r') as old_file:
                tree_temp_file.write(old_file.read())

    command = ['mafft'] + flags + [input_file, '>', output_file]
    if verb:
        print('Running MAFFT with command {}'.format(command))
    out, err = run_cmd(command)
    if verb:
        print('MAFFT output:')
        print(out)
        print('MAFFT error stream:')
        print(err)

    # Transferring the tree output from the default output to the specified address.
    if tree_out:
        with open(tree_out, 'w') as tree_out_file, open(tree_default_address, 'r') as tree_default_file:
            tree_out_file.write(tree_default_file.read())
        os.remove(tree_default_address)

        # Restoring the file that was overridden.
        if tree_temp_file:
            with open(tree_default_address, 'w') as tree_default_file:
                tree_temp_file.seek(0)
                tree_default_file.write(tree_temp_file.read())
        if tree_temp_file:
            tree_temp_file.close()

    assert os.path.exists(output_file), 'Output file was not created!'


def run_tests():
    """
    Running tests on the defined functions:
    - runcmd
    - mafft
    """
    print('Testing runcmd:')
    out, err = run_cmd('echo hello')
    # print('Out: {}'.format(out))
    # print('Err: {}'.format(err))

    print('Testing MAFFT:')


    mafft(input_file="/home/kilicali/multi-domain_gpcr/datafiles/pipelinework/6PS8_T2.fasta", output_file="/home/kilicali/multi-domain_gpcr/datafiles/pipelinework/6PS8_T2.aln", verb=True)
    # for fasta_file in os.listdir("/home/kilicali/multi-domain_gpcr/datafiles/representatives/"):
    #     in_addr = f'{HOME}/datafiles/representatives/{fasta_file.split(".")[0]}.fasta'
    #     out_addr = f'{HOME}/datafiles/representative_msa/{fasta_file.split(".")[0]}.aln'
    #     mafft(in_addr, out_addr)


if __name__ == "__main__":
    run_tests()

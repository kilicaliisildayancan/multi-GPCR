'''
A class to handle MSAs.
'''
import random
from functools import cached_property
from general import average
import os

_FASTA_SUFFIXES = {'fa', 'afa', 'fasta'}
_STOCKHOLM_SUFFIXES = {'sto'}
_ALN_SUFFIXES = {'aln'}
_RAPTORX_SUFFIXES = {'rap', 'raptor', 'raptorx'}

RAPTORX_MAX_LENGTH = 1300

class alignment(dict):
    '''
    An object to allow handling MSAs.
    The alignment class supports all Dictionary operations.
    '''

    def __init__(self, *args, **kwargs):
        """
        A constructor. Valid arguments are:
        - Address of MSA file, in any accepted format.
        - Dictionary of sequences.

        If the format keyword is given, the alignment treats the input file according to the specified format.
        If the sequence_names argument is given, only the sequences with the given names will be read from the file.
        """


        if len(args) == 1:
            #Copy constructor.
            if isinstance(args[0], dict):
                for name, seq in args[0].items():
                    self[name] = seq
            #Parsing a file.
            elif type(args[0]) == str:
                self._parse_file(args[0], force_format=kwargs.get('format', None), sequence_names=kwargs.get('sequence_names', None))
    
    def _parse_file(self, address, force_format=None, sequence_names=None, **kwargs):
        """
        Initializes the alignment from a file.
        The force_format argument forces the alignment to treat the file as a specific format.
        """
        #Getting the file suffix.

        if force_format:
            suffix = force_format
        else:
            suffix = address.split('.', 1)
            if len(suffix) == 0:
                raise NotImplementedError('File with no format specifier: {}'.format(address))
            suffix = suffix[1]

        # print('Parsing file {}'.format(address))
        # print('Sequence names: {}'.format(len(sequence_names) if sequence_names else 0))

        #Handling FASTA-like files
        if suffix in _FASTA_SUFFIXES:
            name = None
            with open(address, 'r') as data_file:
                for line in data_file:
                    line = line.strip()
                    #A sequence identifier line.
                    if line[:1] == '>':
                        name = line[1:].split()[0]
                        if sequence_names and (name not in sequence_names):
                            name = None
                        if name and (name not in self):
                            self[name] = ''
                    else:
                        if name:
                            self[name] += line

        else:
            raise NotImplementedError('File with unrecognized suffix: {}'.format(address))
    
    def print_to_file(self, address, force_format=None, **kwargs):
        """
        Saves the alignment to the given address.
        :param address: The address to save the alignment.
        :param force_format: Optional argument to set the format of the output file.
        :param kwargs:
        """
        if force_format:
            suffix = force_format
        else:
            suffix = address.split('.', 1)
            if len(suffix) == 0:
                raise NotImplementedError('File with no format specifier: {}'.format(address))
            suffix = suffix[1]

        # print('alignment::print_to_file', suffix)

        if suffix in _FASTA_SUFFIXES:
            with open(address, 'w') as out_file:
                for name, seq in self.items():
                    out_file.write('>{}\n{}\n'.format(name, seq))
        elif suffix in _STOCKHOLM_SUFFIXES:
            with open(address, 'w') as out_file:
                out_file.write("# STOCKHOLM 1.0\n")
                for name in self:
                    out_file.write(name+" "+self[name]+"\n")
                out_file.write("//\n")
        elif suffix in _RAPTORX_SUFFIXES:
            _raptor_format = lambda s:s.replace('B', 'N').replace('Z', 'Q').replace('X', 'A')
            with open(address, 'w') as out_file:
                # Handling first sequence.
                # first_name = max(self.keys(), key=lambda n:len(self[n].replace('-', '')))
                if 'first_name' not in kwargs:
                    first_name = random.choice(list(self.keys()))
                else:
                    first_name = kwargs['first_name']
                out_file.write('>{}\n{}\n'.format(first_name, _raptor_format(self[first_name].replace('-', 'G'))))

                for name, seq in self.items():
                    assert len(seq) <= RAPTORX_MAX_LENGTH, f'Printing alignment {address} with sequence of length {len(seq)}!'
                    if name != first_name:
                        out_file.write('>{}\n{}\n'.format(name, _raptor_format(seq)))
        elif suffix in _ALN_SUFFIXES:
            # The format used by TripletRes. Doesn't include sequence names.
            with open(address, 'w') as out_file:
                for _, seq in self.items():
                    out_file.write(f'{seq}\n')

        else:
            raise NotImplementedError('File with unrecognized suffix: {}'.format(address))     
    
    
    def is_aligned(self):
        """
        Returns whether all the sequences in the alignment have the same length.
        """
        if len(self) == 0:
            return True
        length = len(next(iter(self.values())))

        return all(len(seq) == length for seq in self.values())

    def length(self):
        """
        Returns the length of the alignment.
        If the alignment is not aligned, returns the average length. 
        """
        if self.is_aligned():
            return len(next(iter(self.values())))

        return average(len(seq) for seq in self.values())

    def trim(self, cutoff):
        """
        Removes all positions in the alignment determined by the cutoff.
        The cutoff can be a function, array, or a float.
        """
        assert self.is_aligned(), "Can't trim a non-MSA alignment!"
        if isinstance(cutoff, float):
            # Handling float cutoffs.
            counts = [0]*self.length()
            for seq in self.values():
                for index, i in enumerate(seq):
                    counts[index] += (i != '-')
            return self.trim([index for index, count in enumerate(counts) if count >= len(self) * cutoff])

        elif isinstance(cutoff, list):
            # Handling lists. The cutoff is the list of indices kept.
            res = alignment()
            for name in self.keys(): res[name] = ''.join(self[name][i] for i in sorted(cutoff))
            return res
        else:
            #Handling functions.
            return self.trim([i for i in range(self.length()) if cutoff(i)])


def run_tests():
    '''
    Running tests on the alignment class.
    '''
    from general import HOME

    alignment_address = f'{HOME}/datafiles/representatives/'
    out_address = f'{HOME}/datafiles/representative_msa/'
    for fasta_file in os.listdir(alignment_address):
        al = alignment(alignment_address+fasta_file)
        print(f'Number of sequences: {len(al)}')
        print(f'Length of sequences: {al.length()}')
        al.print_to_file(out_address+fasta_file.split(".")[0]+".sto", force_format = "sto")


if __name__ == "__main__":
    run_tests()
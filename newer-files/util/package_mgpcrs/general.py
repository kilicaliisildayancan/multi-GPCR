"""
A general utility file.
Includes paths to databases and utility functions.
"""
import enum
import tempfile
import subprocess
import os
from enum import Enum
from typing import Callable, Tuple, Union, Generator
import sys

DATABASE_HOME = "/home/kilicali/DB/UniProt"
HOME = "/home/kilicali/multi-domain_gpcr/datafiles"


# Searching for the home directory.
if HOME is None:
    parts = __file__.split(os.path.sep)
    HOME = os.path.sep.join(parts[:-2])

if DATABASE_HOME is None:
    DATABASE_HOME = HOME

PDB = f'{DATABASE_HOME}/pdb.fa'
PDB25 = f'{DATABASE_HOME}/pdb25.fa'
PDB50 = f'{DATABASE_HOME}/pdb50.fa'
PDB70 = f'{DATABASE_HOME}/pdb70.fa'
PDB90 = f'{DATABASE_HOME}/pdb90.fa'

UNIREF100 = UNIREF = f'{DATABASE_HOME}/uniref100.fa'
UNIREF90 = f'{DATABASE_HOME}/uniref90.fa'
UNIREF_PATTERN = f'{DATABASE_HOME}/uniref_len_{{}}.fa'  # The pattern for the uniref database filtered by length.
UNIREF_MIN_LENGTH = 0  # The minimum length of the uniref pattern.
UNIREF_MAX_LENGTH = 2001  # One above the maximum length of the uniref pattern.
UNIREF_LENGTH_JUMP = 100  # The jump of the uniref pattern.

_BUILTIN_PATHS = [HOME, PDB, PDB25, PDB50, PDB70, PDB90, UNIREF, UNIREF90,
                  *(UNIREF_PATTERN.format(i) for i in range(UNIREF_MIN_LENGTH, UNIREF_MAX_LENGTH, UNIREF_LENGTH_JUMP))]

THREE_LETTER_CODES = dict(ALA='A', CYS='C', ASP='D', GLU='E', PHE='F', GLY='G', HIS='H', ILE='I', LYS='K', LEU='L',
                          MET='M', ASN='N', PYL='O', PRO='P', GLN='Q', ARG='R', SER='S', THR='T', SEC='U', VAL='V',
                          TRP='W', TYR='Y')

AMINO_ACIDS = 'ARNDCQEGHILKMFPSTWYV-'
BLOSUM62 = {
    '-': {'-': 1, 'A': -4, 'C': -4, 'B': -4, 'E': -4, 'D': -4, 'G': -4, 'F': -4, 'I': -4, 'H': -4, 'K': -4, 'M': -4,
          'L': -4, 'N': -4, 'Q': -4, 'P': -4, 'S': -4, 'R': -4, 'T': -4, 'W': -4, 'V': -4, 'Y': -4, 'X': -4, 'Z': -4},
    'A': {'-': -4, 'A': 4, 'C': 0, 'B': -2, 'E': -1, 'D': -2, 'G': 0, 'F': -2, 'I': -1, 'H': -2, 'K': -1, 'M': -1,
          'L': -1, 'N': -2, 'Q': -1, 'P': -1, 'S': 1, 'R': -1, 'T': 0, 'W': -3, 'V': 0, 'Y': -2, 'X': 0, 'Z': -1},
    'C': {'-': -4, 'A': 0, 'C': 9, 'B': -3, 'E': -4, 'D': -3, 'G': -3, 'F': -2, 'I': -1, 'H': -3, 'K': -3, 'M': -1,
          'L': -1, 'N': -3, 'Q': -3, 'P': -3, 'S': -1, 'R': -3, 'T': -1, 'W': -2, 'V': -1, 'Y': -2, 'X': -2, 'Z': -3},
    'B': {'-': -4, 'A': -2, 'C': -3, 'B': 4, 'E': 1, 'D': 4, 'G': -1, 'F': -3, 'I': -3, 'H': 0, 'K': 0, 'M': -3,
          'L': -4, 'N': 3, 'Q': 0, 'P': -2, 'S': 0, 'R': -1, 'T': -1, 'W': -4, 'V': -3, 'Y': -3, 'X': -1, 'Z': 1},
    'E': {'-': -4, 'A': -1, 'C': -4, 'B': 1, 'E': 5, 'D': 2, 'G': -2, 'F': -3, 'I': -3, 'H': 0, 'K': 1, 'M': -2,
          'L': -3, 'N': 0, 'Q': 2, 'P': -1, 'S': 0, 'R': 0, 'T': -1, 'W': -3, 'V': -2, 'Y': -2, 'X': -1, 'Z': 4},
    'D': {'-': -4, 'A': -2, 'C': -3, 'B': 4, 'E': 2, 'D': 6, 'G': -1, 'F': -3, 'I': -3, 'H': -1, 'K': -1, 'M': -3,
          'L': -4, 'N': 1, 'Q': 0, 'P': -1, 'S': 0, 'R': -2, 'T': -1, 'W': -4, 'V': -3, 'Y': -3, 'X': -1, 'Z': 1},
    'G': {'-': -4, 'A': 0, 'C': -3, 'B': -1, 'E': -2, 'D': -1, 'G': 6, 'F': -3, 'I': -4, 'H': -2, 'K': -2, 'M': -3,
          'L': -4, 'N': 0, 'Q': -2, 'P': -2, 'S': 0, 'R': -2, 'T': -2, 'W': -2, 'V': -3, 'Y': -3, 'X': -1, 'Z': -2},
    'F': {'-': -4, 'A': -2, 'C': -2, 'B': -3, 'E': -3, 'D': -3, 'G': -3, 'F': 6, 'I': 0, 'H': -1, 'K': -3, 'M': 0,
          'L': 0, 'N': -3, 'Q': -3, 'P': -4, 'S': -2, 'R': -3, 'T': -2, 'W': 1, 'V': -1, 'Y': 3, 'X': -1, 'Z': -3},
    'I': {'-': -4, 'A': -1, 'C': -1, 'B': -3, 'E': -3, 'D': -3, 'G': -4, 'F': 0, 'I': 4, 'H': -3, 'K': -3, 'M': 1,
          'L': 2, 'N': -3, 'Q': -3, 'P': -3, 'S': -2, 'R': -3, 'T': -1, 'W': -3, 'V': 3, 'Y': -1, 'X': -1, 'Z': -3},
    'H': {'-': -4, 'A': -2, 'C': -3, 'B': 0, 'E': 0, 'D': -1, 'G': -2, 'F': -1, 'I': -3, 'H': 8, 'K': -1, 'M': -2,
          'L': -3, 'N': 1, 'Q': 0, 'P': -2, 'S': -1, 'R': 0, 'T': -2, 'W': -2, 'V': -3, 'Y': 2, 'X': -1, 'Z': 0},
    'K': {'-': -4, 'A': -1, 'C': -3, 'B': 0, 'E': 1, 'D': -1, 'G': -2, 'F': -3, 'I': -3, 'H': -1, 'K': 5, 'M': -1,
          'L': -2, 'N': 0, 'Q': 1, 'P': -1, 'S': 0, 'R': 2, 'T': -1, 'W': -3, 'V': -2, 'Y': -2, 'X': -1, 'Z': 1},
    'M': {'-': -4, 'A': -1, 'C': -1, 'B': -3, 'E': -2, 'D': -3, 'G': -3, 'F': 0, 'I': 1, 'H': -2, 'K': -1, 'M': 5,
          'L': 2, 'N': -2, 'Q': 0, 'P': -2, 'S': -1, 'R': -1, 'T': -1, 'W': -1, 'V': 1, 'Y': -1, 'X': -1, 'Z': -1},
    'L': {'-': -4, 'A': -1, 'C': -1, 'B': -4, 'E': -3, 'D': -4, 'G': -4, 'F': 0, 'I': 2, 'H': -3, 'K': -2, 'M': 2,
          'L': 4, 'N': -3, 'Q': -2, 'P': -3, 'S': -2, 'R': -2, 'T': -1, 'W': -2, 'V': 1, 'Y': -1, 'X': -1, 'Z': -3},
    'N': {'-': -4, 'A': -2, 'C': -3, 'B': 3, 'E': 0, 'D': 1, 'G': 0, 'F': -3, 'I': -3, 'H': 1, 'K': 0, 'M': -2, 'L': -3,
          'N': 6, 'Q': 0, 'P': -2, 'S': 1, 'R': 0, 'T': 0, 'W': -4, 'V': -3, 'Y': -2, 'X': -1, 'Z': 0},
    'Q': {'-': -4, 'A': -1, 'C': -3, 'B': 0, 'E': 2, 'D': 0, 'G': -2, 'F': -3, 'I': -3, 'H': 0, 'K': 1, 'M': 0, 'L': -2,
          'N': 0, 'Q': 5, 'P': -1, 'S': 0, 'R': 1, 'T': -1, 'W': -2, 'V': -2, 'Y': -1, 'X': -1, 'Z': 3},
    'P': {'-': -4, 'A': -1, 'C': -3, 'B': -2, 'E': -1, 'D': -1, 'G': -2, 'F': -4, 'I': -3, 'H': -2, 'K': -1, 'M': -2,
          'L': -3, 'N': -2, 'Q': -1, 'P': 7, 'S': -1, 'R': -2, 'T': -1, 'W': -4, 'V': -2, 'Y': -3, 'X': -2, 'Z': -1},
    'S': {'-': -4, 'A': 1, 'C': -1, 'B': 0, 'E': 0, 'D': 0, 'G': 0, 'F': -2, 'I': -2, 'H': -1, 'K': 0, 'M': -1, 'L': -2,
          'N': 1, 'Q': 0, 'P': -1, 'S': 4, 'R': -1, 'T': 1, 'W': -3, 'V': -2, 'Y': -2, 'X': 0, 'Z': 0},
    'R': {'-': -4, 'A': -1, 'C': -3, 'B': -1, 'E': 0, 'D': -2, 'G': -2, 'F': -3, 'I': -3, 'H': 0, 'K': 2, 'M': -1,
          'L': -2, 'N': 0, 'Q': 1, 'P': -2, 'S': -1, 'R': 5, 'T': -1, 'W': -3, 'V': -3, 'Y': -2, 'X': -1, 'Z': 0},
    'T': {'-': -4, 'A': 0, 'C': -1, 'B': -1, 'E': -1, 'D': -1, 'G': -2, 'F': -2, 'I': -1, 'H': -2, 'K': -1, 'M': -1,
          'L': -1, 'N': 0, 'Q': -1, 'P': -1, 'S': 1, 'R': -1, 'T': 5, 'W': -2, 'V': 0, 'Y': -2, 'X': 0, 'Z': -1},
    'W': {'-': -4, 'A': -3, 'C': -2, 'B': -4, 'E': -3, 'D': -4, 'G': -2, 'F': 1, 'I': -3, 'H': -2, 'K': -3, 'M': -1,
          'L': -2, 'N': -4, 'Q': -2, 'P': -4, 'S': -3, 'R': -3, 'T': -2, 'W': 11, 'V': -3, 'Y': 2, 'X': -2, 'Z': -3},
    'V': {'-': -4, 'A': 0, 'C': -1, 'B': -3, 'E': -2, 'D': -3, 'G': -3, 'F': -1, 'I': 3, 'H': -3, 'K': -2, 'M': 1,
          'L': 1, 'N': -3, 'Q': -2, 'P': -2, 'S': -2, 'R': -3, 'T': 0, 'W': -3, 'V': 4, 'Y': -1, 'X': -1, 'Z': -2},
    'Y': {'-': -4, 'A': -2, 'C': -2, 'B': -3, 'E': -2, 'D': -3, 'G': -3, 'F': 3, 'I': -1, 'H': 2, 'K': -2, 'M': -1,
          'L': -1, 'N': -2, 'Q': -1, 'P': -3, 'S': -2, 'R': -2, 'T': -2, 'W': 2, 'V': -1, 'Y': 7, 'X': -1, 'Z': -2},
    'X': {'-': -4, 'A': 0, 'C': -2, 'B': -1, 'E': -1, 'D': -1, 'G': -1, 'F': -1, 'I': -1, 'H': -1, 'K': -1, 'M': -1,
          'L': -1, 'N': -1, 'Q': -1, 'P': -2, 'S': 0, 'R': -1, 'T': 0, 'W': -2, 'V': -1, 'Y': -1, 'X': -1, 'Z': -1},
    'Z': {'-': -4, 'A': -1, 'C': -3, 'B': 1, 'E': 4, 'D': 1, 'G': -2, 'F': -3, 'I': -3, 'H': 0, 'K': 1, 'M': -1,
          'L': -3, 'N': 0, 'Q': 3, 'P': -1, 'S': 0, 'R': 0, 'T': -1, 'W': -3, 'V': -2, 'Y': -2, 'X': -1, 'Z': 4}}
IDENTITY = {i: {j: 1 if i == j else 0 for j in AMINO_ACIDS} for i in AMINO_ACIDS}

BENTALSCALE = {"I": -2.6,
"L": -2.6,
"F": -1.5,
"V": -1.2,
"A": -0.2,
"G": 0.0,
"C": 0.4,
"S": 0.8,
"T": 1.1,
"M": 1.3,
"W": 1.3,
"P": 2.8,
"Y": 4.3,
"Q": 5.4,
"H": 6.8,
"K": 7.4,
"N": 7.7,
"E": 9.5,
"D": 11.5,
"R": 19.8}

# for path in _BUILTIN_PATHS:
#     assert os.path.exists(path), 'Builtin path doesn\t exist: {}'.format(path)

class OS(Enum):
    WINDOWS = enum.auto()
    LINUX = enum.auto()


def run_cmd(command: Union[str, list], *args, **kwargs) -> Tuple[str, str]:
    """
    Runs a windows command.
    :param command: A string or a list of strings representing a windows command.
    """

    if isinstance(command, list):
        command = ' '.join(command)

    proc = subprocess.run(command, shell=True, capture_output=True)

    out_str = proc.stdout.decode('utf-8')
    err_str = proc.stderr.decode('utf-8')

    return out_str, err_str


def average(iterable: 'iterable') -> float:
    """
    Calculates the average of an iterable object containing floats.
    If there are zero items, returns 0.
    """
    res = 0
    count = 0
    for i in iterable:
        res += i
        count += 1

    if count == 0:
        return 0

    return res / count


def read_fasta(address: str) -> Generator[Tuple[str, str], None, None]:
    """
    Reads the sequences in a FASTA files.
    Returns a generator of the names and sequences to allow handling extremely large alignments.
    :param address: The address of the file to read.
    :return: A generator yielding the pairs (name, sequence).
    """
    name = ''
    seq = ''
    with open(address) as f:
        for ln in f:
            if ln[0] == '>':
                if name:
                    yield name, seq
                name = ln[1:].strip()
                seq = ''
            else:
                seq += ln.strip()
        if seq:
            yield name, seq

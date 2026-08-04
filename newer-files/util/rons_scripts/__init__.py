"""
An __init__ file for the utility package.
"""

from util.general import *
from util.alignment import alignment
from util.mafft import mafft
from util.union_tree import *

# The phylogeny module require DendroPy for tree handling.
try:
    from phylogeny import *
except ImportError as e:
    print('Warning: Importing the phylogeny functions failed. Is DendroPy installed?')
    print(e)

from general import run_cmd, HOME, PDB, average, UNIREF_MIN_LENGTH, UNIREF_MAX_LENGTH, UNIREF_LENGTH_JUMP, UNIREF_PATTERN, OS
from mafft import mafft
from alignment import alignment
import os
import tempfile


def hmmbuild(inp, output, *args, **kwargs):
    """
    Builds an HMM file from the given MSA file in the stockholm format.
    """
    assert os.path.exists(inp), 'Input MSA file doesn\'t exist: {}'.format(inp)

    verb = ("-v" in args) or kwargs.get('verb', False)
    cmd = ['hmmbuild']
    for flag in args:
        if flag != "-v":
            cmd.append(flag)
    cmd += [output, inp]
    res = run_cmd(cmd, operating_system=OS.LINUX)
    if verb:
        for ln in res:
            print(ln[:-1])

    assert os.path.exists(output), 'Target HMM was not created: {}'.format(output)


class Match(object):
    """
    A match between two protein sequences.
    """

    def __init__(self, q_start: int, q_end: int, t_start: int, t_end: int, e_value: float):
        self.q_start = q_start
        self.q_end = q_end
        self.t_start = t_start
        self.t_end = t_end
        self.e_value = e_value

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'Match(q{self.q_start, self.q_end}, t{self.t_start, self.t_end}, {self.e_value})'


class SearchResult(dict):
    """
    A class that holds the result of a HMMER search.
    Not properly documented.
    """

    def __init__(self):
        pass

    def parse_hmmer(self, sr, cutoff=1e-5):
        """
        Parses the results of the HMMER search.
        Ignores results with score below the cutoff.
        """
        name = ""
        for line in sr.split('\n'):
            ln = line.split()

            if len(ln) < 2:
                continue
            if ln[0] == ">>":
                name = ln[1]
            if (ln[1] == "!" or ln[1] == "?") and (name != ""):
                # print(ln)
                score = float(ln[5])
                if score > cutoff: continue
                if name not in self:
                    self[name] = []
                self[name].append(Match(int(ln[6]), int(ln[7]), int(ln[9]), int(ln[10]), score))

    def __getitem__(self, protein_name: str) -> list:
        """
        Overloading the dict __getitem__ to add typing information.
        :param protein_name: A name of a protein.
        :return: The hits of the given protein.
        """
        return dict.__getitem__(self, protein_name)


def hmmsearch(hmm, database, cutoff=1e-5, verb=False, backup=None, *args) -> SearchResult:
    """
    Performs a HMMER search on a database using the given HMM address and cutoff.
    """
    assert os.path.exists(hmm), f"HMM file doesn't exist: {hmm}"
    assert os.path.exists(database), f"Database file doesn't exist: {database}"

    # verb = ("-v" in args)

    cmd = ['hmmsearch']
    for flag in args:
        if flag != "-v":
            cmd.append(flag)
    cmd += ["--noali"]
    cmd += [hmm, database]
    # print(cmd)

    # If there is a backup of the HMMsearch, we read from the backup first.
    # If the backup doesn't exist, we create it.
    if backup and os.path.exists(backup):
        with open(backup, 'r') as backup_file:
            res = backup_file.read()
    else:
        res, _ = run_cmd(cmd, operating_system=OS.LINUX)
        if backup:
            with open(backup, 'w') as backup_file:
                backup_file.write(res)

    if verb:
        for ln in res:
            print(ln[:-1])
    search_results = SearchResult()
    search_results.parse_hmmer(res, cutoff)
    return search_results


def hmmalign(src_address: str, output_file: str, hmm_address: str):
    """
    Creates an MSA of the given sequence file using the given HMM file.
    :param src_address: The file containing the sequences to be aligned.
    :param hmm_address: The file containing the HMM used for aligning.
    :param output_file: The address to print the MSA.
    """
    assert os.path.exists(src_address), f"Sequence file doesn't exist: {src_address}"
    assert os.path.exists(hmm_address), f"HMM file doesn't exist: {hmm_address}"

    command = ['hmmalign', hmm_address, src_address]

    output_str, err_str = run_cmd(command, operating_system=OS.LINUX)

    with open(output_file, 'w') as f:
        f.write(output_str)

    assert os.path.exists(output_file), f'Output file {output_file} was not formed.'


def make_hmm(src_address, alignment_address, target_address, lazy=False, verb=False, reorder= True, auto=True):
    """
    Creates an HMM from the given alignment.
    If the alignment address is given, the MSA is stored.
    """
    assert os.path.exists(src_address), 'Non-existent source FASTA file: {}'.format(src_address)

    if len(alignment(src_address)) == 1:
        alignment(src_address).print_to_file(alignment_address)

    elif (not lazy) or (not os.path.exists(alignment_address)):
        mafft(src_address, alignment_address, verb=verb, reorder=reorder, auto=auto)
        alignment(alignment_address, format='afa').print_to_file(alignment_address)

    hmmbuild(alignment_address, target_address, verb=verb)


def gather_homologs(seq_address: str, database: str = None, len_diff: float = 0.8, verb: bool = False,
                    repeats: int = 2, trim: bool = True, cutoff: float = 1e-5) -> alignment:
    """
    Gathers homologs for a given sequence, an returns an alignment containing the sequences.
    The input must be an alignment containing a single sequence.
    The gathered sequences are put in the out address.

    The database option can be used to specify a database other than uniref100.
    """

    # The addresses storing intermediate sequences.
    addresses = []

    base_address = seq_address.split('.', 1)[0]

    addresses.append(base_address)
    for i in range(repeats):
        addresses.append(f'{base_address}_T{i + 1}')

    result_sequences = None
    for i in range(repeats):
        if verb:
            print(f'hmmer::gather_homologs Starting iteration {i}')

        al = alignment(addresses[i] + '.fasta')
        # assert len(al) == 1, 'Base alignment has more than one sequence!'

        if verb:
            print(f'Built HMM')

        make_hmm(addresses[i] + '.fasta', addresses[i] + '.sto', addresses[i] + '.hmm')

        seq_len = average(len(seq) for seq in al.values())

        min_len = max(int(round(seq_len * len_diff - 50, -2)), UNIREF_MIN_LENGTH)
        max_len = min(int(round(seq_len / len_diff + 50, -2)), UNIREF_MAX_LENGTH)

        if verb:
            print(f'Round {i} Starting gathering homologs with lengths {min_len}<{seq_len}<{max_len}')
            print(f'Gathering homologs for {addresses[i].split("/")[-1]}')

        # Performing the HMMER search.

        results = {}

        if database:
            results = hmmsearch(addresses[i] + '.hmm', database, backup=f'{addresses[i]}.hres', cutoff=cutoff)
        else:
            for search_len in range(min_len, max_len, UNIREF_LENGTH_JUMP):
                if verb:
                    print('Searching for homologs in uniref_len_{}.fa'.format(search_len))
                results.update(hmmsearch(addresses[i] + '.hmm', UNIREF_PATTERN.format(search_len),
                                         backup=f'{addresses[i]}_{search_len}.hres'))

        # A dict from a name to strongly matching segments.
        good_hits = {}

        # Filtering only the full matches in the SearchResult.
        for name, hits in results.items():
            for hit in hits:
                if name not in good_hits:
                    good_hits[name] = []
                if len_diff <= (hit.q_end - hit.q_start) / seq_len <= 1. / len_diff:
                    good_hits[name].append((hit.t_start, hit.t_end))

        # Reading the sequences of the sequences with full matches.
        temp_sequences = alignment()
        result_sequences = alignment()
        if database:
            temp_sequences = alignment(database, sequence_names=good_hits)
        else:
            for seq_len in range(min_len, max_len, UNIREF_LENGTH_JUMP):
                temp_sequences.update(alignment(UNIREF_PATTERN.format(seq_len), sequence_names=good_hits))

        # Transferring the good matches to the new alignment.
        for name in good_hits:
            if trim:
                if len(good_hits[name]) == 1:
                    segment = good_hits[name][0]
                    result_sequences[name] = temp_sequences[name][segment[0]:segment[1]]
                else:
                    for index, segment in enumerate(good_hits[name]):
                        result_sequences[f'{name}_{index}'] = temp_sequences[name][segment[0]:segment[1]]
            else:
                result_sequences[name] = temp_sequences[name]

        if len(result_sequences) == 0:
            return alignment(seq_address)

        result_sequences.print_to_file(addresses[i + 1] + '.fasta')

    # Handling an expansion with 0 expansion cycles.
    if result_sequences is None:
        return alignment(seq_address)

    return result_sequences


def run_tests():
    """
    Tests the HMMER search procedures.
    """
    print('Building test HMM.')
    base_addr = f'{HOME}/pipelinework/'
    ali_addr = f'{HOME}/representative_msa/'
    hmm_addr = f'{HOME}/representative_hmm/'

    for file in os.listdir(base_addr):
        if "_T2.fasta" in file:
            name = file.split(".")[0]
            fasta_file = base_addr+file
            make_hmm(base_addr+name+".fasta", ali_addr+name+".afa", hmm_addr+name+".hmm", verb = True, reorder=False, auto = True)



    #print('Searching for homologs.')
    #es = hmmsearch(hmm_addr, PDB)

    #for name, hits in res.items():
    #    print(name, len(hits))


if __name__ == "__main__":
    run_tests()

from Bio import AlignIO
import os

base_dir = "/home/kilicali/multi-domain_gpcr/chemokines/msas/rep_msas"
def remove_duplicates(input_file, output_file):
    alignment = AlignIO.parse(input_file, "stockholm")
    unique_seqs = {}

    for record in alignment:
        seq_id = record.id
        seq = str(record.seq)

        if seq_id in unique_seqs:
            # Skip if the identifier is already encountered
            continue

        if seq in unique_seqs.values():
            # Skip if the sequence is already encountered
            continue

        unique_seqs[seq_id] = seq

    with open(output_file, "w") as outfile:
        for record in alignment:
            seq_id = record.id
            seq = str(record.seq)

            if seq_id in unique_seqs and seq == unique_seqs[seq_id]:
                outfile.write(f">{seq_id}\n{seq}\n")
                del unique_seqs[seq_id]

# Provide a list of input and output file paths
alignment_files = os.listdir(base_dir)

for input_file in alignment_files:
    input_file = os.path.join(base_dir, input_file)
    output_file = input_file + ".new"
    remove_duplicates(input_file, output_file)

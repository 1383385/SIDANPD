from Bio import SeqIO

# get the IDs in commensal_hit.fasta
commensal_ids = set([rec.id for rec in SeqIO.parse('additional_files/commensal_hit.fasta', 'fasta')])

# get entries unique to pathogen_hit.fasta
non_commensal = (rec for rec in SeqIO.parse('additional_files/test_large_seq.fasta', 'fasta') if rec.id not in commensal_ids)

# write unique entries to new file: pathogen_unique.fna
with open('additional_files/non_commensal.fasta', 'w') as target:
    SeqIO.write(non_commensal, target, 'fasta')



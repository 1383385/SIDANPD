from Bio import SeqIO
commensal_ids = set([rec.id for rec in SeqIO.parse('additional_files/commensal_hit.fasta', 'fasta')])
non_commensal = (rec for rec in SeqIO.parse('additional_files/test_large_seq.fasta', 'fasta') if rec.id not in commensal_ids)
with open('additional_files/non_commensal.fasta', 'w') as target:
    SeqIO.write(non_commensal, target, 'fasta')



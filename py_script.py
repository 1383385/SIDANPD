import os
import pandas as pd 
import matplotlib.pyplot as plt
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio import SeqIO
file_input = 'generic'

###Conversion of FASTQ to FASTA
print("Converting FASTQ to FASTA")
fq_to_fa = 'wsl seqtk seq -a {}.fastq > additional_files/{}.fasta'.format(file_input,file_input)
os.system(fq_to_fa)


###Removal of Adapters
print("Removing Adapters")
pore_chop = "wsl porechop -i additional_files/{}.fasta -o additional_files/{}1.fasta".format(file_input,file_input)
os.system(pore_chop)

###Removal of Shorter Sequences
print("Removing shorter sequences")
rmv_short_seq = "wsl seqtk seq -L 1000 additional_files/{}1.fasta > additional_files/{}_large_seq.fasta".format(file_input,file_input)
os.system(rmv_short_seq)


###Megablast of processed sequences with the Pathogen database 
print("Megablast with pathogen database")
megablast_path_database = "wsl blastn -query additional_files/{}_large_seq.fasta -db database/pathogen -out additional_files/query_pathogen.csv -outfmt 6 -evalue 1e-100 -max_target_seqs 1 -perc_identity 85 -qcov_hsp_perc 90 -task megablast".format(file_input)
os.system(megablast_path_database)

seqtk1 = "wsl seqtk subseq additional_files/{}.fasta additional_files/query_pathogen.list > additional_files/pathogen_hit.fasta".format(file_input)
os.system(seqtk1)

###Retrieval of the sequences that gave hit with the pathogen database
 
FastaFile = open('additional_files/pathogen_hit.fasta')
LenFile = open('additional_files/pathogen_lenghth.csv', 'w')

for name, seq in SimpleFastaParser(FastaFile):
    seqLen = len(seq)
    LenFile.write(name + ',' + str(seqLen) + '\n')

FastaFile.close()
LenFile.close()




###Megablast of retrieved sequences from pathogen run with the Commensal database 
print("Megablast with commensal database")
megablast_com_database = "wsl blastn -query additional_files/pathogen_hit.fasta -db database/commensal -out additional_files/query_commensal.list -outfmt '6 qseqid' -evalue 1e-100 -max_target_seqs 1 -perc_identity 75 -qcov_hsp_perc 90 -task megablast".format(file_input)
os.system(megablast_com_database)
seqtk2 = "wsl seqtk subseq additional_files/pathogen_hit.fasta additional_files/query_commensal.list > additional_files/commensal_hit.fasta".format(file_input)
os.system(seqtk2)




FastaFile = open('')
LenFile = open('./data/lengths.csv', 'w')

for name, seq in SimpleFastaParser(FastaFile):
    seqLen = len(seq)
    LenFile.write(name + ',' + str(seqLen) + '\n')

FastaFile.close()
LenFile.close()

###Removal of the sequences that gave in the Commensal BLASTY run 
# get the IDs in commensal_hit.fasta
commensal_ids = set([rec.id for rec in SeqIO.parse('additional_files/commensal_hit.fasta', 'fasta')])
# get entries unique to pathogen_hit.fasta
non_commensal = (rec for rec in SeqIO.parse('additional_files/pathogen_hit.fasta', 'fasta') if rec.id not in commensal_ids)
# write unique entries to new file: pathogen_unique.fna
with open('additional_files/non_commensal.fasta', 'w') as target:
    SeqIO.write(non_commensal, target, 'fasta')



###BLAST run of the non-coomensal sequence with the pathogen database
print("Megablast with pathogen database")
megablast_path_database_final = "wsl blastn -query additional_files/non_commensal.fasta -db database/pathogen -out additional_files/query_pathogen_final.csv -outfmt 6 -evalue 1e-100 -max_target_seqs 10 -perc_identity 85 -qcov_hsp_perc 95 -task megablast"
os.system(megablast_path_database_final)

###Removal of duplicates and sorting the results
df = pd.read_csv("additional_files/query_pathogen_final.csv", sep = "\t", names = ['query' , 'subject', 'identity', "Alignment lenth", "mismatches", "gap opens", "qstart", "qend", "s start", "s end", "evalue", "bitscore"])
#print(df)
df['subject'] = df['subject'].apply(lambda x: ' '.join(x.split('_')[:2]))
df = df.sort_values('query').drop_duplicates(subset=['query', 'subject'])
total = df['subject'].value_counts()
total.to_csv('additional_files/pathogen_final_result.csv')
#print(total)

df2 = pd.read_csv('additional_files/pathogen_final_result.csv', names = ['Pathogen', 'HITS'])
df2 = df2.iloc[1:]
df2['Relative Abundance(%)'] = (df2['HITS'].astype(float) / df2['HITS'].astype(float).sum()) * 100 
df2.to_csv('Final_result/pathogen_final_result.csv')
df2 = df2.round(2) 
print(df2)

strain = df2['Pathogen']
percentage = df2['Relative Abundance(%)']

###Ploting of the results
plt.rcdefaults()
fig, ax = plt.subplots()

ax.barh(strain, percentage)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Relative Abundance(%)')
ax.set_title('Gut Pathogens')
for i, v in enumerate(percentage):
    ax.text(v , i, str(v), color='blue', fontweight='bold')
plt.show()


os.system("rm generic.fastq")







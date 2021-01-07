echo |mkdir additional_files
echo |mkdir Final_result
printf '%s\n' "Converting FASTQ to FASTA"
echo |seqtk seq -a test.fastq > additional_files/test.fasta
printf '%s\n' "Removing Adapters" 
echo |porechop -i additional_files/test.fasta -o additional_files/test1.fasta
printf '%s\n' "Removing shorter sequences"
echo |seqtk seq -L 1000 additional_files/test1.fasta > additional_files/test_large_seq.fasta
printf '%s\n' "Megablast with pathogen database"
echo |blastn -query additional_files/test_large_seq.fasta -db database/pathogen -out additional_files/query_pathogen.csv -outfmt 6 -evalue 1e-100 -max_target_seqs 1 -perc_identity 85 -qcov_hsp_perc 95 -task megablast
printf '%s\n' "Megablast with commensal database"
echo |blastn -query additional_files/test_large_seq.fasta -db database/commensal -out additional_files/query_commensal.csv -outfmt 6 -evalue 1e-100 -max_target_seqs 1 -perc_identity 75 -qcov_hsp_perc 90 -task megablast
echo |python3 identityhit.py
printf '%s\n' "Gathering sequences similar to pathogen database"
echo |seqtk subseq additional_files/test.fasta additional_files/pathogen_query.list > additional_files/pathogen_hit.fasta
printf '%s\n' "Gathering sequences similar to commensal database"
echo |seqtk subseq additional_files/test.fasta additional_files/commensal_query.list > additional_files/commensal_hit.fasta
echo |python3 non_commensal.py
echo |cat additional_files/non_commensal.fasta additional_files/pathogen_hit.fasta > additional_files/pathogen_total.fasta
printf '%s\n' "Removing duplicate sequences"
echo |seqkit rmdup -s additional_files/pathogen_total.fasta > additional_files/pathogen_final.fasta
printf '%s\n' "Megablast with pathogen database"
echo |blastn -query additional_files/pathogen_final.fasta -db database/pathogen -out additional_files/query_pathogen_final.csv -outfmt 6 -evalue 1e-100 -max_target_seqs 10 -perc_identity 85 -qcov_hsp_perc 95 -task megablast
printf '%s\n' "Pathogen Hits"

echo |python3 pathogen_hit_count.py





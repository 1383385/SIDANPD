# SIDANPD(Under Development)
SIDANPD is an automated pipeline for detecting gut pathogen using sequence from ONT-Nanopore Sequencing(FASTQ)


Prerequisites:

BLAST+:

`sudo apt-get update`
`sudo apt-get install ncbi-blast+-legacy`

seqtk:

`sudo apt-get install seqtk`


porechop:

`sudo apt-get install porechop`

seqkit:

https://github.com/shenwei356/seqkit/releases

`sudo cp seqkit /usr/local/bin/`

Python dependencies:

`pip3 install pandas`
`pip3 install biopython`

# Usage

Download the database(https://drive.google.com/drive/folders/1RDWMOacKUAe29VoccGpOL7uASiMg264f?usp=sharing) files and put in the database folder.
Rename the fastq sequence to "test.fastq"

Run the following command:

`bash automate.sh`

# Results
`               Pathogen  HITS  Relative Abundance(%)
1    EHEC/STEC Pathogen  1310              31.680774
2         Shigella spp.   614              14.848851
3         UPEC Pathogen   591              14.292624
4         ETEC Pathogen   477              11.535671
5         EAEC Pathogen   461              11.148730
6         EPEC Pathogen   278               6.723096
7         STEC O113:H21   200               4.836759
8          EIEC O96:H19   188               4.546554
9   Salmonella enterica     6               0.145103
10        Yersinia spp.     6               0.145103
11          E. albertii     2               0.048368
12           Stx1 phage     2               0.048368`   

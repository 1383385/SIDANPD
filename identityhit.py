import pandas as pd 
df1 = pd.read_csv("additional_files/query_pathogen.csv", sep = "\t", names = ['query' , 'subject', 'identity', "Alignment lenth", "mismatches", "gap opens", "qstart", "qend", "s start", "s end", "evalue", "bitscore"])
df2 = pd.read_csv("additional_files/query_commensal.csv", sep = "\t", names = ['query' , 'subject', 'identity', "Alignment lenth", "mismatches", "gap opens", "qstart", "qend", "s start", "s end", "evalue", "bitscore"])
#print(df)
file1 = open('additional_files/pathogen_query.list', 'w')
file2 = open('additional_files/commensal_query.list', 'w')
df1 = df1[df1.identity >= 85]
df2 = df2[df2.identity >= 85]
names1 = df1["query"]
names2 = df2["query"]
#print(names)
for i in names1:
    file1.write(i + "\n") 
for j in names2:
    file2.write(j + "\n") 

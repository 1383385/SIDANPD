import pandas as pd 

df = pd.read_csv("additional_files/query_pathogen_final.csv", sep = "\t", names = ['query' , 'subject', 'identity', "Alignment lenth", "mismatches", "gap opens", "qstart", "qend", "s start", "s end", "evalue", "bitscore"])
#print(df)

df['subject'] = df['subject'].apply(lambda x: ' '.join(x.split('_')[:2]))
df = df.drop_duplicates(subset=['query', 'subject'])
total = df['subject'].value_counts()
total.to_csv('additional_files/pathogen_final_result.csv')
#print(total)

df2 = pd.read_csv('additional_files/pathogen_final_result.csv', names = ['Pathogen', 'HITS'])
df2 = df2.iloc[1:]
df2['Relative Abundance(%)'] = (df2['HITS'].astype(float) / df2['HITS'].astype(float).sum()) * 100 
df2.to_csv('Final_result/pathogen_final_result.csv')

print(df2)


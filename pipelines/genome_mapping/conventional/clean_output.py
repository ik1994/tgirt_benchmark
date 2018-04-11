#/usr/bin/env python

import pandas as pd
import os
import re

def read_genes_info():
    genes_bed = '/stor/work/Lambowitz/ref/benchmarking/human_transcriptome/genes.bed'
    return pd.read_table(genes_bed, 
                         usecols = [3,6,7],
                         names = ['name', 'type', 'id'])

def assign_rRNA(row):
    id = row['id']
    if row['type'] == 'rRNA':
        if '5S' in row['name']:
            id = '5S_rRNA' 
        elif '5-8S' in row['name'] or '5.8S' in row['name'] or '5_8S' in row['name']:
            id = '5.8S_rRNA'
        elif '18S' in row['name']:
            id = '18S_rRNA'
        elif '28S' in row['name']:
            id = '28S_rRNA'
    return id



project_path = os.environ['WORK'] + '/cdw2854/bench_marking_new/bench_marking/genome_mapping'
count_path = project_path + '/conventional/counts'

df = pd.read_table(count_path + '/counts.tsv',
        skiprows=1) 
df.columns = list(map(lambda x: os.path.basename(x.replace('.bam','')), df.columns))
df.columns = list(map(lambda x: x.replace('-','_'), df.columns))
df.drop(['Chr','Start','End','Strand','Length'], axis=1, inplace=True)
df.rename(columns = {'Geneid':'id'},inplace=True)
colnames = sorted(df.columns)
colnames.remove('id')
new_colnames = ['id']
new_colnames.extend(colnames)
df = df[new_colnames]
df['id'] = df['id'].str.replace('_gene$','')

tablename =count_path + '/feature_counts.tsv' 
df \
    .merge(read_genes_info(), on ='id', how = 'inner') \
    .assign(id = lambda d: [assign_rRNA(row) for i, row in d.iterrows()])\
    .drop(['name','type'], axis=1)\
    .to_csv(tablename, index=False, sep='\t')
print('Written %s' %tablename)


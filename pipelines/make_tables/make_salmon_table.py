#!/usr/bin/env python

import pandas as pd
import numpy as np
import glob
import ujson
import os
import re

def read_sample(sample_folder):
    samplename = os.path.basename(sample_folder)
    json_file = open(sample_folder + '/lib_format_counts.json')
    salmon = ujson.decode(json_file.read())
    df = pd.DataFrame({'variable':list(salmon.keys()),
                       'value':list(salmon.values())}) \
            .drop(6) \
            .assign(sample = samplename)
    return df

project_path = '/stor/work/Lambowitz/cdw2854/bench_marking_new/bench_marking'
datapath = project_path + '/alignment_free/salmon'
samples = glob.glob(datapath + '/Sample-*')
samples = list(filter(lambda x: re.search('001$',x), samples))
df = pd.concat(map(read_sample, samples), axis=0) \
    .query("value!=0") \
    .pipe(pd.pivot_table, index='sample', 
          columns = 'variable', values='value', 
          aggfunc=np.sum)  \
    .reset_index() \
    .sort_values('sample')  \
    .drop(['read_files','num_consistent_mappings'], axis=1)

tablename = project_path + '/tables/salmon_table.csv'
df['compatible_fragment_ratio'] = df['compatible_fragment_ratio'].map(lambda x: '%.3f' %float(x))
df.columns = df.columns.str.replace('_',' ')
df.rename(columns={'sample':'Sample name'}, inplace=True)
df.columns = df.columns.str.replace('num ','')
df = df[df.columns[~df.columns.str.contains('consistent|exp')]]
df.to_csv(tablename, index=False)
print('Written %s' %tablename)


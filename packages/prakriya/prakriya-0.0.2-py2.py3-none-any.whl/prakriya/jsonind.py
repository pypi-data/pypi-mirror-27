#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import json

inputdir = 'data/jsonsorted1'
filenames = glob.glob(os.path.join(inputdir, '*.json'))
outdir = 'data/json'
ind = {}
counter = 1
for filename in filenames:
    nm = filename.split('/')[-1].split('.')[0]
    print counter, nm
    ind[nm] = str(counter)
    with open(filename, 'r') as fin, open(os.path.join(outdir, str(counter) + '.json'), 'w') as fout:
        json.dump(json.load(fin), fout)
    counter += 1
with open('data/jsonindex.json', 'w') as indexfile:
    json.dump(ind, indexfile)

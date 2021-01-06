# -*- coding: utf-8 -*-
"""
Created on 06/01/2021

@author: XLGEO
"""
import glob
import os

inDelimiter = ' '
outDelimiter = ','
colNames = ['X','Y','Z']
Header = 'Y'
indir = r'D:\GitHubDownload\PyXYZ-main'
os.chdir(indir)
Ext = "*.xyz"
outfname = 'merge.csv'
outfile = open(outfname,'w')
if Header == 'Y':
    colNames = str(colNames)[1:-1].replace("'","").replace(', ',outDelimiter)
    outfile.write(str(colNames)+'\n')
list_all_file = glob.glob(Ext)
print(list_all_file)
for file in list_all_file:
    if file != 'merge.xyz':
        with open(file,'r') as infile:
            for line in infile:
                print(file,':',line)
                if line != '\n':
                    line = line.replace(inDelimiter,outDelimiter)
                    outfile.write(line)

outfile.close()

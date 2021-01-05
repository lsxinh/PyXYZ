# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2021

@author: XLGEO
"""
#%% 
import os
import sys
import glob
import pandas as pd
from datetime import datetime
from argparse import ArgumentParser
sys.path.append(os.path.join(os.path.dirname(__file__)))
# os.chdir(os.path.join(os.path.dirname(__file__)))
def main():
    stime = datetime.now()
    parser = ArgumentParser(description='Merge multiple point clouds xyz files into one file. Type in python py_mergeALLXYZ.py -i . to merge all point cloud file in this current working directory')
    parser.add_argument('-i',dest='inputfolder',type=str, metavar='', default='', help='input folder to process: eg. -i . for current folder')
    parser.add_argument('-on',dest='outName',type=str, metavar='', default='', help='Output name for merge point cloud file: eg. -on merge_out.xyz, default name is merge.xyz')
    parser.add_argument('-iExt',dest='Ext',type=str, metavar='', default='', help='Input point cloud file extention: eg. -iExt *.txt, default is *.xyz')
    parser.add_argument('-colN',dest='colNames',type=str, metavar='', default='', help='Output column names: eg. -colN E,N,Z, default: X,Y,Z')
    parser.add_argument('-hd',dest='Header',type=str, metavar='', default='', help='Output header for merged file or not: Y/N eg. -hd Y')
    parser.add_argument('-iDel',dest='inDelimiter',type=str, metavar='', default='', help='Input delimiter, eg. -idel , default is space,  t for tab, sp for space, : for colon, ; for semicolon')
    parser.add_argument('-oDel',dest='outDelimiter',type=str, metavar='', default='', help='Output delimiter, eg. -odel t, default is comma. t for tab, sp for space, : for colon, ; for semicolon')
    args = parser.parse_args()

    #input args check and print help
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #execute main program
    process(args)
    
    #time it
    print('Processing time: %s' % (datetime.now() - stime))
    print(100*'#'+'\n\n')

def process(args):
    if args.inputfolder == '.':
        args.inputfolder = os.getcwd()
        odir = newFolderF(args.inputfolder,'Merge')
    if not os.path.isdir(odir):
        os.makedirs(odir)
    if args.outName == '':
        args.outName = os.path.join(odir,'merge.xyz')
    elif args.outName != '':
        args.outName = os.path.join(odir,args.outName)
    if args.Ext == '':
        args.Ext = '*.xyz'
    if args.colNames == '':
        args.colNames = ['X','Y','Z']
    elif args.colNames != '':
        args.colNames = args.colNames.split(',')
    if args.Header == '':
        args.Header = 'Y'

    if args.inDelimiter == '':
        args.inDelimiter = ' '
    elif args.inDelimiter == 'sp':
        args.inDelimiter = ' '
    elif args.inDelimiter == 't':
        args.inDelimiter = '\t'

    if args.outDelimiter == '':
        args.outDelimiter = ','
        mergeXYZ_pd(args.inputfolder,args.outName,args.Ext,args.colNames,args.Header,args.inDelimiter)
    elif args.outDelimiter == 't':
        args.outDelimiter = '\t'
        print(args.inDelimiter)
        print(args.outDelimiter)
        mergeXYZ_py_large(args.inputfolder,args.outName,args.Ext,args.colNames,args.Header,args.inDelimiter,args.outDelimiter)
    elif args.outDelimiter == 'sp':
        args.outDelimiter = ' '
        mergeXYZ_py_large(args.inputfolder,args.outName,args.Ext,args.colNames,args.Header,args.inDelimiter,args.outDelimiter)
    else:
        mergeXYZ_py_large(args.inputfolder,args.outName,args.Ext,args.colNames,args.Header,args.inDelimiter,args.outDelimiter)
    
    print(f'New merged file: {args.outName}')

def mergeXYZ_pd(indir,outfname='merge.xyz',Ext="*.xyz",colNames=['X','Y','Z'],Header='Y',delimiter=' '):
    '''The default output delimiter is comma '''
    os.chdir(indir)
    fList=glob.glob(Ext)
    df_mergeList = list()
    for fname in fList:
        if fname != 'merge.xyz':
            # print(fname)
            df = pd.read_csv(fname,sep=' ',header=None)
            df_mergeList.append(df)
    df_merge = pd.concat(df_mergeList, axis=0) #row merge
    if Header=='Y':
        df_merge.columns = colNames
        df_merge.to_csv(outfname,index=None)
    else: 
        df_merge.to_csv(outfname,index=None,header=None)
        
#mergeXYZ_pd(os.getcwd(),outfname='merge.xyz',Ext="*.xyz",colNames=['X','Y','Z'],Header='N',delimiter=' ')

def mergeXYZ_py_large(indir,outfname='merge.xyz',Ext="*.xyz",colNames=['X','Y','Z'],Header='Y',inDelimiter=' ',outDelimiter=','):
    outfile = open(outfname,'w')
    colNames = str(colNames)[1:-2].replace("'","").replace(', ',outDelimiter)
    if Header == 'Y':
        outfile.write(colNames+'\n')
    else: pass
    list_all_file = glob.glob(Ext)
    for file in list_all_file:
        if file != 'merge.xyz':
            with open(file,'r') as infile:
                for line in infile:
                    line = line.replace(inDelimiter,outDelimiter)
                    if line != '\n': 
                        outfile.write(line)
                        print(line)
    outfile.close()

#mergeXYZ_py_large(os.getcwd(),outfname='merge.xyz',Ext="*.xyz",colNames=['X','Y','Z'],Header='Y',inDelimiter=' ',outDelimiter='\t')


def newFolderF(containFolder,newFolder='newFolder'):
    '''
    create new folder
    containFolder: the location of new created foler
    newFolder: new folder name
    Step 1: change dir to containFolder
    Step 2: check if the new folder is existed or not
    Step 3: if not make new folder using os.mkdir
    return the function result to new path.
    '''
    os.chdir(containFolder)
    if os.path.exists(containFolder+"\\"+newFolder): #if newFolder exists
        next
        #print ("Already exists:",containFolder+"\\"+newFolder)
    else:
        os.mkdir(newFolder)
    return containFolder+"\\"+newFolder #return the abspath

if __name__ == "__main__": 
	main()
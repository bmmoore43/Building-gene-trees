## genes2remove.py

'''
INPUT
		-oldgenes: list of all genes in fasta or orthogroup
		-newgenes: list of filtered genes in fasta or orthogroup
		-header: Does old gene list have header? T/F. Default is T. New gene list should not have header.
OUTPUT
	newgenesfile_genes2remove.txt: list of genes to remove from tree to be used as input into prune_tree.R
'''

import sys, os

#defaults
HEADER="T"

for i in range (1,len(sys.argv),2):

  if sys.argv[i] == '-oldgenes':
    oldfile = sys.argv[i+1]
  if sys.argv[i] == '-newgenes':
    newfile = sys.argv[i+1]
  if sys.argv[i] == '-header':
    HEADER = sys.argv[i+1]

def get_list(inp, list1, HEADER):
	if HEADER=="T":
		header= inp.readline()
		for line in inp:
			L=line.strip().split("\t")
			gene= L[0]
			list1.append(gene)
	else:
		for line in inp:
			L=line.strip().split("\t")
			gene= L[0]
			list1.append(gene)
	return list1
	
inp1= open(oldfile,'r')
list1=[]
list1=get_list(inp1,list1,HEADER)
print("old genes total:",len(list1))
inp2= open(newfile,'r')
list2=[]
HEADER="F"
list2=get_list(inp2,list2,HEADER)
print("new genes total:",len(list2))

out= open(str(newfile)+"_genes2remove.txt", "w")
for gene in list1:
	if gene in list2:
		pass
	else:
		out.write('%s\n' % gene)

inp1.close()
inp2.close()
out.close()


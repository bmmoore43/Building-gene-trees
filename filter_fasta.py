"""
PURPOSE:
To filter fasta files by length and by duplicate sequences.

INPUT:
	-fasta input one fasta file
	-dir Directory with all fasta files - looks for .fa or .fasta
	-bp number (integer) of basepairs or amino acid sequences. Below this number and gene is skipped.
		default is 3x standard deviations shorter than mean of sequence length

OPTIONAL:
	-save output file name
	
OUTPUT:
	output filtered fasta file 

"""
import sys, os
import pandas as pd
import numpy as np
import timeit
import Bio

start = timeit.default_timer()

# default parameters

startdir="none"
fa_file="none"
bp="stddev"

for i in range (1,len(sys.argv),2):

  if sys.argv[i] == '-dir':         #directory with promoter fastas for positive clusters
    startdir = sys.argv[i+1]
  if sys.argv[i] == '-fasta':         #fasta file for positive cluster (if just one)
    fa_file = sys.argv[i+1]
    SAVE = str(fa_file)+"_parsed.fa"
  if sys.argv[i] ==  '-bp':
    bp = fa_file = sys.argv[i+1]
  if sys.argv[i] == '-save':         #output name
    SAVE = sys.argv[i+1]

## functions

# remove unwanted characters in gene names
def remove_char(string):
	string = string.strip()
	while '"' in string:
		string = string.replace('"',"")
	while ':' in string:
		string = string.replace(':',"")
	while '(' in string:
		string = string.replace('(',"")
	while ')' in string:
		string = string.replace(')',"")
	while ',' in string:
		string = string.replace(',',"")
	while '  ' in string:
		string = string.replace('  '," ")
		string = string.replace(' ',"_")
	while '=' in string:
		string = string.replace('=','')
	return string

## read in fasta function
def read_fasta(fasta, D):
	from Bio import SeqIO
	from Bio.Seq import Seq
	from scipy import stats
  
	#Open fasta files
	f = open(fasta, 'r')
	#get sequence and length of sequence for each gene
	for seq_record in SeqIO.parse(f, 'fasta'): ###finding kmers in the fasta file
		#num_pos += 1
		gene = seq_record.id #gene ID
		gene= remove_char(gene)
		#genes.append(gene) # append all genes to list
		#print(genes)
		seq = str(seq_record.seq) # get sequence in fasta
		length= len(seq_record.seq)
		D[gene]= [seq, length]
	
	f.close()
	return D

## get standard deviation function
def get_std(D):
	from scipy import stats
	data = list(D.values())
	data2= [item[1] for item in data]
	x_array = np.array(data2)
	#print(x_array)
	std= stats.tstd(x_array)
	print('stdev of gene lengths: ', std)
	mn= stats.tmean(x_array)
	print("mean of gene lengths: ", mn)
	x= mn-3*std
	print("cutoff mean-3*std: ", x)
	return x

## remove duplicate genes
def remove_dups(D):
	temp = [] 
	list2 = []
	res = dict() 
	for key, val in D.items(): 
		if val[0] not in temp: 
			temp.append(val[0]) 
			res[key] = val
		else:
			list2.append(key)
	return res, list2


## get input fastas
fasta_D={}
if startdir != "none" and fa_file=="none":
	for file in os.listdir(startdir):
		if file.endswith(".fa"):
			fa_file= str(startdir)+"/"+str(file)
			fasta_D = read_fasta(fa_file, fasta_D)

		elif file.endswith(".fasta"):
			fa_file= str(startdir)+"/"+str(file)
			fasta_D = read_fasta(fa_file, fasta_D)

else:
	fasta_D = read_fasta(fa_file, fasta_D)
	
print("number of genes in fasta:", len(fasta_D))

x= get_std(fasta_D)
## 
## filter fasta and write output
output= open(SAVE,"w")
fasta_D, list2= remove_dups(fasta_D)
print("number of genes in fasta after dups removed:", len(fasta_D))
print("genes removed", list2)
for gene in fasta_D:
	dataall=fasta_D[gene]
	seq= dataall[0]
	length= dataall[1]
	if bp == 'stddev':
		if int(length) < float(x):
			print(gene, " removed because too short, less than ", x)
		else:
			output.write('>%s\n%s\n' % (gene, seq))
	else:
		if int(length) < float(bp):
			print(gene, " removed because too short, less than ", bp)
		else:
			output.write('>%s\n%s\n' % (gene, seq))

stop = timeit.default_timer()
print('Run time: %.2f min' % ((stop-start)/60))

output.close()


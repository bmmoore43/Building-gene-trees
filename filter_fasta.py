"""
PURPOSE:
To filter fasta files by length and by duplicate sequences.

INPUT:
	-fasta input one fasta file
	-dir Directory with all fasta files - looks for .fa or .fasta
	-bp number (integer) of basepairs or amino acid sequences. Below this number and gene is skipped.
		default is 3x standard deviations shorter than mean of sequence length
	-stdv number (integer) of std deviations from mean length that you want to remove genes. Above and below this length gene is removed

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
STDEV=''

for i in range (1,len(sys.argv),2):

  if sys.argv[i] == '-dir':         #directory with promoter fastas for positive clusters
    startdir = sys.argv[i+1]
  if sys.argv[i] == '-fasta':         #fasta file for positive cluster (if just one)
    fa_file = sys.argv[i+1]
    SAVE = str(fa_file)+"_filter.fa"
  if sys.argv[i] ==  '-bp':
    bp = sys.argv[i+1]
  if sys.argv[i] == '-stdv':
    STDEV= int(sys.argv[i+1])
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
def read_fasta(fasta, D, charlist):
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
		if gene.startswith("Aco"):
			first_chars = gene[0:4]
		else:
			first_chars = gene[0:5]
		#genes.append(gene) # append all genes to list
		#print(genes)
		seq = str(seq_record.seq) # get sequence in fasta
		length= len(seq_record.seq)
		D[gene]= [seq, length]
		if first_chars not in charlist:
			charlist.append(first_chars)
	
	f.close()
	return D, charlist

## get standard deviation function
def get_std(D, z):
	from scipy import stats
	data = list(D.values())
	data2= [item[1] for item in data]
	x_array = np.array(data2)
	#print(x_array)
	std= stats.tstd(x_array)
	print('stdev of gene lengths: ', std)
	mn= stats.tmean(x_array)
	print("mean of gene lengths: ", mn)
	x= mn-z*std
	y= mn+z*std
	if x < 0:
		print('z*stdev is greater than mean. Trying stdev*mean only.')
		x=mn-std
		if x < 0:
			print("stdev is greater than mean, try giving bp cutoff")
			x='NA'
	print("cutoff mean-/+z*std: ", x,y)
	return x,y

## remove duplicate genes
def remove_dups(D,charlist):
	list2 = []
	res = dict()
	for ch in charlist:
		temp = []
		list1=[]  
		for key, val in D.items(): 
			if key.startswith(ch):
				if val[0] not in temp:  # get only unique sequences
					temp.append(val[0]) # sequence list of unique sequences
					list1.append(key) # gene list of unique sequences
				else:
					list2.append(key) # gene list of redundant sequences
# remove partial dups and get longest sequence
		for key in list1: # for gene in unique sequences
			val= D[key] # get sequence
			part_dup=[]
			for t in temp: # for seq in sequence list
				if val[0] in t: # if gene seq is in seq
				#print(val[0],t)
					part_dup.append(t) # append as partial duplicate to duplicate seq list
				else:
					if val[0] not in part_dup:
						part_dup.append(val[0]) # include gene sequence here
		# Longest String in list 
		# using max() + key 
			string = max(part_dup, key = len) # find the longest sequence from duplicate seq list
			if string == val[0]: # if this longest seq is your gene, keep
				res[key]=val
			else: # else do not add to result, add to remove list
				list2.append(key)
			
	return res, list2
## 
## filter fasta and write output
def writeout(fasta_D, x, y, bp, SAVE, D2, charlist, filename):
	output= open(SAVE,"w")
	print("number of genes in fasta:", len(fasta_D))
	fasta_D, list2= remove_dups(fasta_D, charlist)
	print("number of genes in fasta after dups removed:", len(fasta_D))
	print("duplicate/ partial duplicate genes removed", list2)
	D2[filename]={}
	for gene in fasta_D:
		dataall=fasta_D[gene]
		seq= dataall[0]
		length= dataall[1]
		if bp == 'stddev':
			if x != 'NA':
				if int(length) < float(x):
					print(gene, " removed because too short, less than ", x)
				elif int(length) > float(y):
					print(gene, " removed because too long, more than ", y)
				else:
					output.write('>%s\n%s\n' % (gene, seq))
					for ch in charlist:
						if gene.startswith(ch):
							if ch not in D2[filename]:
								D2[filename][ch]=[gene]
							else:
								D2[filename][ch].append(gene)
			else:
				if int(length) > float(y):
					print(gene, " removed because too long, more than ", y)
				else:
					output.write('>%s\n%s\n' % (gene, seq))
					for ch in charlist:
						if gene.startswith(ch):
							if ch not in D2[filename]:
								D2[filename][ch]=[gene]
							else:
								D2[filename][ch].append(gene)
		else:
			if int(length) < float(bp):
				print(gene, " removed because too short, less than ", bp)
			else:
				output.write('>%s\n%s\n' % (gene, seq))
				for ch in charlist:
						if gene.startswith(ch):
							if ch not in D2[filename]:
								D2[filename][ch]=[gene]
							else:
								D2[filename][ch].append(gene)
	output.close()
	return D2


## get input fastas

D2={}
charlist=[]
if startdir != "none" and fa_file=="none":
	for file in os.listdir(startdir):
		fasta_D={}
		if file.endswith(".fa"):
			fa_file= str(startdir)+"/"+str(file)
			print(str(file))
			SAVE= str(file)+"_filter.fa"
			fasta_D,charlist = read_fasta(fa_file, fasta_D, charlist)
			if STDEV != '':
				x,y= get_std(fasta_D,STDEV)
			else:
				x,y= get_std(fasta_D,3)
			D2= writeout(fasta_D, x, y, bp, SAVE, D2, charlist, str(file))
		elif file.endswith(".fasta"):
			fa_file= str(startdir)+"/"+str(file)
			print(str(file))
			SAVE= str(file)+"_filter.fa"
			fasta_D,charlist = read_fasta(fa_file, fasta_D, charlist)
			if STDEV != '':
				x,y= get_std(fasta_D,STDEV)
			else:
				x,y= get_std(fasta_D,3)
			D2= writeout(fasta_D, x, y, bp, SAVE, D2, charlist, str(file))

else:
	fasta_D={}
	fasta_D,charlist = read_fasta(fa_file, fasta_D, charlist)
	if STDEV != '':
			x,y= get_std(fasta_D,STDEV)
	else:
		x,y= get_std(fasta_D,3)
	D2= writeout(fasta_D, x, y, bp, SAVE, D2, charlist, str(fa_file))

# write out gene count per species
print(D2)
out= open("filtered_count_matrix.txt","w")
charstr="\t".join(charlist)
out.write("file\t%s\n" % charstr)
for f, f_info in D2.items():
	print(f)
	out.write('%s\t' % f)
	for ch in charlist:
		if ch in f_info.keys():
			genes= f_info[ch]
			out.write('%i\t' % len(genes))
		else:
			out.write('%i\t' % 0)
	out.write('\n')
out.close()
# for p_id, p_info in people.items():
#     print("\nPerson ID:", p_id)
#     
#     for key in p_info:
#         print(key + ':', p_info[key])

stop = timeit.default_timer()
print('Run time: %.2f min' % ((stop-start)/60))



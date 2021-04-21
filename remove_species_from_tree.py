# remove species name from tree
import sys

inptree = open(sys.argv[1],"r").readlines()
speciesl = open(sys.argv[2],"r")

print(inptree)
sp_list=[]
def cleardots(string):
	while "." in string:
		string= string.replace(".","_")
	return string

for sp in speciesl:
	#print(sp)
	sp =sp.strip().split("\t")[0]
	if sp.startswith("#"):
		pass
	else:
		sp= sp.split(": ")[1]
		if sp.endswith("mod.fa"):
			sp= sp.replace("mod.fa","mod_")
		elif sp.endswith("fasta"):
			sp= sp.replace("fasta","")
		else:
			print(sp, "not adjusted")
		sp= cleardots(sp)
		sp_list.append(sp)
		
print(sp_list)

inptreestr= "\t".join(inptree)
for i in sp_list:
	while i in inptreestr:
		inptreestr = inptreestr.replace(i,"")

out= open(sys.argv[1]+"_mod.txt", "w")
print(inptreestr)
out.write(inptreestr)
out.close()
speciesl.close()
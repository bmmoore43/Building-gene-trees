# Building-gene-trees
Methods for building gene trees

1. For basic gene tree building or if completely new to gene trees see https://github.com/HiroshiLab/Building-Gene-Trees-workshop-1.
2. Finding homologous genes via local alignment. Normally I start with Orthofinder, then if I need to add in other species the quickest way is to add genes via BLAST. You can also add genes via Orthofinder.

   a. By BLAST (download latest version here: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
  
   1. Make BLAST database. Note for program commands, if you are a Windows user you will need to add .exe. So makeblastdb would be makeblastdb.exe
    
          ncbi-blast-2.10.0+/bin/makeblastdb -in <fasta file> -dbtype <prot or nucl>
      
   2. Run BLAST with query sequence (your gene or genes) against the database. Function blastp is for protein sequences, blastn is for nucleotide. Add flag -evalue for a specific evalue cutoff.
      
          ncbi-blast-2.10.0+/bin/blastp -db <fasta file from database> -query <query fasta file> -out <output name> -outfmt 6
          
   3. The result is a list of genes that significantly match your query sequence.
  
   b. By Orthofinder
   
   1. For complete instructions see: https://github.com/davidemms/OrthoFinder.
   
   2. Easiest install is if you have anaconda (https://www.anaconda.com/products/individual). This allows you to easily install in the command line.
   
          conda install orthofinder
          
   3. To run: Note this can take hours or days depending on your computer and how many fastas you have. It is recommended that you run on a cluster such as the UW chtc.
   
        Check if your installation worked by running sample data:
        
          OrthoFinder/orthofinder -f OrthoFinder/ExampleData
          
        If this works then run with your fasta files. First put all fasta files in one directory
        
          mkdir my_fasta_files
          
          mv *.fa my_fasta_files
          
        Next run with your directory as input
        
          OrthoFinder/orthofinder -f my_fasta_files/
          
    4. Orthofinder can be run from different steps. If your run does not complete, but has run partially, you can try restarting from different steps (see https://github.com/davidemms/OrthoFinder).
     
       To restart after BLASTs complete: ('previous_orthofinder_directory' is the OrthoFinder 'WorkingDirectory/' containing the file 'SpeciesIDs.txt'.)
        
            orthofinder -b previous_orthofinder_directory
          
    5. Result files needed:
    
       You should get a list of orthogroups and the genes they contain in **Orthogroups.tsv**. Search for your gene in this file and then all the genes in its orthogroups would be the gene's homologs. You can also check out the tutorial for looking at results: https://davidemms.github.io/orthofinder_tutorials/exploring-orthofinders-results.html
   
3. Checking genes with Fasttree and removing duplicates/ fragmented genes.

   a. Install Fasttree (http://www.microbesonline.org/fasttree/)
   
   1. Install Fasttree using conda
      
           conda install -c bioconda fasttree
           
   2. Check installation by running
   
           Fasttree
   
   This should give you a list of options.
   
   b. Align your fasta file using MAFFT
   
   1. Check if MAFFT is installed. If not installed, follow previous instructions in https://github.com/HiroshiLab/Building-Gene-Trees-workshop-1
   
            which mafft
            
   2. Run MAFFT to align fasta
   
            mafft --auto --anysymbol [fasta file] > [output]
            
   3. Use output alignment file to run Fasttree
   
   c. Run Fasttree- this should be relatively fast (seconds to minutes)
   
   1. For protein alignments:
   
            FastTree alignment.file > tree_file
            
   2. For nucleotide alignments:
   
            FastTree -gtr -nt alignment_file > tree_file
            
   3. Fasttree output is in Newick format. Check tree for very close/ overlapping leaves of the same species as well as leaves that are very long. Very close leaves may indicate sequence duplicates (these are likely due to sequencing errors and not actual duplicates), or multiple fragmented sequences of the same gene. Very long leaves could indicate very divergent sequences or genes that are perhaps not orthologous.
   
   d. Run filter fasta- this script removes duplicate genes and genes shorter than 3x standard deviation from the mean- or a given length (input from the user)
   
            python filter_fasta.py -fasta <fasta file> 
            
            other options: -dir <directory of fasta files> -bp <genes you want to remove that are shorter than this length- an interger> -save <output file name>
            
  e. Rerun alignment and fasttree with new filtered fasta. Recheck tree in Dendroscope, compare to previous. If genes still stick out then check the alignment. Use Sequence Manipulation Suite (SMS) https://www.bioinformatics.org/sms2/ and the color align program to check your fasta file for weird genes.
   
4. Running tree using RAxML on CHTC. For this step you will need a CHTC account. You will also need to download the raxml script to the chtc.
   Find latest RAxML download: https://github.com/stamatak/standard-RAxML

  a. Transfer alignment file to chtc. Note you may be on a different submit server, use the address of your account.
  
            scp <file name> username@submit2.chtc.wisc.edu:
            
  b. Set up submit file: This file tells chtc how to run your job.
  
  1. Create the submit file:
  
            nano raxml_job.sub
            
  2. Add options. Be sure to put in your alignment files as input. Example submit file:
  
            # raxml.sub
            ##
            # Specify the HTCondor Universe (vanilla is the default and is used
            #  for almost all jobs), the desired name of the HTCondor log file,
            #  and the desired name of the standard error file.  
            #  Wherever you see $(Cluster), HTCondor will insert the queue number
            #  assigned to this set of jobs at the time of submission.
            universe = vanilla
            log = raxmlPTALmono_$(Cluster).log
            error = raxmlPTALmono_$(Cluster)_$(Process).err
            output = raxmlPTALmono_$(Cluster)_$(Process).out
            ##
            # Specify your executable (single binary or a script that runs several
            #  commands), arguments, and a files for HTCondor to store standard
            #  output (or "screen output").
            #  $(Process) will be a integer number for each job, starting with "0"
            #  and increasing for the relevant number of jobs.
            # Here we specify the command raxml.sh and arguments which refer to the number of cpus to use
            executable = raxml.sh
            arguments = $(request_cpus)
            ##
            # Specify that HTCondor should transfer files to and from the
            # computer where each job runs. Here we transfer the alignment
            # file and the raxml program
            should_transfer_files = YES
            when_to_transfer_output = ON_EXIT
            transfer_input_files = alignment_file,standard-RAxML.tar.gz 
            ##
            #  Tell HTCondor what amount of compute resources
            #  each job will need on the computer where it runs.
            #  For large trees use 16 cpus, smaller trees can use 8 or 4
            request_cpus = 16
            request_memory = 2GB
            request_disk = 1GB
            ##
            # If job runs over 72 hours, you will need to specify a Long job:
            # +LongJob = true
            ##
            # Tell HTCondor to run 1 instances of our job:
            queue 1
            
  c. Set up the executable file. This file contains the RAxML command. This can vary based on how you want to run your RAxML job. 
  
  1. Example 1: Running RAxML on a protein alignment with specific outgroups:
  
           #!/bin/bash
            tar -xzf standard-RAxML.tar.gz

            standard-RAxML/raxmlHPC-PTHREADS -T $1 -n <tree file name> -f a -x <random 5 digit number> -p <random 5 digit number> -N 100 -m PROTGAMMAJTT -s <alignment file> -o <outgroup_gene1,outgroup_gene2>
            
   2. Example 2: Running RAxML on a cds alignment with outgroups:
   
           #!/bin/bash
           tar -xzf standard-RAxML.tar.gz

           standard-RAxML/raxmlHPC-PTHREADS -T $1 -n <tree file name> -f a -x <random 5 digit number> -p <random 5 digit number> -N 100 -m GTRGAMMA -s <alignment file> -o <outgroup_gene1,outgroup_gene2>
           
   3. Example 3: Running RAxML with guide tree:
   
            #!/bin/bash
            tar -xzf standard-RAxML.tar.gz
            tar -xzf data.tar.gz

            standard-RAxML/raxmlHPC-PTHREADS -T $1 -n <tree file name> -f t -p <random 5 digit number> -N 100 -m PROTGAMMAJTT -s <alignment file> -t <guide tree>
            
      After this runs, you get 100 separate trees. Trees need to combined to form a consensus tree. The next steps can all be done on your computer.
      First concatenate all output trees into one file:
      
            cat RAxML_output_tree* > all_trees_file
            
      Next use RAxML to combine the all_trees_file:
      
            standard-RAxML/raxmlHPC-PTHREADS -n <consensus tree file name> -J MRE -m PROTGAMMAJTT -z <all_trees_file> -T 2 -N 100 
            
      Re-evaluate consensus tree to get branch lengths:
      
            standard-RAxML/raxmlHPC-PTHREADS -T 2 -n <output file name> -f e -m PROTGAMMAJTT -s <alignment file> -t <ConsensusTree>
            
      Add back in bootstrap values:
      
            standard-RAxML/raxmlHPC-PTHREADS -T 2 -n <output file name> -f b -m PROTGAMMAJTT -t <evaluated ConsensusTree> -z <all_trees_file>
      
            
            

   
      
           
           

  

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
          
    4. Orthofinder can be run from different steps. If your run does not complete, but has run partially, you can try restarting from different steps.
     
       To restart after BLASTs complete: ('previous_orthofinder_directory' is the OrthoFinder 'WorkingDirectory/' containing the file 'SpeciesIDs.txt'.)
        
            orthofinder -b previous_orthofinder_directory
          
    5. Result files needed:
    
       You should get a list of orthogroups and the genes they contain in **Orthogroups/Orthogroups.txt**. Search for your gene in this file and then all the genes in its orthogroups would be the gene's homologs. The Orthofinder tree for your Orthogroup can be found in **Resolved_Gene_Trees/**. This tree can be used as a guide tree for building your maximum likelihood tree later on, or can just be visualized using FigTree or Dendroscope to find outgroups.
       
       You can also check out the tutorial for looking at results: https://davidemms.github.io/orthofinder_tutorials/exploring-orthofinders-results.html.
   
3. Checking genes with Fasttree. FastTree infers approximately-maximum-likelihood phylogenetic trees from alignments of nucleotide or protein sequences. If you want to get a guide tree from your alignment or just want to get a fast tree, this is a good program for getting approximate ML phylogenetic trees.

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
   
            FastTree -gtr -nt alignment_file > fasttree_file
            
   3. Fasttree output is in Newick format. Check tree using Dendroscope or other tree visualization programs for very close/ overlapping leaves of the same species as well as leaves that are very long. Very close leaves may indicate sequence duplicates (these are likely due to sequencing errors and not actual duplicates), or multiple fragmented sequences of the same gene. Very long leaves could indicate very divergent sequences or genes that are perhaps not orthologous.
   
   d. Run tree shrink to get rid of divergent sequences that are likely not part of the gene family.
   
   1. Check if you have python and R. If not they should be installed on your computer.
            
            python3 --version
            
            R --version
            
   2. TreeShrink can be downloaded here: https://github.com/uym2/TreeShrink
   
   3. Untar and run tree shrink.
   
            tar -xzf TreeShrink.tar.gz
            
            python3 TreeShrink/run_treeshrink.py -t fasttree_file
   
4. Filter your fasta file to get rid of duplicates, partial duplicates, or genes of spurious length.

   1. Run filter fasta- this script removes duplicate genes and genes shorter than 3x standard deviation from the mean- or a given length (input from the user)
   
            python filter_fasta.py -fasta <fasta file> 
            
            other options: -dir <directory of fasta files> -bp <genes you want to remove that are shorter than this length- an interger> -stdv <number of standard deviations for cutoff- both length over and under> -save <output file name>
            
     if you run on a directory, filter_fasta.py looks for files that end in .fa or .fasta. Script will also ouput a "filtered_count_matrix.txt" that gives the post-filtered gene count of each species for each fasta file.
     
            python filter_fasta.py -dir <directory> -bp [or] -stdv
            
  2. Rerun alignment and fasttree with new filtered fasta. Recheck tree in Dendroscope, compare to previous. If genes still stick out then check the alignment. Use Sequence Manipulation Suite (SMS) https://www.bioinformatics.org/sms2/ and the color align program to check your fasta file for weird genes.

   For many fastas, you can rerun alignment in a loop:
   
            for i in *filter.fa; do echo $i; name="${i}"; file_output="${name}.aln"; echo ${file_output}; mafft --auto --anysymbol $i > ${file_output}; done

5. Finding the best evolutionary model using ModelTest (https://github.com/ddarriba/modeltest). The evolutionary model affects how your tree is built because it determines the rate in which nucleotides or amino acids are substituted, and the frequency in which they occur- thus affecting branch length, distances, and likelihood of a tree. The best evolutionary model can vary across enzyme families and is dependent on what taxa are included.
   
   a. install modeltest using git
   
      i.	clone modeltest repository

            git clone https://github.com/ddarriba/modeltest
            
      ii. install dependencies
      
      for PC or Debian-based systems:
      
            sudo apt-get install flex bison
            
      for mac:
      
      First make sure homebrew (https://brew.sh/) is installed. Try:
      
            brew
            
      if you get a list of commands using brew, then it is installed. 
      
      if not found, then install
      
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      
      Get dependencies using brew:
      
            brew install flex bison
            
      iii. build
      
      Need to install cmake if you don't have it: https://cmake.org/install/
      
      for mac download: cmake-3.20.0-macos-universal.tar.gz
      
      untar:
      
            tar -xvzf cmake-3.20.0-macos-universal.tar.gz
            
     in modeltest folder make build folder and go to build 

            mkdir build && cd build
            
     call cmake from wherever it was downloaded
     
            ~/Desktop/Github/cmake-3.20.0-macos-universal/CMake.app/Contents/bin/cmake ..
            
     Now make
     
            make
            
     Result: Linking CXX executable. Modeltest-ng should be in bin folder within Github folder
     
            /Users/Beth/Desktop/Github/modeltest/bin/modeltest-ng
            
     iv. Run
     
     To see input options: https://github.com/ddarriba/modeltest/wiki/Command-line
     
     Try on example data (this can be found within Github folder):
     
           ./bin/modeltest−ng −i example−data/dna/tiny.fas -t ml
           
     On amino acid data: -i <alignment file> -d <indicates data type: aa= amino acid> -p <number of cpus to use> -t <type of tree to build for each model: ml= max. likelihood>
     
            /Github/modeltest/bin/modeltest-ng -i <aln_file> -t ml -d aa -p 2

     Check only specific model types (add -m)
     
            Github/modeltest/bin/modeltest-ng -i <aln_file> -t ml -d aa -m JTT,JTT-DCMUT -p 2

      v. Run on chtc
      
      Downlaod modeltest_install.tar.gz from Beth
      
      Set up run:
      
      Sub file:
      
           modeltest_loop.sub or modeltest1.sub

      sh file:
      
           modeltest.sh or modeltest1.sh
      
      
6. Setting up and running raxml-ng locally.

   

7. Running tree using RAxML-ng on CHTC. For this step you will need a CHTC account. You will also need to download the raxml script to the chtc.
   
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
   
   
   
8. Running old version of standard RAxML:   
Find latest RAxML download: https://github.com/stamatak/standard-RAxML

  
  
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
      
            
            

   
      
           
           

  

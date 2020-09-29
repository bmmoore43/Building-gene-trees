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

  

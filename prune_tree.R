#drop.tip removes the terminal branches of a phylogenetic tree, possibly removing the corresponding internal branches.
#options: 
## phy	
# an object of class "phylo".
## tip	
# a vector of mode numeric or character specifying the tips to delete.
## trim.internal	
# a logical specifying whether to delete the corresponding internal branches.
## subtree	
# a logical specifying whether to output in the tree how many tips have been deleted and where.
## root.edge	
# an integer giving the number of internal branches to be used to build the new root edge. This has no effect if trim.internal = FALSE.
## rooted	
# a logical indicating whether the tree must be treated as rooted or not. This allows to force the tree to be considered as unrooted (see examples).
## collapse.singles	
# a logical specifying whether to delete the internal nodes of degree 2.
## node	
# a node number or label.
## interactive	
# if TRUE the user is asked to select the tips or the node by clicking on the tree which must be plotted.
################################################################################
# First get vector of tips to drop
nc= "PMT_grplant_Feb19_filter_stdv2.fa_genes2remove.txt"
p2<-read.table(nc, sep='\t') 
p2
tip <- p2$V1 # where V1 is column name with tips
tip
# Next read in tree
library(ape) #CRAN package
phy <- read.tree("OG0000871_tree.txt_mod.txt")
phy
# now get new tree with pruned tips
newphy<- drop.tip(phy, tip, trim.internal = TRUE, subtree = FALSE,
         root.edge = 0, rooted = is.rooted(phy), collapse.singles = TRUE,
         interactive = FALSE)
newphy
write.tree(newphy, file = "OG0000871_tree.txt_mod_stdv2.txt", append = FALSE,
           digits = 6, tree.names = FALSE)

#quick plot:
plot(newphy, type = "phylogram", use.edge.length = TRUE,
     node.pos = NULL, show.tip.label = TRUE,cex=.5)

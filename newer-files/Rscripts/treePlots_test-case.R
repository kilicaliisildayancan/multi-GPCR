##learning to plot

library(treedataverse)

taxidList <- c(9593,
               9598,
               9606,
               63221,
               499232)
someAttri1 <- c("Big",
                "Very Big",
                "Meh",
                "Medium",
                "Small")

mydbTax <- taxize::classification(taxidList, db = "ncbi")

treeInit <- taxize::class2tree(mydbTax)

treeInit$classification$genus[treeInit$names == '9606'] #genus that match taxid '9606'


treeData <- treeInit$phylo
treeData$edge.length <- treeData$edge.length # this does change the plot if geom_treescale is used

ggtree(treeData) +
  xlim(0, max(treeData$edge.length)+30) + #this fixes the length problem
  geom_tree() +
  geom_tiplab() +
  geom_label()



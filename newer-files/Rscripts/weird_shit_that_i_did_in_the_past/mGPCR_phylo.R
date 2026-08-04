#get libraries
library(treedataverse)

#import JSON database
Tax_ID <-c(6657, 113540, 8457, 46731, 30732, 43150, 202257, 175121, 7957, 8469, 46360, 56216, 8218, 7067, 419612, 175774, 240159, 7070, 6689, 1594786, 123683, 84645, 246437, 9126, 52904, 400682, 9770, 8112, 13489, 133434, 48698, 32443, 495550, 215358, 885580, 9685, 8022, 40151, 7897, 8665, 7906, 7399, 36200, 8168, 77932, 7917, 33528, 9083, 50429)

TaxID <- unique(Tax_ID)

mydbTax <- taxize::classification(TaxID, db = "ncbi")
speciesFull <- taxize::class2tree(unique(mydbTax))

speciesClass <- speciesFull$classification$class
speciesPhylum <- speciesFull$classification$phylum

speciesTree <- treeio::as.treedata(speciesFull$phylo)

speciesTree <- as.treedata(speciesTree)

ggtree(speciesTree)
p1 <- speciesTree %>% ggtree() +
  geom_tiplab(offset =0) +
  geom_nodelab(geom = "label") +
  theme(legend.position = "right")

p1
viewClade(p1, MRCA(p1, "Actinopteri"))




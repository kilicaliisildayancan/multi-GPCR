library('ggtree')
library('ggplot2')
direcPhylo1 <- '/home/kilic_tp/multi-domain_gpcr/phylo/unrankedTaxaInc.phy'
direcPhylo2 <- '/home/kilic_tp/multi-domain_gpcr/phylo/phyliptree.phy'

readFile1 <- ape::read.tree(direcPhylo1)
readFile2 <- ape::read.tree(direcPhylo2)
p1 <- ggtree(readFile1) + geom_tiplab(offset = 0.1 )+ xlim(0, 100)
p1 + geom_nodelab(geom = 'label')


p2 <- ggtree(readFile2) + geom_tiplab(offset = 0.1)
p2 + geom_nodelab(geom = 'label', fill = 'lightblue') + xlim(0, 20)

edges <- data.frame(readFile2$edge, edge_num = 1:nrow(readFile2$edge))
colnames(edges)=c("parent", "node", "edge_num")
p2 %<+% edges + geom_label(aes(x=branch, label=edge_num)) + geom_tiplab() + xlim(0,60)


p2 + geom_cladelab(node = 65, geom = 'label', label = 'some clade', color = 'red', barsize = 10,
                   align = TRUE, offset = 2) + xlim(0, 30)


readFile2$edge
readFile2$node.label == 'Mammalia'

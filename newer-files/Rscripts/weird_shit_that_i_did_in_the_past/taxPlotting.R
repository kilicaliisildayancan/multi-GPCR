library('ggtree')
library('ggplot2')
library('ggimage')
direcPhylo <- '/home/kilicali/multi-domain_gpcr/focus_chemokines/chemokines_preliminary.tsv'
direcImage <- '/home/kilicali/multi-domain_gpcr/focus_chemokines/trees'

filePhylo <- read.csv(direcPhylo, sep = '\t')
name <- filePhylo$Name
domainCount <- filePhylo$HitCount
taxidCol <- c(as.numeric(filePhylo$TaxID))

taxDB <- taxize::classification(taxidCol, db = 'ncbi')

speciesTree <- taxize::class2tree(unique(taxDB))
speciesTree <- speciesTree$phylo
allSpecies <- speciesTree$tip.label
commNames <- taxize::sci2comm(filePhylo)
commNames <- as.character(commNames)
commNames[commNames == 'character(0)'] <- 'DNE'
speciesTree$tip.label <- commNames

speciesTree <- treeio::as.treedata(tidytree::as_tibble(speciesTree))

#layout roundrect
p <- ggtree(speciesTree) + geom_tiplab(offset = .1, size = 6.5)


edges <- data.frame(speciesTree$edge, edge_num = 1:nrow(speciesTree$edge))
colnames(edges)=c("parent", "node", "edge_num")
p %<+% edges + geom_label(aes(x=branch, label=edge_num)) + xlim(0,100)

p + geom_label(aes(x=branch, label=S), fill='lightgreen')


geom_label(aes(label=D), fill='steelblue') +
  geom_text(aes(label=B), hjust=-.5)

#Data prep
imageData <- data.frame(x = c(77, 84, 81, 84.5, 77, 79, 81, 81, 79, 81, 86, 85, 81, 84, 81, 83, 83, 81),
                        y = c(63.5, 63.5, 60.5, 58, 57.5, 53, 50, 48, 44.7, 40, 37, 34, 31, 25, 18, 13, 7, 1.5),
                        image = c(paste0(direcImage, "/camelus.png"), paste0(direcImage, "/bos.png"),
                                  paste0(direcImage, "/balaenoptera.png"), paste0(direcImage, "/lynx.png"),
                                  paste0(direcImage, "/pteropus.png"), paste0(direcImage, "/diceros.png"),
                                  paste0(direcImage, "/neotoma.png"), paste0(direcImage, "/fukomys.png"),
                                  paste0(direcImage, "/callithrix.png"), paste0(direcImage, "/calypte.png"),
                                  paste0(direcImage, "/melopsittacus.png"), paste0(direcImage, "/ophiophagus.png"),
                                  paste0(direcImage, "/lacerta.png"), paste0(direcImage, "/rana.png"),
                                  paste0(direcImage, "/poecilia.png"), paste0(direcImage, "/fundulus.png"),
                                  paste0(direcImage, "/gambusia.png"), paste0(direcImage, "/lepisosteus.png")),
                        size = c(.055, .055, .08, .05, .055, .06, .045, .04, .04,
                                 .06, .06, .055, .1, .045, .07, .07, .07, .08
)
                        )



nodeLab <- data.frame(node = c(72, 67, 75, 70, 74), name = c('Mammals', 'Fish', 'Birds', 'Amphibians', 'Scaled \nReptiles'))



p + geom_cladelab(data = nodeLab, mapping = aes(node = node, label = name, color = name),
                  align = TRUE, geom = 'text',
                  offset = 40, show.legend = FALSE, fontsize = 7) + xlim(0, 110)+
  geom_image(x=79, y=63.5, image=paste0(direcImage, "/camelus.png"), size=.055) +
  geom_image(x=86, y=63.5, image=paste0(direcImage, "/bos.png"), size=.055) +
  geom_image(x=83, y=60.5, image=paste0(direcImage, "/balaenoptera.png"), size=.08) +
  geom_image(x=86.5, y=58, image=paste0(direcImage, "/lynx.png"), size=.05) +
  geom_image(x=79, y=57.5, image=paste0(direcImage, "/pteropus.png"), size=.055) +
  geom_image(x=81, y=53, image=paste0(direcImage, "/diceros.png"), size=.06) +
  geom_image(x=81, y=50, image=paste0(direcImage, "/neotoma.png"), size=.045) +
  geom_image(x=81, y=48, image=paste0(direcImage, "/fukomys.png"), size=.04) +
  geom_image(x=79, y=44.7, image=paste0(direcImage, "/callithrix.png"), size=.04) +
  geom_image(x=81, y=40, image=paste0(direcImage, "/calypte.png"), size=.06) +
  geom_image(x=86, y=37, image=paste0(direcImage, "/melopsittacus.png"), size=.06) +
  geom_image(x=82, y=33, image=paste0(direcImage, "/ophiophagus.png"), size=.04) +
  geom_image(x=81, y=28.5, image=paste0(direcImage, "/lacerta.png"), size=.1) +
  geom_image(x=79, y=24.5, image=paste0(direcImage, "/rana.png"), size=.038) +
  geom_image(x=85, y=24.5, image=paste0(direcImage, "/microcaecilia.png"), size=.06) +
  geom_image(x=81, y=19, image=paste0(direcImage, "/poecilia.png"), size=.07) +
  geom_image(x=83, y=15, image=paste0(direcImage, "/fundulus.png"), size=.07) +
  geom_image(x=83, y=7, image=paste0(direcImage, "/gambusia.png"), size=.07) +
  geom_image(x=81, y=3.5, image=paste0(direcImage, "/lepisosteus.png"), size=.08)









#============================================= Circular ========================
#layout circular
ggtree(speciesTree, layout = 'circular') + geom_tiplab(offset = .1) + geom_cladelab(data = nodeLab, mapping = aes(node = node, label = name, color = name),
                                                                                    align = TRUE,
                                                                                    show.legend = TRUE, offset = 45)

+
  xlim(0, 30) + ggplot2::ylim(0, 90)





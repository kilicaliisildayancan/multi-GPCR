library('jsonlite')
library('ggtree')
library('ggplot2')
library('ggimage')
library('RColorBrewer')


#data
homedir <- "/home/kilicali/multi-domain_gpcr/pipeline/clustered_taxonomy/neuropeptide_w-neuropeptide_b_receptors/"
homedir <- "/home/kilicali/multi-domain_gpcr/datafiles/clusters/chemokine_receptors/8-22TM/"
clusters_dir <- paste0(homedir, "clusters.json")
taxIds_dir <- paste0(homedir, "cluster_taxids.json")
tm_dir <- paste0(homedir, "TM_counts.json")

clusters <- jsonlite::fromJSON(clusters_dir)
taxIds <- jsonlite::fromJSON(taxIds_dir)
TM_counts <- jsonlite::fromJSON(tm_dir)

#get different clusters taxids
cluster_with_taxids <- list()
for (cluster in names(clusters)) {
  cluster_ids <- c()
  tm_counts <- c()
  for (acc_id in clusters[[cluster]]) {
    taxid <- taxIds[[acc_id]]
    cluster_ids <- c(cluster_ids, taxid)

    tm_count <- TM_counts$tm_count[TM_counts$accession == acc_id]
    tm_counts <- c(tm_counts,tm_count)
  }
  cluster_with_taxids[[cluster]] <- list(tax = cluster_ids,tm = tm_counts)
}

#get all species taxids
all_species <- c()
for (cluster in cluster_with_taxids) {
  all_species <- unique(c(all_species, cluster))
}

#get tree
tax_classification <- taxize::classification(all_species, db = 'ncbi')
fullTree <- taxize::class2tree(tax_classification, check=FALSE)
tree <- fullTree$phylo
tree_tax_ids <- fullTree$names
tree_tax_names <- tree$tip.label

#heatmap matrix init
heatmapMat <- as.data.frame(matrix(0, nrow=length(all_species),ncol=length(cluster_with_taxids)))
rownames(heatmapMat) <- all_species

#fill heatmap
for (index_cluster in 1:length(cluster_with_taxids)) {
  for (index_taxid in 1:nrow(heatmapMat)) {
    if (rownames(heatmapMat)[[index_taxid]] %in% cluster_with_taxids[[index_cluster]]$tax) {
        if (sum(cluster_with_taxids[[index_cluster]]$tax %in% rownames(heatmapMat)[index_taxid]) > 1) {
          heatmapMat[index_taxid, index_cluster] <- -1
        } else {
          heatmapMat[index_taxid, index_cluster] <- cluster_with_taxids[[index_cluster]]$tm[cluster_with_taxids[[index_cluster]]$tax %in% rownames(heatmapMat)[index_taxid]]
        }
    }
  }
}


heatmapMat <- as.data.frame(sapply(heatmapMat, as.character))
rownames(heatmapMat) <- all_species



for (i in 1:nrow(heatmapMat)) {
  rownames(heatmapMat)[i] <- tree_tax_names[rownames(heatmapMat)[i] == tree_tax_ids]
}
colnames(heatmapMat) <- names(cluster_with_taxids)



#finish heatmap specs
heatmap.colours <- c("black", "lightgray", "green", "limegreen", "#85C914",
                            "#FF8F1F","#E65D22", "red", "#E81C62",
                            "#FC1FFF", "lightblue1", "skyblue1", "skyblue2", "skyblue3",
                             "blue")

names(heatmap.colours) <- c(-1,0,9:21)

#plot both phylo and heatmap
p <- ggtree(tree) + geom_tiplab()

gheatmap(p, heatmapMat, offset = 10,
         colnames_angle=90, colnames_offset_y = 1,
         hjust=0, font.size=2)+
  scale_fill_manual(values=heatmap.colours)

library('jsonlite')
library('ggtree')
library('ggplot2')
library('ggimage')
library('RColorBrewer')

generateHeatPlot <- function(protein_family) {
  #data
  homedir <- paste0("/home/kilicali/multi-domain_gpcr/pipeline/clustered_taxonomy/", protein_family)
  clusters_dir <- paste0(homedir, "/clusters.json")
  taxIds_dir <- paste0(homedir, "/cluster_taxids.json")
  tm_dir <- paste0(homedir, "/TM_counts.json")

  print(protein_family)
  plot_name <- paste0("/", protein_family, ".png")
  save_dir <- paste0(homedir, plot_name)

  if (file.exists(save_dir)) {
    return()
  }

  clusters <- jsonlite::read_json(clusters_dir)
  taxIds <- jsonlite::read_json(taxIds_dir)
  TM_counts <- jsonlite::fromJSON(tm_dir)

  if (length(clusters) == 0) {
    return()
  }

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
    all_species <- unique(c(all_species, cluster$tax))
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
        } else if (length(cluster_with_taxids[[index_cluster]]$tax) != length(cluster_with_taxids[[index_cluster]]$tm)) {
          heatmapMat[index_taxid, index_cluster] <- -1
        } else {
          count_sel <- cluster_with_taxids[[index_cluster]]$tax %in% rownames(heatmapMat)[index_taxid]
          heatmapMat[index_taxid, index_cluster] <- cluster_with_taxids[[index_cluster]]$tm[count_sel]
        }
      }
    }
  }

  #more heatmap stuff, rownames, colnames, types
  heatmapMat <- as.data.frame(sapply(heatmapMat, as.character))
  rownames(heatmapMat) <- all_species

  for (i in 1:nrow(heatmapMat)) {
    rownames(heatmapMat)[i] <- tree_tax_names[rownames(heatmapMat)[i] == tree_tax_ids]
  }
  colnames(heatmapMat) <- names(cluster_with_taxids)


  #finish heatmap specs
  heatmap.colours <- c("black", "lightgray",
                              "green", "limegreen", "#85C914",
                              "#FF8F1F","#E65D22", "red", "#E81C62", "maroon",
                              "lightblue1", "skyblue1",
                              "skyblue2", "skyblue3", "blue")

  names(heatmap.colours) <- c(-1,0,9:21)

  #plot both phylo and heatmap
  p <- ggtree(tree) + geom_tiplab()

  finalPlot <- gheatmap(p, heatmapMat, offset = 10,
           colnames_angle=90, colnames_offset_y = 1,
           hjust=0, font.size=2)+
    scale_fill_manual(values=heatmap.colours)


  ggsave(save_dir, finalPlot, width=4870, height=5470,units = "px", dpi = 200, limitsize = F)
}

all_pfams <- list.dirs(path = "/home/kilicali/multi-domain_gpcr/pipeline/clustered_taxonomy", full.names = F, recursive = F)

for (pfam in all_pfams) {
  generateHeatPlot(pfam)
}

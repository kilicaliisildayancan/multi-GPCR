library(ggplot2)

data_path <- "/home/kilicali/multi-domain_gpcr/focus_cCKRs/CCR2-CCR5/inter-genic_distance.tsv"
ig_dist <- read.table(data_path, sep = "\t", header = TRUE)


boxplot(ig_dist$IntergenicDistance, horizontal = TRUE, xlab = "Inter-genic distance between CCR2 - CCR5 in 30 vertebrates")

png("/home/kilicali/multi-domain_gpcr/intergenic_dist_boxplot.png", width = 900, height = 200)

dev.off()

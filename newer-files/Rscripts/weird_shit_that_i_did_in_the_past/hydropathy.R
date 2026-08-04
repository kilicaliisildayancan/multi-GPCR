source("./utilities.R")
source("./gradientDescent.R")

pdbid <- "7CKY"
PDBchain <- "R"

pdb <- bio3d::read.pdb(pdbid)

secondaryStructure <- "helix"
PDBdb <- PDBdbInitialize(pdb)
PDBdb <- helixAttributor(PDBdb, pdb)

helixDB <- helixDBinit(PDBdb)
helixDB <- helixDB[helixDB$chain == PDBchain,]
helixVector <- data.frame(x = helixDB$x, y = helixDB$y, z = helixDB$z)


seq7TM <- bio3d::pdbseq(bio3d::trim.pdb(pdb, bio3d::atom.select(pdb, chain = 'R')))
seq7TM <- paste0(seq7TM, collapse = '')
idpr::scaledHydropathyLocal(seq7TM, plotResults = TRUE)

source("./utilities.R")
source("./gradientDescent.R")

pdbid <- "7CKY"
PDBchain <- "R"

pdb <- bio3d::read.pdb(pdbid)
secondaryStructure <- "helix"
PDBdb <- PDBdbInitialize(pdb)
PDBdb <- helixAttributor(PDBdb, pdbfile = pdb)
Oxydb <- OXYdbInitialize(pdb)
Oxydb <- helixAttributor(Oxydb, pdb)

sel <- (Oxydb$chain == PDBchain) & (162 > Oxydb$resno) & (Oxydb$resno > 90) & (Oxydb$ssType == secondaryStructure)
oxyThree <- matrix(c(x = Oxydb$x[sel], y = Oxydb$y[sel], z = Oxydb$z[sel]), nrow = length(Oxydb$y[sel]))


sel <- (PDBdb$chain == PDBchain) & (162 > PDBdb$resno) & (PDBdb$resno > 90) & (PDBdb$ssType == secondaryStructure)
hThree <- matrix(c(x = PDBdb$x[sel], y = PDBdb$y[sel], z = PDBdb$z[sel]), nrow = length(PDBdb$y[sel]))

sizeCA <- numeric(nrow(hThree)) + 0.03
sizeO <- numeric(nrow(oxyThree)) + 0.03

vecCA <-character(nrow(hThree))
vecCA[] <- 'red'

vecO <- character(nrow(oxyThree))
vecO[] <- 'blue'

hThreeDF <- data.frame(x = hThree[,1],y = hThree[,2], z = hThree[,3], sizeH = sizeB)
oxyDF <- data.frame(x = oxyThree[,1],y = oxyThree[,2], z = oxyThree[,3], sizeH = sizeB)

CAandO <- data.frame(x = c(hThree[,1],oxyThree[,1]), y = c(hThree[,2],oxyThree[,2]), z = c(hThree[,3],oxyThree[,3]), size = c(sizeCA, sizeO), color = c(vecCA, vecO))


plotA <- plotly::plot_ly(CAandO, x=~x, y=~y, z=~z, type = 'scatter3d', mode = 'markers', size = ~size, color = ~color)

plotA

plotA <- NULL
#===============================================================================


OXYdbInitialize <- function(pdbfile) {
  sel <- pdbfile$atom$elety == "O"
  pdbDataFrame <- data.frame(resno = pdbfile$atom$resno[sel],
                             resid = pdbfile$atom$resid[sel],
                             chain = pdbfile$atom$chain[sel],
                             ssType = character(length(pdbfile$atom$resno[sel])),
                             x = pdbfile$atom$x[sel],
                             y = pdbfile$atom$y[sel],
                             z = pdbfile$atom$z[sel])
  #does not add the annotations of secondary structures here,
  #just an empty vector of characters

  return(pdbDataFrame)
}

# GOAL: domainDB of the GPCR in interrogation
# input: GPCR dF, helix dF
# 1 get the good coordinates by helixGD
# 2 sort all the distances of helices, best 7 are the TM helices
# 3 go back to helix dF to get the residue numbers
# 4 construct all the domains with their residue numbers
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

#1
goodCoor <- helixGD(helixVector, learn_rate = 1, max_iter = 15, tolerance = 0.1)

#2
dstMat <- c()
for (i in 1:nrow(helixVector)) {
  dstMat <- rbind(dstMat, vNorm(goodCoor-helixVector[i,]))
}
sel <- order(dstMat)[1:7]

best7 <- helixDB[sel,]
best7 <- best7[order(rownames(best7)),]

resNum <- as.data.frame(sapply(best7$resno_couple, 'strsplit', '-')) #still character
resNum <- as.numeric(cbind(resNum[1,], resNum[2,]))
resNum <- resNum[order(resNum)]


domainsGPCR <- domainSetter(resNum, PDBdb, chain = PDBchain)


allICL <- c('C-term', 'ICL1', 'ICL2', 'ICL3')
pdbICL <- domainTrimmer(pdb, domainsGPCR, allICL)

allECL <- c('N-term', 'ECL1', 'ECL2', 'ECL3')
pdbECL <- domainTrimmer(pdb, domainsGPCR, allECL)

allTM <- c('TM1', 'TM2', 'TM3', 'TM4', 'TM5', 'TM6', 'TM7')
pdbTM <- domainTrimmer(pdb, domainsGPCR, allTM)

bio3d::write.pdb(pdbICL, sprintf('%s_ICL.pdb', pdbid))
bio3d::write.pdb(pdbECL, sprintf('%s_ECL.pdb', pdbid))
bio3d::write.pdb(pdbTM, sprintf('%s_TM.pdb', pdbid))

#========================= FUNCTION TEST ZONE ==================================




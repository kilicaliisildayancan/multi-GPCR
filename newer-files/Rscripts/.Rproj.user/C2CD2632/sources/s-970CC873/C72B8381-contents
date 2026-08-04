source("./utilities.R")



pdbid <- "6N51"
pdbfile <- bio3d::read.pdb(pdbid, rm.insert = FALSE, rm.alt = FALSE)
chain <- "B"
secondaryStructure <- "helix"
PDBdb <- PDBdbInitialize(pdbfile)

PDBdb <- helixAttributor(PDBdb, pdbfile)

startEndCoercion <- ssStartEndSelector( PDBdb, chain, secondaryStructure)

atoSeq <- atomicSequenceExtractor(pdbfile, PDBdb, chain, startEndCoercion[1], startEndCoercion[2])

finalTrimmed <- seqresExtractor(pdbfile, chain, atoSeq)


allHelices <- indSSExtractor(PDBdb, secondaryStructure, chain)

#make the df to be converted to JSON
storeData <- data.frame(pdbid = pdbid,
                        GPCRseq = finalTrimmed)
storeData$Helix <- list(allHelices)

bio3d::pdbseq(pdbfile)



seqLength <- length(pdbfile$seqres)
selCA <- pdbfile$atom$elety == "CA"

selSS <- PDBdb$ssType == "helix"
selChain <- PDBdb$chain == chain
resnoV <- PDBdb$resno[selSS & selChain]


resnoHelix <- split(resnoV, cumsum(c(1, diff(resnoV) != 1)))


helix1 <- resnoHelix[["1"]]
xHelix1 <- PDBdb$x[PDBdb$resno[helix1]]
yHelix1 <- PDBdb$y[PDBdb$resno[helix1]]
zHelix1 <- PDBdb$z[PDBdb$resno[helix1]]

vecStart <- c(xHelix1[1], yHelix1[1], zHelix1[1])
vecEnd <- c(xHelix1[length(xHelix1)], yHelix1[length(xHelix1)], zHelix1[length(xHelix1)])
vectorHelix1 <- vecEnd-vecStart
vectorHelix1 <- vectorHelix1/norm(vectorHelix1, type = "2")

rad2deg <- function(rad) {
  return((180 * rad) / pi)
}

a <- helixDBinit(PDBdb)
#-------------------------------------------------------------------------------
resnoV <- PDBdb$resno
allHelix <- split(resnoV, cumsum(c(1, diff(resnoV) != 1)))



#access helix_no from the grouping
targetH <- allHelix[["1"]]

#get coordinates for the helix
xHelix <- PDBdb$x[PDBdb$resno[targetH]]
yHelix <- PDBdb$y[PDBdb$resno[targetH]]
zHelix <- PDBdb$z[PDBdb$resno[targetH]]


#calculate axis
vecStart <- c(xHelix[1], yHelix[1], zHelix[1])
vecEnd <- c(xHelix[length(xHelix)], yHelix[length(yHelix)], zHelix[length(zHelix)])
vectorHelix <- vecEnd-vecStart

hLength <- norm(vectorHelix, type = "2")                    #calculate length

vectorHelix <- vectorHelix/hLength   #convert to unit vector <- axis

#get their average value
xAvg <- mean(xHelix)
yAvg <- mean(yHelix)
zAvg <- mean(zHelix)

#calculate angle
alpha <- ((180*acos(vectorHelix[1])/pi))      #convert rad to degrees
beta <- ((180*acos(vectorHelix[2])/pi))       #convert rad to degrees
gamma <- ((180*acos(vectorHelix[3])/pi))      #convert rad to degrees

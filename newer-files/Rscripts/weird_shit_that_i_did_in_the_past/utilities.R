# Utilities for MDG Project


#================== Functions - TOC ===========================
# 1 - dbInitialize
# 2 - helixAttributor
# 3 - sheetAttributor
# 4 - ssStartEndSelector
# 5 - atomicSequenceExtractor
# 6 - seqresExtractor
# 7 - indSSExtractor
# 8 -
# 9 -
# 10 -
# 11 -
# 12 - getGPCRresno
#==============================================================
#NOTE --> bio3d::read.pdb(pdbid) gets online pdb file

#1 - PDBdbInitialize:  Create dataFrame from PDB file
PDBdbInitialize <- function(pdbfile) {
  sel <- pdbfile$atom$elety == "CA"
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


#-------------------------------------------------------------------------------

#2 - helixAttributor:  Add helix annotations to dataFrame
helixAttributor <- function(dataF, pdbfile) {
  #parameter tests
  testthat::expect_true(is.data.frame(dataF))

  #combine into a df all helix start-end indices with their respective chains
  helixStart <- pdbfile$helix$start
  helixEnd <- pdbfile$helix$end
  helixFull <- data.frame(helixStart, helixEnd, chain = pdbfile$helix$chain)


  for (i in 1:nrow(helixFull)) { #iterate over each start-end-chain couple
    ssStart <- helixFull[i,][["helixStart"]]
    ssEnd <- helixFull[i,][["helixEnd"]]
    ssChain <- helixFull[i,][["chain"]]


    selChain <- dataF$chain == ssChain

    #get the accessible rowname from resno
    intervalStart <- rownames(dataF)[dataF$resno == ssStart & selChain]
    intervalEnd <- rownames(dataF)[dataF$resno == ssEnd & selChain]
    dataF$ssType[intervalStart:intervalEnd] <- "helix"
  }
  return(dataF)
}
#-------------------------------------------------------------------------------

#3 - sheetAttributor:  Add sheet annotations to dataFrame
sheetAttributor <- function(dataF, pdbfile) {
  #parameter tests
  testthat::expect_true(is.data.frame(dataF))

  #combine into a df all sheet start-end indices with their respective chains
  sheetStart <- pdbfile$sheet$start
  sheetEnd <- pdbfile$sheet$end
  sheetFull <- data.frame(sheetStart, sheetEnd, chain = pdbfile$sheet$chain)


  for (i in 1:nrow(sheetFull)) { #iterate over each start-end-chain couple
    ssStart <- sheetFull[i,][["sheetStart"]]
    ssEnd <- sheetFull[i,][["sheetEnd"]]
    ssChain <- sheetFull[i,][["chain"]]


    selChain <- dataF$chain == ssChain

    #get the accessible rowname from resno
    intervalStart <- rownames(dataF)[dataF$resno == ssStart & selChain]
    intervalEnd <- rownames(dataF)[dataF$resno == ssEnd & selChain]
    dataF$ssType[intervalStart:intervalEnd] <- "sheet"
  }
  return(dataF)
}
#-------------------------------------------------------------------------------

#4 - ssStartEndSelector
ssStartEndSelector <- function(dataF, chain = TRUE, ss) {

  selChain <- dataF$chain == chain
  selss <- dataF$ssType == ss

  selDF <- dataF$resno[selChain & selss]
  ssStart <- head(selDF, 1)
  ssEnd <- tail(selDF, 1)

  return(c(ssStart, ssEnd))
}
#returns a list of integers, c(start, end)

#-------------------------------------------------------------------------------

#5 - atomicSequenceExtractor
atomicSequenceExtractor <- function(pdbfile, dataF, strChain, resnoStart, resnoEnd) {
  #there is a major problem with the gaps between

  selChain <- dataF$chain == strChain
  intervalStart <- rownames(dataF)[(dataF$resno == resnoStart) & selChain]
  intervalEnd <- rownames(dataF)[(dataF$resno == resnoEnd) & selChain]

  threeLetterAASequence <- dataF$resid[intervalStart:intervalEnd]
  oneLetterAASequence <- bio3d::aa321(threeLetterAASequence)
  atomicSequence <- paste0(oneLetterAASequence, collapse = "")

  return(atomicSequence)
}

#-------------------------------------------------------------------------------

#6 - seqresExtractor
seqresExtractor <- function(pdbfile, strChain, atomicSeq) {
  selChain <- names(pdbfile$seqres) == strChain
  fullSeq <- paste0(bio3d::aa321(pdbfile$seqres[selChain]), collapse = "") #full CHAIN sequence

  targetvfullMSA <- msa::msaClustalOmega(c(fullSeq, atomicSeq), type = "protein")

  charMSA <- as.character(targetvfullMSA)
  fullSeqMSA <- unlist(strsplit(charMSA[1], split = ""))
  atomicSeqMSA <- unlist(strsplit(charMSA[2], split = ""))

  testthat::expect_equal(length(fullSeqMSA), length(atomicSeqMSA))

  #mark all the ones that are aligned
  indexing <- numeric()
  for (i in 1:length(atomicSeqMSA)) {
    if (atomicSeqMSA[i] != "-") {
      indexing <- rbind(indexing, i)
    }
  }
  start <- head(indexing, 1)
  end <- tail(indexing, 1)

  finalSequence <- paste0(fullSeqMSA[start:end],collapse = "")
  return(finalSequence)
}

#-------------------------------------------------------------------------------

#7 - indSSExtractor
indSSExtractor <- function(dF, df_ssType, df_chain = TRUE) {
  #select chain and ssType from dataframe
  selSS <- dF$ssType == df_ssType
  selChain <- dF$chain == df_chain

  #get resno and resid vectors from selection
  resnoV <- dF$resno[selSS & selChain]
  residV <- dF$resid[selSS & selChain]

  #do the really cool thing-a-magick: split into lists all sequential resno's that are non-consecutive
  allHelix <- split(residV, cumsum(c(1, diff(resnoV) != 1)))

  toBeReturned <- character()
  for (i in 1:length(allHelix)){
    toBeReturned <- rbind(toBeReturned, paste0(bio3d::aa321(allHelix[[i]]), collapse = ""))
  }
  return(toBeReturned)
}

#-------------------------------------------------------------------------------

#8 - readPDB
readPDB <- function(pdbid) {
  pdbfile <- NULL
  pdbfile <- try(bio3d::read.pdb(pdbid))
  return(pdbfile)
}

#-------------------------------------------------------------------------------

#9 - convList2Char_DF
convList2Char_DF <- function(dF) {
  for (column in colnames(dF)) {
    if (is.list(dF[[column]])) {
      for (index in 1:length(dF[[column]])) {
        dF[[column]][[index]] <- paste0(dF[[column]][[index]], collapse = ", ")
      }
      dF[[column]] <- as.character(dF[[column]])
    }
  }
  return(dF)
}

#-------------------------------------------------------------------------------

#10 - angleCoordLengthAttributor
angleCoordLengthAttributor <- function(dF, helix_no) {
  #group helices in dataframe
  #select chain and ssType from dataframe
  selSS <- dF$ssType == "helix"


  #get resno and resid vectors from selection
  resnoV <- dF$resno[selSS]
  chainV <- dF$chain[selSS]

  allHelix <- split(resnoV, cumsum(c(1, diff(resnoV) != 1)))
  chainNames <- split(chainV, cumsum(c(1, diff(resnoV) != 1)))
  names(allHelix) <- c(sapply(chainNames, "[", 1))

  #access helix_no from the grouping
  targetH <- allHelix[[helix_no]]

  #get coordinates for the helix
  xHelix <- dF$x[dF$resno[targetH]]
  yHelix <- dF$y[dF$resno[targetH]]
  zHelix <- dF$z[dF$resno[targetH]]


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
  alpha <- acos(vectorHelix[1]) #radians
  beta <-  acos(vectorHelix[2]) #radians
  gamma <- acos(vectorHelix[3]) #radians

  # if (alpha >= pi/2) {alpha <- (alpha-pi)}
  # if (beta >= pi/2) {beta <- (beta-pi)}
  # if (gamma >= pi/2) {gamma <- (gamma-pi)}
  #return everything in proper order
  return (data.frame(x = xAvg, y = yAvg,z = zAvg, alpha = alpha, beta= beta,gamma = gamma, axis_length = hLength))
}

#-------------------------------------------------------------------------------

#11 - helixDBinit
helixDBinit <- function(dF) {
  #group helices in dataframe
  #select chain and ssType from dataframe
  selSS <- dF$ssType == "helix"


  #get resno and resid vectors from selection
  resnoV <- dF$resno[selSS]
  chainV <- dF$chain[selSS]

  allHelix <- split(resnoV, cumsum(c(1, diff(resnoV) != 1)))
  chainNames <- split(chainV, cumsum(c(1, diff(resnoV) != 1)))
  names(allHelix) <- c(sapply(chainNames, "[", 1))



  helixFrame <- data.frame(matrix(ncol = 9, nrow = 0))
  colnames(helixFrame) <- c("resno_couple",
                            "chain",
                            "alpha",
                            "beta",
                            "gamma",
                            "x",
                            "y",
                            "z",
                            "axis_length")

  for (i in 1:length(allHelix)) {
    resno_couple1 <- list(head(allHelix[[i]], 1), tail(allHelix[[i]], 1))

    targetValues <- angleCoordLengthAttributor(dF, i)

    targetValues <- cbind(chain = names(allHelix[i]), targetValues)
    targetValues <- cbind(resno_couple = paste0(resno_couple1, collapse = '-'), targetValues)
    helixFrame <- rbind(helixFrame, targetValues)
  }
  return(helixFrame)
}

#-------------------------------------------------------------------------------

#12 - domainSetter
domainSetter <- function(resno_coupleV, PDBdb, chain) {
  Nterm <- "N-term"
  Cterm <- "C-term"
  intraDomains <- c("TM1","ICL1","TM2","ECL1",
                    "TM3","ICL2","TM4","ECL2","TM5",
                    "ICL3","TM6","ECL3","TM7")
  selChain <- PDBdb$chain == chain
  PDBdb <- PDBdb[selChain,]

  domain <- character(nrow(PDBdb))

  for (i in 1:length(domain)) {
    if (all(PDBdb$resno[i] < resNum)) {
      domain[i] <- Nterm
    } else if (all(PDBdb$resno[i] > resNum)){
      domain[i] <- Cterm
    } else if (any(PDBdb$resno[i] == resNum)) {
      whichMatch <- which(PDBdb$resno[i] == resNum) - 1
      domain[i] <- intraDomains[2*(whichMatch%/%2)+1]
    } else {
      bitVector <- as.numeric(PDBdb$resno[i] > resNum)
      sumBV <- sum(bitVector)
      domain[i] <- intraDomains[sumBV]
    }
  }
  return(cbind(PDBdb, domain))
}


#-------------------------------------------------------------------------------
domainTrimmer <- function(pdb, PDBdb, domains) {
  # A wrapper function that utilizes bio3::trim.pdb for trimming, bio3d::atom.select for selecting
  # the domains


  # PDBdb variable must have been processed through to have the annotated domains.
  # Please refer to the function domainSetter() for clarification

  sel <- PDBdb$resno[PDBdb$domain %in% domains]
  selChain <- PDBdb$chain[PDBdb$domain %in% domains]
  pdbSelexn <- bio3d::atom.select(pdb, resno = sel, chain = selChain)

  return(bio3d::trim.pdb(pdb = pdb, inds = pdbSelexn))

}



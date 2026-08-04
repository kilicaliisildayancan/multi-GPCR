source("./utilities.R")
secondaryStructure <- "helix"

#Help protect when sourcing file
startFromScratch = TRUE
if (startFromScratch) {
  JSONdb <- data.frame(pdbid = character(),
                       GPCRseq = character(),
                       Helix = character())
}

directory <- "/home/kilicali/multi-domain_gpcr/datafiles/data_from_R/"
opmrawdata <- read.csv("/home/kilicali/multi-domain_gpcr/opmrawdata_final.csv")

#main "pipeline" function

trimPDBid <- function(pdbid, chain) {
  out <- tryCatch(
    expr = {
      pdbfile <- readPDB(pdbid)
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
      return(storeData)
    },
    error = function(e) {
      print(e)
      return(NULL)
    },
    finally = {
      print(sprintf("Done with %s!", pdbid))
    }
  )
  return(out)
}



for (i in (nrow(JSONdb)+1):length(opmrawdata$pdbid)) {
  temp_pdbid <- opmrawdata$pdbid[[i]]
  temp_chain <- opmrawdata$chain_id[[i]]
  temp_db <- trimPDBid(temp_pdbid, temp_chain)
  if (is.list(temp_db)) {
    JSONdb <- rbind(JSONdb, temp_db)
  }
  if (is.null(temp_db)) {
    next
  }
  else {
    print(sprintf("Check problem with %s", temp_db))
  }
}

#finish up and conver to JSON, then write it out to file in directory - not using for now
toWrite <- jsonlite::toJSON(convList2Char_DF(JSONdb))
jsonlite::write_json(toWrite, sprintf("%s7TMtrimmed_byR.json", directory))

toWrite <- convList2Char_DF(JSONdb)

write.csv(toWrite, sprintf("%s7TMtrimmed_byR.csv", directory), row.names = FALSE)

usedMaterialsTable <- function(dfEq,dfReag,dfBE,dfCont) {
  colEq <- dfEq
  colReag <- dfReag
  colBE <- dfBE
  colCont <- dfCont
  maxLen <- max(length(colEq), length(colReag), length(colBE), length(colCont))
  length(colEq) <- maxLen
  length(colReag) <- maxLen
  length(colBE) <- maxLen
  length(colCont) <- maxLen
  matTable <- cbind(colEq, colReag, colBE, colCont)
  colnames(matTable) <- c("Equipment", "Reagents", "Bio. Ent.", "Containers")
  return(matTable)
}

costEquipment <- function(pathEq, eqNames) {
  eqCSV <- read.csv(pathEq)
  cost <- 0
  for (name in eqNames) {
    sel <- eqCSV$Name == name
    cost <- cost + as.numeric(eqCSV$Price[sel])
  }
  return(format(cost, scientific=FALSE))
}

costReagents <- function(pathReag, reagents) {
  reagCSV <- read.csv(pathReag)
  cost <- 0
  for (reagent in 1:length(reagents[,1])) {
    if (grepl("g", reagents[reagent, 2])) {
      reagentMass <- massConvGrams(reagCSV$Amount[reagCSV$Name == reagents[reagent, 1]])
      reagentPrice <- reagCSV$Price[reagCSV$Name == reagents[reagent, 1]]

      ratioUsed <- massConvGrams(reagents[reagent, 2])/reagentMass
      cost <- cost + ratioUsed*reagentPrice

    }
    else {
      # later do the same for molarity, and then volume and concentration used
      print("This is not implemented yet!")
    }
  return(format(cost, scientific=FALSE))


  }
}

costDisposables <- function(dispCSVpath, disps) {
  dispCSV <- read.csv(dispCSVpath)
  cost <- 0
  for (disp in 1:length(disps[,1])) {
    name <- disps[disp,1]
    vol <- disps[disp,2]
    quant <- as.numeric(disps[disp,3])

    sel <- dispCSV$Name == name & dispCSV$Volume == vol
    listPrice <- dispCSV$Price[sel]
    listQuant <- as.numeric(dispCSV$Quantity[sel])

    ratioUsed <- quant/listQuant
    return(format(ratioUsed*listPrice, scientific = FALSE))

  }
}
# costBE <- function() {}

costContainers <- function() {}



massConvGrams <- function(mass) {
  if (grepl("kg",mass)) {
    mass <-as.numeric(strsplit(mass, "kg")[[1]])
    return(mass*1000)
  }
  else if (grepl("mg",mass)) {
    mass <-as.numeric(strsplit(mass, "mg")[[1]])
    return(mass*0.001)
  }
  else if (grepl("ug",mass)) {
    mass <-as.numeric(strsplit(mass, "ug")[[1]])
    return(mass*0.000001)
  }
  else if (grepl("g", mass)) {
    return(as.numeric(strsplit(mass, "g")[[1]]))
  }
}




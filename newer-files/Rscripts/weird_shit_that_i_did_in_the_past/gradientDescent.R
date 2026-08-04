#GRADIENT DESCENT IMPLEMENTATION FOR GPCR COORDINATES
#function for distances: abs(coor1 - x)
#derivative of function: (x - coor1)/abs(coor1 - x), condition that coor1 != x
#helper function: Vector Norm
vNorm <- function(vector) {
  return(sqrt(sum(vector**2)))
}

#this function returns the gradient vector
helixGradient <- function(x, helixVector) {
  #x is a 3D vector, and helixVector is a matrix of (Nx3 dimensions)
  gradientVec <- numeric(3)
  gradientMat <- matrix(nrow = dim(helixVector)[1], ncol = length(x))
  for (i in 1:dim(helixVector)[1]) {
    denominator <- vNorm(x-helixVector[i,])
    if (denominator == 0) {
      sel <- denominator == 0
      denominator[sel] <- 10**-7  #replicate 0
    }
    for (j in 1:length(x)) {
      numerator <- x[j]-helixVector[i, j]
      gradientMat[i, j] <- numerator/denominator
    }
  }
  for (col in 1:ncol(gradientMat)) {
    gradientVec[col] <- sum(gradientMat[,col])
  }
  return(gradientVec)
}

helixGD <- function(helixVector, learn_rate, max_iter, tolerance) {
  coord <- c(mean(helixVector[,1]),
                 mean(helixVector[,2]),
                 mean(helixVector[,3]))
  iteration <- 0
  converged <- FALSE
  while (!converged) {
    diff <- helixGradient(coord, helixVector)
    coord <- coord -(diff*learn_rate)
    print(diff)
    if (sqrt(sum(diff**2)) <= tolerance) {
      converged <- TRUE
    }
    else if (iteration >= max_iter) {
      converged <- TRUE
    }
    iteration <- iteration +1
  }
  return(coord)
}


### Helix Axis from C-O direction

problemHelix <- bio3d::trim.pdb(pdb, bio3d::atom.select(pdb, resno = c(92:161), chain = 'R'))
pCA <- helixAttributor(PDBdbInitialize(problemHelix), problemHelix)
pO <- helixAttributor(OXYdbInitialize(problemHelix), problemHelix)
a <- data.frame()
for (i in 1:nrow(pO)-3) {
  AngleVec1 <- c(pO$x[i] - pCA$x[i], pO$y[i] - pCA$y[i], pO$z[i] - pCA$z[i])
  AngleVec2 <- c(pO$x[i + 1] - pCA$x[i + 1], pO$y[i + 1] - pCA$y[i + 1], pO$z[i + 1] - pCA$z[i + 1])
  AngleVec3 <- c(pO$x[i + 2] - pCA$x[i + 2], pO$y[i + 2] - pCA$y[i + 2], pO$z[i + 2] - pCA$z[i + 2])
  AngleVec4 <-c(pO$x[i+3] - pCA$x[i+3], pO$y[i+3] - pCA$y[i+3], pO$z[i+3] - pCA$z[i+3])

  FinalAngle <- (AngleVec1+AngleVec2+AngleVec3+AngleVec4)/4
  FinalAngle <- FinalAngle/vNorm(FinalAngle)
  a <- rbind(a, FinalAngle)
}

aaaNorm <- data.frame()
for (i in 1:(nrow(a)-1)) {
  diff <- a[i+1,] - a[i,]
  aaaNorm <- rbind(aaaNorm, vNorm(diff))
}

kaka <- data.frame()
for (i in 1:nrow(pO)) {
  FinalAngle <- c(pO$x[i] - pCA$x[i], pO$y[i] - pCA$y[i], pO$z[i] - pCA$z[i])
  FinalAngle <- FinalAngle/vNorm(FinalAngle)
  kaka <- rbind(kaka, FinalAngle)
}
kakaDiff <- data.frame()
for (i in 1:(nrow(kaka)-1)) {
  diff <- kaka[i+1,] - kaka[i,]
  kakaDiff <- rbind(kakaDiff, vNorm(diff))
}

c1 <- character(length(1:67))
c1[1:34] <- 'red'
c1[35:44] <- 'blue'
c1[45:67] <- 'yellow'
aDF <- data.frame(x = a[,1], y = a[,2], z = a[,3], col1 = c1)

plotly::plot_ly(aDF, x = ~x, y = ~y, z = ~z, type = 'scatter3d', mode = 'markers', color = ~c1)






c1 <- character(length(1:70))
c1[1:35] <- 'red'
c1[36:44] <- 'blue'
c1[45:70] <- 'yellow'
kakaDF <- data.frame(x = kaka[,1], y = kaka[,2], z = kaka[,3], col1 = c1)

plotly::plot_ly(kakaDF, x = ~x, y = ~y, z = ~z, type = 'scatter3d', mode = 'markers', color = ~c1, size = numeric(nrow(kakaDF))+0.03)

kakaAng <- data.frame()
for (i in 1:(nrow(kakaDF)-1)) {
  angle <- (acos(geometry::dot(t(kakaDF[i+1,]), t(kakaDF[i,])))*180)/pi
  kakaAng <- rbind(kakaAng, data.frame(alpha = angle))
}

plotly::plot_ly(kakaAng, x = ~alpha, y = ~beta, z = ~gamma, type = 'scatter3d', mode = 'markers', color = c1)



View(data.frame(a = kakaAng[order(kakaAng[,1]),]))

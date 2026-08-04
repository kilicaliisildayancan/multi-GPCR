source("./utilities.R")
source("./gradientDescent.R")
#group angles of helices, get the best 7

pdbid <- "4XT3"
pdb <- bio3d::read.pdb(pdbid)

chain <- "A"
secondaryStructure <- "helix"
PDBdb <- PDBdbInitialize(pdb)
PDBdb <- helixAttributor(PDBdb, pdb)

helixDB <- helixDBinit(PDBdb)

helixVector <- data.frame(x = helixDB$x, y = helixDB$y, z = helixDB$z)
goodCoor <- gradientDescent(helixVector, learn_rate = 0.1, max_iter = 15, tolerance = 0.1)


fig <- plotly::plot_ly(y = a$alpha, type = 'box')
fig <- plotly::add_trace(fig, y = a$beta)
fig <- plotly::add_trace(fig, y = a$gamma)

fig2 <- plotly::plot_ly(a, x=~x, y=~y, z=~z, type = 'scatter3d', color =rownames(a), mode = 'markers')
fig2 <- plotly::add_trace(fig2, x=goodCoor[1], y=goodCoor[2], z=goodCoor[3])
fig
fig2


#after we can extract best 7, we can start joining all the helices between
#the best 7's sandwiwitching planes
d <- data.frame()
for (i in 1:length(rownames(helixVector))) {
  d <- rbind(d, abs(goodCoor-helixVector[i,]))
}

data.frame(resno_couple = resno_couple1,
           chain = names(allHelix[i]),
           x = x, y = y, z = z, alpha = alpha, beta = beta,
           gamma = gamma, axis_length = axis_length)

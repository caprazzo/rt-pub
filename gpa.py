import gp

# simple doubling function
double = gp.node(gp.addw,[gp.paramnode(0),gp.paramnode(0)])

# echo
echo = gp.node(gp.addw,[gp.paramnode(0), gp.constnode(0)])

# evolve all output from 8 to 20
def score_820(tree, dataset):
	dif = 0
	values = {}
	for d in dataset:
		v = tree.evaluate([d, d])
		if v < 480 or v > 1200:
			dif += 2
		sv = str(v)
		if sv in values:
			dif += values[sv]
			values[sv] =+ 1
		else:
			values[sv] = 1
		
	return dif
	
def getrankfunction(scorefunction, dataset):
  def rankfunction(population):
    scores=[(scorefunction(t,dataset),t) for t in population]
    scores.sort()
    return scores
  return rankfunction
  
#for i in range(1,701):
#	print echo.evaluate([i])
#	print double.evaluate([i])

#print score_820(gp.makerandomtree(1), range(1,701))



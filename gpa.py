import gp

# simple doubling function
double = gp.node(gp.addw,[gp.paramnode(0),gp.paramnode(0)])

# echo
echo = gp.node(gp.addw,[gp.paramnode(0), gp.constnode(0)])

# evolve all output from 8 to 20
def score_820(tree, dataset):
	dif = 0
	for d in dataset:
		print d
		v = tree.evaluate(d)
		if v < 480 or v > 1200:
			dif += 1
		print dif
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
	
gp.evolve(1, 50, getrankfunction(score_820, range(1,701)))
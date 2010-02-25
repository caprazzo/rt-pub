#from numpy import array
from scipy.cluster.vq import whiten, vq, kmeans
from random import choice
import random
from random import randint
from datetime import datetime
import time

def key(url):
	return url.split('/').pop().replace('>','')
	
def keys(line):
	u, i = line.strip().split('\t')
	return (key(u), key(i))

def distance(itemA, itemB):
	return numpy.linalg.norm(numpy.array(itemA)-numpy.array(itemB))

def fop():
	count = -1+len(items)**2
	filled_items = {}
	f=open('distances.txt','w')
	for i in items:
		for j in items:
			if i == j: continue
			if i not in filled_items:
				filled_items[i] = user_matrix(items[i])
			if j not in filled_items:
				filled_items[j] = user_matrix(items[j])

			d = distance(filled_items[i], filled_items[j])
			print "%s %s %d %f" % (i, j, count, d)
			f.write('%s %s %f\n' % (i, j, d))
			count -= 1

def kcluster(users, items, k=5):
	l=100
	l=len(users)
	print 'start kclusters'
	clusters = [ [random.random()*2.0+1.0 for i in range(l)] for j in range(k)]

	lastmatches = None
	start = datetime.now()
	for t in range(100):
		now = datetime.now()
		print '%s Iteration %d' % (now-start, t)
		start=now
		bestmatches=[[] for i in range(k)]
		
		for item in items:
			bestmatch = 0
			item_users = items[item]

			for i in range(1,k):
				d = distance(clusters[i], item_users)
				if d > distance(clusters[bestmatch], item_users):
					bestmatch = i
			bestmatches[bestmatch].append(item)
		
		if bestmatches == lastmatches: break
		lastmatches = bestmatches
		
		for i in range(k):
			avgs=[0.0]*l
			if len(bestmatches[i]) > 0:
				for itx in bestmatches[i]:
					item_users = items[itx]
					for m in range(l):
						avgs[m] += item_users[m]
						
				for j in range(len(avgs)):
					avgs[j] /= len(bestmatches[i])

				clusters[i] = avgs

		for _x in range(len(bestmatches)):
			print _x, len(bestmatches[_x])
	
	c = 0
	f = open('clusters_%s.txt' % time.time(), 'w')	
	for x in bestmatches:
		for e in x:
			print c, e
			f.write('%d %s\n' % (c, e))
		c += 1
	f.close()
	
def user_matrix(l, item_users, sorted_users):
	a = [0.0]*l
	for i in range(l):
		if sorted_users[i] in item_users:
			a[i] = 1.0
	return a

def custom():
	_items = {}
	users = []

	for line in open('my_items_likehood.txt'):
		user, item = keys(line)
		users.append(user)
		if item in _items:
			_items[item].append(user)
		else:
			_items[item] = [user]


	sorted_users = sorted(users)
	l = len(sorted_users)
	items={}
	count=0
	features=[]
	for item in _items:
	
		features.append(user_matrix(l, _items[item], sorted_users))
		if count == 100: break
		count += 1

	print 'whiten'
	whitened = whiten(array(features))
	print 'kmeans'
	print kmeans(whitened)
	print "%d items voted by %d users" % (len(items), len(users))

custom()


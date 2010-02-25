import sys
import random
users = []
items = []

def index(seq, item):
	for index in (i for i in xrange(len(seq)) if item == seq[i]):
		return index
	return -1
	
def num(seq, name):
	num_id = index(seq, name)
	if num_id == -1:
		num_id = len(seq)
		seq.append(name)
	return num_id+1

def dump(seq, fname):
	f = open(fname,'w')
	for i in range(len(seq)):
		f.write('%d,%s\n' % (i+1, seq[i]))
	f.close
	
csv = open('mahout_seq.csv','w')
last = None
for l in open(sys.argv[1]):
	u,i = l.strip().replace('<','').replace('>','').split('\t')

	user_id = num(users,  u.split('/').pop())
	item_id = num(items, i.split('/').pop())
	if last is not None and last <> user_id:
		csv.write('\n')
	csv.write('%s,%s,%f\n' % (user_id, item_id+9999, 0.1))
	last = user_id
	
csv.close()

dump(users, 'users_map.csv')
dump(items, 'items_map.csv')


import sys, re

src = sys.argv[1]
out_mahout = '%s_mahout.txt' % src
out_users = '%s_users.txt' % src
out_items = '%s_items.txt' % src

users = {}
items = {}
rows = {}
f_out_mahout = open(out_mahout, 'w')
for line in open(src):
	try:
		user, item = [re.sub('^.*/','',t).strip() for t in re.sub('[<>]', '', line).split('\t')]
	
		if user not in users:
			users[user] = len(users)		
		
		if item not in items:
			items[item] = len(items)
	
		f_out_mahout.write('%s,%s\n' % (users[user], items[item]))
	except Exception, e:
		print e
		
f_out_mahout.close()
		
f_out_users = open(out_users, 'w')
for user in users:
	f_out_users.write('%s,%s\n' % (user, users[user]))
f_out_users.close()

f_out_items = open(out_items, 'w')
for item in items:
	f_out_items.write('%s,%s\n' % (item, items[item]))
f_out_items.close()
		
	

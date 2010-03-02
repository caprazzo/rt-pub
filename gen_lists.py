import shlex, subprocess
from operator import itemgetter

q= """PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cu: <http://caprazzi.net/cu/2010/>

SELECT ?item ?user WHERE {
	?user cu:shares ?item .
	OPTIONAL { 
		?item dc:title ?title .
	}
	filter (!BOUND(?title))
}
ORDER BY ?user
LIMIT %d
OFFSET %d"""

def get_query(page_size, page_num):
	return (q % (page_size, (page_num-1)*page_size)).replace('\n',' ')
	

def generate(args):
	p = subprocess.Popen(args, bufsize=1, stdout=subprocess.PIPE)
	head=True
	items=[]
	users={}
	for line in p.stdout:
		if head:
			head=False
			continue
		i, u = line.strip().split('\t')
		item = i.split('/').pop().replace('>','')
		user = u.split('/').pop().replace('>','')
		items.append(item)
		if user in users:
			users[user] += 1
		else:
			users[user] = 1
			
	return (items, users)
	


page_size=500000
page_count=1
for page_num in range(1, page_count+1):
	command_line = '4s-query -f text -s 16000000 curiosity "%s"' % get_query(page_size, page_num)
	args = shlex.split(command_line)
	items, users = generate(args)
	f_items = open('data_matic/items_%04d.txt' % page_num, 'w')
	for item in items:
		f_items.write(item + '\n')
	f_items.close()
	
	f_users = open('data_matic/users_%04d.txt' % page_num, 'w')
	for user, count in sorted(users.items(), key=itemgetter(1)):
		f_users.write('%s %s\n' % (user, count))
	f_users.close()
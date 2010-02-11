visited_items = set([])
visited_users = []
queue = ['04542763409539038815']
triples = set([])

def store(subj, pred, obj):
	f = open('store.txt', 'a')
	f.write(json.dumps((subj, pred, obj)) + '\n')
	f.close()

def shared_items(user):

def drill_user(user):
	for item in shared_items(user):
		store(item.id, 'dc:title', item.title) 
		store(user, 'cu:shares', item.id)
		if item.id not in visited_items:
			visited_items.add(item.id)
			for liker in gr.item_likers(item.id)
				store(liker, 'cu:likes', item.id)
				queue.append(liker)
					
def run():
	while len(queue) > 0:
		user = queue.pop()
		visited_users.append(user)
		drill_user(user)
		
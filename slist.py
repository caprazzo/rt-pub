from blist import blist
class Slist():
	def __init__(self):
		self.lists = {}

	def __len__(self):
		return sum([len(self.lists[c]) for c in self.lists])
		
	def append(self, item):
		c = item[0]
		if not c in self.lists:
			self.lists[c] = []
		self.lists[c].append(item)
		
	def try_remove(self, item):
		c = item[0]
		try:
			self.lists[c].remove(item)
			return True
		except ValueError:
			return False



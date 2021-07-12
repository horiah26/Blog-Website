class Post:
	def __init__(self, id, title, text, owner, date_created, date_modified):
		self.id = id
		self.title = title
		self.text = text
		self.date_created = date_created;
		self.date_modified = date_modified;
		self.owner = owner;
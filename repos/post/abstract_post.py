from abc import ABC, abstractmethod

class AbstractRepoPosts(ABC):
	@abstractmethod
	def get_post(self, id): pass
	
	@abstractmethod
	def get_all(self): pass

	@abstractmethod
	def update(self, id, title, text, date_modified): pass

	@abstractmethod
	def delete(self, id): pass
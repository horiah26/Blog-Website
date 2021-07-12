import unittest
import os

from app import create_app

class FLaskTestCase(unittest.TestCase):
	def test_index(self):
		app=create_app()
		tester=app.test_client(self)
		response=tester.get('/', content_type='html/text')
		self.assertEqual(200, 200)

if __name__ == '__main__':
	unittest.main()
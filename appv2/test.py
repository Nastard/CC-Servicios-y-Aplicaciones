from pymongo import MongoClient
import unittest

class TestStringMethods(unittest.TestCase):
	def test_ar_24(self):
		client = MongoClient('0.0.0.0', 27017)
		db = client.practica2
		coll = db.san_francisco_ar_24.find()
		client.close()

		count = 0
		for c in coll:
			count = count +1
		self.assertEqual(count, 24)

	def test_ar_48(self):
		client = MongoClient('0.0.0.0', 27017)
		db = client.practica2
		coll = db.san_francisco_ar_48.find()
		client.close()

		count = 0
		for c in coll:
			count = count +1
		self.assertEqual(count, 48)

	def test_ar_72(self):
		client = MongoClient('0.0.0.0', 27017)
		db = client.practica2
		coll = db.san_francisco_ar_72.find()
		client.close()

		count = 0
		for c in coll:
			count = count +1
		self.assertEqual(count, 72)

if __name__ == '__main__':
    unittest.main()

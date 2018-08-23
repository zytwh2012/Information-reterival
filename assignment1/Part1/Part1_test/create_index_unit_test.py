import os
import sys
import glob
import nltk
import sqlite3
import unittest


connection = None


'''
# In this unit test file, we have three test functions:

# 1. check if there is a stopword in database.
# 2. check if a noun word is be lemmatized
# 3. check if data form is correct 
'''
class TestStringMethods(unittest.TestCase):

	def test_checkStopWords(self):
		query = "select * from posting where word = 'for' "
		self.assertEqual(executeQuery(query), [])
		query = "select * from posting where word = 'while'"
		self.assertEqual(executeQuery(query), [])
		query = "select * from posting where word = 'and' "
		self.assertEqual(executeQuery(query), [])
		query = "select * from posting where word = 'OR' "
		self.assertEqual(executeQuery(query), [])
	def test_checkLemmatize(self):
		query = "select distinct(doc) from posting where word = 'friends'"
		self.assertEqual(executeQuery(query), [])
		query = "select distinct(doc) from posting where word = 'friend'"
		self.assertEqual(executeQuery(query), [(1971,)])
		query = "select distinct(doc) from posting where word = 'graduating'"
		self.assertTrue(executeQuery(query) != [])

	def test_format(self):
		query = "select * from posting limit 1"
		self.assertTrue(type(executeQuery(query)[0][1]) == str)
		self.assertTrue(type(executeQuery(query)[0][0]) == int)
		self.assertTrue(type(executeQuery(query)[0][2]) == int)
		self.assertTrue((executeQuery(query)[0][0])<= 1972 and (executeQuery(query)[0][0]) >= 1971)


'''
# this function is to exexute query
'''
def executeQuery(query):
	cur = connection.cursor() #get cursor
	return [i for i in cur.execute(query)]



'''
# this function is to connect database
'''
def connectionDataBase(data_file_name):
	global connection
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Exception as e:
		print(e)
		exit("Error,unit_test file can not connect database")

'''
# this function is to check if create_index.py exist
# check if Documents contains correct docuemnts
'''
def checkFiles():
	if len(sys.argv) != 1:
		exit("Error, command line error..")
	else:
		if not os.path.isfile("./../create_index.py") or not os.path.isfile("../print_index.py"):
			exit("Error, create_index.py or print_index.py does not exit..") 
	try:
		for filepath in glob.glob(os.path.join("./Documents", '*.txt')):
			if int(filepath.split("_")[1]) != 1971 and int(filepath.split("_")[1]) != 1972:
				exit("Error, Document not correct")
	except Exception:
		raise
		exit("Error, Documents' files not correct")


	print("The documents and python script are correct...\nchecking...")




if __name__ == '__main__':
	checkFiles()
	os.system("python3 ./../create_index.py Documents ")
	connection = connectionDataBase("./Documents/data.db")
	unittest.main(verbosity=2)
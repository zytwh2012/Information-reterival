import os
import sys
import glob
import nltk
import sqlite3
import unittest
import math



connection = None


class TestStringMethods(unittest.TestCase):

	def test_illegalInput(self):
		os.system("python3 ./../vs_query.py ./Documents/data.db > output1.txt")
		fp = open("./output1.txt")
		for line in fp:
			first_line  = line.split()
			break
		fp.close()
		self.assertEqual(first_line[0],"Error")

	def test_query_one(self):
		os.system("python3 ./../vs_query.py ./Documents/data.db 4 y one > output2.txt")	
		fp = open("./output2.txt")
		line_list = [ line for line in fp ]
		fp.close()
		for l in line_list:
			if len(l.split()) > 1:
				score = float(l.split()[1])
				self.assertEqual(score,0.0)
			else:
				self.assertTrue()

	def test_query_two(self):
		os.system("python3 ./../vs_query.py ./Documents/data.db 4 y ten NINE y one > output3.txt")	
		fp = open("./output3.txt")
		line_list = [ line for line in fp ]
		fp.close()
		for l in line_list:
			if len(l.split()) > 1:
				score = float(l.split()[1])
				self.assertEqual(score,0.0)
			else:
				self.assertTrue(False)

	def test_query_three(self):
		os.system("python3 ./../vs_query.py ./Documents/data.db 4 y two three > output4.txt")	
		fp = open("./output4.txt")
		line_list = [ line for line in fp ]
		fp.close()
		for l in line_list:
			if len(l.split()) > 1:
				score = float(l.split()[1])
				doc_id = int(l.split()[0])
				if doc_id == 1:
					self.assertEqual(score,1.0)
				elif doc_id == 2 or doc_id == 4:
					self.assertTrue(score<0.707108)
					self.assertTrue(score>0.707106)
				else:
					self.assertEqual(score,0.0)
			else:
				self.assertTrue(False)
	

'''
# this function is to execute query
'''
def executeQuery(query):
	cur = connection.cursor() #get cursor
	return [i for i in cur.execute(query)]


'''
# this function is to connect to database
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
		if not os.path.isfile("./../vs_query.py"):
			exit("Error, vs_query.py does not exit..") 
	try:
		for filepath in glob.glob(os.path.join("./Documents", '*.txt')):
			if int(filepath.split(".")[-2].split("_")[1]) > 4 or int(filepath.split(".")[-2].split("_")[1]) < 1:
				exit("Error, Document not correct")
	except Exception:
		raise
		exit("Error, Documents' files not correct")


	print("The documents and python script are correct...\nchecking...")


if __name__ == '__main__':
	checkFiles()
	connection = connectionDataBase("./Documents/data.db")
	unittest.main(verbosity=2)

import os
import sys
import glob
import nltk
import sqlite3
import unittest


connection = None

'''
# In this unit test file, we have three test functions:

# 1. check if all words in database been printed
# 2. check if the word "angle" is printed correctly
# 3. check if the word "year" is printed correctly
'''
class TestStringMethods(unittest.TestCase):

	def test_totalNum(self):
		fp = open("./output.txt")
		count = 0
		for line in fp:
			count +=1
		fp.close()
		query = "select count(distinct word) from posting "		
		self.assertEqual(executeQuery(query)[0][0],count)

	def test_angle_info(self):	
		fp = open("./output.txt")
		angle_list = None
		for line in fp:
			a_list = line.split("	")
			if a_list[0] == "angle":
				angle_list = a_list[1].split(";")[:-1]	
		fp.close()
		self.assertTrue((angle_list)!= None)
		self.assertEqual(len(angle_list), 1)
		self.assertEqual(int(angle_list[0].split(":")[0]),1971)
		self.assertEqual(int(angle_list[0].split(":")[1]),250)

	def test_years_info(self):	
		fp = open("./output.txt")
		year_list = None
		for line in fp:
			a_list = line.split("	")
			if a_list[0] == "year":
				year_list = a_list[1].split(";")[:-1]	
		fp.close()
		self.assertTrue((year_list)!= None)
		self.assertEqual(len(year_list), 2)
		self.assertTrue( "1972:5" in year_list)
		self.assertTrue("1971:1" in year_list)


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
	os.system("python3 ./../print_index.py Documents > output.txt")
	connection = connectionDataBase("./Documents/data.db")
	unittest.main(verbosity=2)

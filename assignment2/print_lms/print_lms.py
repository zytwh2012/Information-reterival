import sys
import glob
import os
import nltk
import sqlite3
import os.path
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer


path = None

def main():

	if not checkArgv():
		print("Error(please try one of ways to run program): ")
		print("\t$ python3 print_lms.py path")
		return -1
		
	if not os.path.isfile(path) :
		print("Error no index file ")
		return -1;
	connection = connectionDataBase(path)

	printIndex(connection)

	connection.close()

	return 0;


'''
connect to database
'''
def connectionDataBase(data_file_name):
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Error as e:
		exit("Error,can not connect to databasess")
'''
main function to print index
using query to get infor and store in a_list
'''


def printIndex(connection):
	try:
		cur = connection.cursor()
		last_doc = None
		for (doc, term, prob) in cur.execute("SELECT doc,term,probability from models order by doc "):
			prob = "{:.4f}".format(prob)
			if doc == last_doc:
				tail = ", " + term+":"+ str(prob)
				print(tail,end ="")
			else:
				if last_doc == None:
					print(str(doc) + "\t" + term+":" + str(prob),end = "")
					last_doc = doc
				else:
					last_doc = doc
					print(" \n" + str(doc) + "\t" + term + ":"+ str(prob),end = "")			

		print("\n")
	except Error as e:
		 exit("Error occurs when get information from databasess")
	return 1
'''
check command line input
'''
def checkArgv():
	global path
	if len(sys.argv) != 2:
		print("Error")
		return False
	else:
		path = sys.argv[1]
		if os.path.isfile(path):
			return True
		else:
			return False

if __name__ == "__main__":
	main()

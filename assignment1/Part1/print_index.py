#!/usr/bin/env python3 

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
		print("\t$ python3 printIndex.py path")
		return -1
		
	if not os.path.isfile(path+"/data.db") :
		print("Error no index file ")
		return -1;
	connection = connectionDataBase(path+"/data.db")

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
		a_list = []
		last_word = ""
		for (word, doc, pos) in cur.execute("SELECT word,doc,position from posting order by word "):
			if word == last_word:
				a_list.append(str(doc)+":"+str(pos)+";")
			else:
				if last_word != "":
					str_head = last_word+"\t"
					for i in a_list:
						str_head += i
					print(str_head)
					str_head = ""
				last_word = word
				a_list = [str(doc)+":"+str(pos)+";"]
		str_head = last_word+"\t"
		for i in a_list:
			str_head += i
		print(str_head)
		connection.commit() #save change
	except Error as e:
		 exit("Error occurs when get information from databasess")
	return
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
			return False
		else:
			return True

if __name__ == "__main__":
	main()

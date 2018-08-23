#!/usr/bin/env python3 

#python3 createIndex.py /Users/haotianzhu/Documents/CMPUT397/assignment1/test/

import sys
import glob
import os
import nltk
import sqlite3
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer


path = None
dict = None
stop_words = None

'''
init dict and stop words set
'''
def init():
	global dict,stop_words
	dict = {}
	stop_words = set(stopwords.words("english"))


'''
check command line size and path
'''
def checkArgv():
	global path
	if len(sys.argv) != 2:
		print("Error(please try one of ways to run program):")
		print("\t$ python3 createIndex.py path")
		return False
	else:
		path = sys.argv[1]
		if os.path.isfile(path):
			print("Error(please try one of ways to run program):")
			print("\t$ python3 createIndex.py path")			
			return False
		else:
			return True

'''
read file and tokenize each word,
get information that will be stored in database later
'''
def readDoc(filepath):
	global dict
	fp = open(filepath,"r")
	filename = findDocName(filepath)

	tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
	wnl = WordNetLemmatizer()

	pos = 0
	for line in fp :
		for element in tokenizer.tokenize(line):
			aword  = element.lower()
			if aword in stop_words:
				continue
			lema_word = wnl.lemmatize(aword)
			try: 
				if filename not in dict[lema_word]:
					dict[lema_word].append((filename,pos))
			except KeyError as e:
				dict[lema_word] = [(filename,pos)]
			pos += 1
'''
extract file name from file path
'''	
def findDocName(filepath):
	return filepath.split(".")[-2].split("/")[-1].split("_")[1]


'''
connect to database
'''
def connectionDataBase(data_file_name):
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Error as e:
		exit("can not connect to database")

'''
create table in database
'''
def executeContraints(connection):
	cur = connection.cursor() #get cursor
	try:
		cur.execute("PRAGMA foreign_keys = ON")
		cur.execute("PRAGMA journal_mode = OFF")
		cur.execute("DROP TABLE IF EXISTS posting;")
		cur.execute("CREATE TABLE posting (doc INT, word TEXT, position INT);")
		connection.commit() #save change
	except Error as e:
		print(e)
	return

'''
execute query
'''
def executeQury(connection,query,data):
	#this function to execute query. parameter: connection(def in func connectionDataBase), query(string: the sqlite3 query)
	try:
		cur = connection.cursor() #get cursor
		cur.executemany(query,data)
		connection.commit()
	except Error as e:
		exit("Error when insert data to database")
	return

'''
convert dict to a list => [(doc,term,pos), ...]
'''
def convertDictToList(data_list):
	for term in dict:
		for (doc , pos) in dict[term]:
			data_list.append( (doc,term,pos) )
	return


def main():

	if not checkArgv():
		return -1

	init()
	for filepath in glob.glob(os.path.join(path, '*.txt')):
		try:
			readDoc(filepath)
		except Exception as e:
			print("Error",e)
			raise
			continue
	data_list = []
	data_file_name = path + "/data.db"      #data stored file
	convertDictToList(data_list)
	
	connection = connectionDataBase(data_file_name) #connected to database file

	executeContraints(connection)

	executeQury(connection,"INSERT INTO posting VALUES(?,?,?) ",data_list)

	connection.close()
	return 0



if __name__ == "__main__":
	main()
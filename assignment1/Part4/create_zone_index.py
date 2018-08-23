#!/usr/bin/env python3 



import sys
import glob
import os
import nltk
import sqlite3
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer


input_path = None
output_path = None
b_dict = None
t_dict = None
stop_words = None


def init():
	global b_dict,stop_words,t_dict
	b_dict = {}
	t_dict = {}
	stop_words = set(stopwords.words("english"))


def checkArgv():
	global input_path,output_path

	if len(sys.argv) != 3:
		print("Error(please try one of ways to run program):")
		print("\n\t1.$ make all\n\t  $ ./create_zone_index.py input_path output_path")
		print("\n\t2.$ python3 ./create_zone_index.py input_path output_path")
		return 0
	input_path = sys.argv[1]
	output_path = sys.argv[2]
	return 1


def readDoc(filepath):
	global b_dict,t_dict
	fp = open(filepath,"r")
	filename = findDocName(filepath)
	title_terms = getTitleString(filepath)
	tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
	wnl = WordNetLemmatizer()



	pos = 0
	for term in tokenizer.tokenize(title_terms):
		aterm = term.lower()
		if term in stop_words:
			continue
		lema_term = wnl.lemmatize(aterm)
		try:
			if filename not in t_dict[lema_term]:
				t_dict[lema_term].append((filename,pos))
		except KeyError as e:
			t_dict[lema_term] = [(filename,pos)]
		pos += 1

	pos = 0
	for line in fp :
		for element in tokenizer.tokenize(line):
			aword  = element.lower()
			if aword in stop_words:
				continue
			lema_word = wnl.lemmatize(aword)
			try: 
				if filename not in b_dict[lema_word]:
					b_dict[lema_word].append((filename,pos))
			except KeyError as e:
				b_dict[lema_word] = [(filename,pos)]
			pos += 1

	return
			
def findDocName(filepath):
	try:
		return filepath.split(".")[-2].split("/")[-1].split("_")[1]
	except Exception as e:
		print("doc name error cannot read this file's name")
		raise
		return -1


def getTitleString(filepath):
	try:
		return " ".join(filepath.split("/")[-1].split(".")[-2].split("_")[2:])
	except Exception as e:
		print("doc name error cannot read this file's name")
		raise

def connectionDataBase(data_file_name):
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Error as e:
		print(e)
		raise
	return -1


def executeContraints(connection):
	cur = connection.cursor() #get cursor
	try:
		cur.execute("PRAGMA foreign_keys = ON")
		cur.execute("PRAGMA journal_mode = OFF")
		cur.execute("DROP TABLE IF EXISTS body_posting;")
		cur.execute("DROP TABLE IF EXISTS title_posting;")
		cur.execute("CREATE TABLE body_posting (doc INT, word TEXT, pos INT);")
		cur.execute("CREATE TABLE title_posting (doc INT, word TEXT, pos INT);")
		connection.commit() #save change
	except Error as e:
		print(e)
	return

def executeQury(connection,query,data):
	#this function to execute query. parameter: connection(def in func connectionDataBase), query(string: the sqlite3 query)
	cur = connection.cursor() #get cursor
	try:
		cur.executemany(query,data)
		connection.commit()
	except Error as e:
		print(e) 
		raise
	return

def convertb_dictToList(data_list,data_list2):
	for term in b_dict:
		for (doc , pos) in b_dict[term]:
			data_list.append( (doc,term,pos) )
	for term in t_dict:
		for (doc , pos) in t_dict[term]:
			data_list2.append( (doc,term,pos) )
	return


def main():

	if not checkArgv():
		return -1

	init()

	for filepath in glob.glob(os.path.join(input_path, '*.txt')):
		try:
			readDoc(filepath)
		except Exception as e:
			print("Error",e)
			raise
			continue

	t_list = []
	b_list = []
	convertb_dictToList(b_list,t_list)


	connection = connectionDataBase(output_path+"/zdata.db") #connected to database file
	executeContraints(connection)

	executeQury(connection,"INSERT INTO title_posting  VALUES(?,?,?) ",t_list)
	executeQury(connection,"INSERT INTO body_posting  VALUES(?,?,?) ",b_list)

	connection.close()
	return 



if __name__ == "__main__":
	main()
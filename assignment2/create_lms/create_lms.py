# !/usr/bin/env python3 
import sys
import glob
import os
import nltk
import sqlite3
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer


'''
global variables
path: the document path
dict_list a list contains all file's dict
global_list a list contains all file's length 
file_list contains all filename
'''
path = None
dict_list = []
global_list = []	
filename_list =[]
stop_words = None
out_path = None
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
	global path,out_path
	if len(sys.argv) != 3:
		print("Error(please try one of ways to run program):")
		print("\t$ python3 create_lms.py input_path out_path")
		return False
	else:
		path = sys.argv[1]
		out_path = sys.argv[2]
		if os.path.isfile(path):
			print("Error(please try one of ways to run program):")
			print("\t$ python3 create_lms.py path")		
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
	filename_list.append(filename)
	# [dic1 dict2 dict3] each dict is a dictionary
	# whose key = term and value = count
	file_dict ={}
	dict_list.append(file_dict)


	tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
	wnl = WordNetLemmatizer()

	pos = 0
	count = 0
	# here we store term raw count information
	for line in fp :
		for element in tokenizer.tokenize(line):
			aword  = element.lower()
			if aword in stop_words:
				continue
			count += 1
			lema_word = wnl.lemmatize(aword)
			try:
				file_dict[lema_word]+=1
			except KeyError as e:
				file_dict[lema_word] = 1

	# here calcualte probability
	for k in file_dict.keys():
		file_dict[k] /= count
	
	global_list.append([filename,count])
	

'''
extract file name from file path
'''	
def findDocName(filepath):
	return filepath.split(".")[-2].split("/")[-1].split("_")[1]


'''
connect to database
'''
def connectionDataBase(data_file_name):
	# create a connection to database with file name "data_file_name", if error print it out
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
		cur.execute("DROP TABLE IF EXISTS models;")
		cur.execute("CREATE TABLE models (doc INT, term TEXT, probability float);")
		cur.execute("DROP TABLE IF EXISTS countt;")
		cur.execute("CREATE TABLE countt (doc INT, c int);")
		connection.commit() #save change
	except Error as e:
		print(e)
	return

'''
execute query
'''
def executeQury(connection,query,data):
	# this function to execute query. parameter: connection(def in func connectionDataBase), query(string: the sqlite3 query)
	try:
		cur = connection.cursor() #get cursor
		cur.executemany(query,data)
		connection.commit()
	except Error as e:
		exit("Error when insert data to database")
	return

'''
convert dict to a list

'''
def convertDictToList(data_list): #dict_list
	for i in range(len(dict_list)):
		adict = dict_list[i]
		name = filename_list[i]
		for akey in adict:
			data_list.append( (name,akey,adict[akey]) )
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
	data_file_name = out_path + "/data.db"      #data stored file
	convertDictToList(data_list)
	connection = connectionDataBase(data_file_name) #connected to database file
	executeContraints(connection)
	executeQury(connection,"INSERT INTO models VALUES(?,?,?) ",data_list)
	executeQury(connection,"INSERT INTO countt VALUES(?,?) ",global_list)
	connection.close()
	return 0



if __name__ == "__main__":
	main()

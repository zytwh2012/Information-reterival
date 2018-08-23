#!/usr/bin/env python3 
import sys
import glob
import os
import nltk
import sqlite3
import os.path
import numpy as np
import math
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

dict_tf = None
path = None
k = None
score = None
query_terms = None
query_terms_tf = None
query_weight = None
score_rank =None
score_length = None
stop_words = set(stopwords.words("english"))

def main():

	if not checkArgv():
		print("Error(please try one of ways to run program):")
		print("\t$ python3 vs_query.py path k score term1 term2 ...")
		return -1
		
	if not os.path.isfile(path) :
		print("Error no index file ")
		return -1;

	#begin connection
	connection = connectionDataBase(path)
	#create user define function log in sqlite3
	connection.create_function("log", 1, findLogX)

	getTIDF(connection)
	showResult(connection)

	#close connection
	connection.close()

	
	return 1;



def checkArgv():
	global path,k,query_terms,score,query_terms_tf,score_length,score_rank
	if len(sys.argv) < 5:
		print("Error")
		return False
	else:
		path = sys.argv[1]

		try:
			k = int(sys.argv[2])
		except ValueError as e:
			print("Error\nk should be integer")
			return False

		score = sys.argv[3]
		if score not in ['y','n']:
			print("Error\nscore should be y or n")
			return False

		wnl = WordNetLemmatizer()
		query_terms = []
		query_terms_tf = {}
		for i in range(4,len(sys.argv)):
			lower_term =sys.argv[i].lower()
			if lower_term not in stop_words:
				lema_term = wnl.lemmatize(lower_term)
				if lema_term not in query_terms:
					query_terms.append(lema_term)
					query_terms_tf[lema_term] = 1
				else:
					query_terms_tf[lema_term] += 1
		score_rank = {}
		score_length = {}


	return True


def connectionDataBase(data_file_name):
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Error as e:
		print(e)
		return


def parseData(connection):
	try:
		cur = connection.cursor()
	except Exception as e:
		print(e)
		raise


def findLogX(x):
	return math.log(x,10)

#log(10.0*t3.tf)
def getTIDF(connection):
	global score_rank,score_length
	query_begin  =	'''	with word_t(word,num) as(
						select word as word, count(distinct(doc)) as num
						from posting
						group by word ),
						 total_num(total) as(
						select count(distinct(doc))*(1.0)
						from  posting),
						ctf(word,doc,tf) as(
						select word, doc, count(*)
						from posting
						group by word,doc)
						select t3.doc,t3.word, log(10.0*t3.tf)*log(t2.total/t1.num),log(t2.total/t1.num)
						from ctf t3,word_t t1,total_num t2
						where t3.word = t1.word and (
					'''
	query_end = '''
						)group by t3.doc, t3.word
						order by  t3.doc ASC
				'''	
	query = query_begin
	for term in query_terms[:-1]:
		query += "t1.word = \"" + term + "\" or "
	query += "t1.word = \""+  query_terms[-1]+ "\" "
	query += query_end
	try:
		cur = connection.cursor()
	except Exception as e:
		raise

	query_legth = 0
	query_checked = []
	for (doc, word, doc_weight,dif_weight) in cur.execute(query): 
		if word not in query_checked:
			query_checked.append(word)
			query_legth += dif_weight*dif_weight
		try:
			score_rank[doc] += doc_weight*(dif_weight)
			score_length[doc] += doc_weight*doc_weight
		except KeyError:
			score_rank[doc] = doc_weight*(dif_weight)
			score_length[doc] = doc_weight*doc_weight


	query_legth = math.sqrt(query_legth)

	for key in score_length:
		score_length[key] = math.sqrt(score_length[key])


	for key in score_rank:
		try:
			score_rank[key] = score_rank[key]/(score_length[key]*query_legth)
		except ZeroDivisionError:
			score_rank[key] = 0


	return


def getRootList(connection):
	try:
		cur = connection.cursor()
	except Exception as e:
		raise
	return [ i for (i, ) in  cur.execute("SELECT distinct(doc) FROM posting ")]


def showResult(connection):
	i = 0
	flag = 0
	for v in reversed(sorted(score_rank.values())):
		for key in score_rank:
			if score_rank[key] == v:
				if score == 'y':
					print("%s\t%lf" %(key,v))
				else:
					print("%s\t" %(key))
				i+=1
				if i == k or i == len(score_rank):
					flag = 1
					break
		if flag == 1:
			break

	if i < k:
		for item in getRootList(connection):
			if item not in score_rank.keys():
				if i < k:
					print("%s\t%lf" %(item,float(0)))
					i += 1
	if i < k :
		exit("The k value bigger than all doc..")

	return




if __name__ == "__main__":
	main()
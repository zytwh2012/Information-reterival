#!/usr/bin/env python3 
import sys
import nltk
import sqlite3
from operator import itemgetter, attrgetter
from sqlite3 import Error
from nltk.stem.wordnet import WordNetLemmatizer
import utils as uts


def connectionDataBase(data_file_name):
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Error as e:
		print(e)
		return

def score(g,query,connection,cur):
	result = {}
	all_ids = [ i for (i, ) in  cur.execute("SELECT distinct(doc) FROM body_posting  order by doc DESC")]
	result_body = uts.theMain(1,query,connection)
	result_title = uts.theMain(0,query,connection)


	for doc_id in all_ids:
		score = 0
		if doc_id in result_body:
			score += g
		if doc_id in result_title:
			score += 1-g
		result[doc_id] = score
		score = 0
	return result 


def checkArgv():
	global path
	if len(sys.argv) != 4:
		return False
	else:
		return True

def showResult(connection,score_rank,k):
	i = 0
	flag = 0
	for v in reversed(sorted(score_rank.values())):
		for key in score_rank:
			if score_rank[key] == v:
				print("%s %lf" %(key,v))
				i+=1
				if i == k or i == len(score_rank):
					flag = 1
					break
		if flag == 1:
			break

	if i < k :
		exit("The k value bigger than all doc..")

	return

def main():
	#check argument and inlization query
	if not checkArgv :
		exit("Error, illegal command line")
	database = sys.argv[1]
	try:
		k = int(sys.argv[2])
	except Exception:
		exit("Error, illegal command line")
	try:
		g = float(sys.argv[3])
	except Exception:
		exit("Error, illegal command line")

	if g > 1.0 or g < 0.0:
		exit("Error, illegal command line")
	q = sys.argv[4]

	try:
		# connect to database
		connection = connectionDataBase(database)
		cur = connection.cursor()
	except Exception as e:
		exit("Error, can not connect to database")



	#compute and print result
	result = score(g,q,connection,cur)
	showResult(connection,result,k)
	return
			

main()
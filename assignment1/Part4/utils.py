import sys
import glob
import os
import nltk
import sqlite3
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer,SExprTokenizer
from nltk.stem.wordnet import WordNetLemmatizer



stop_words = None
wnl = None
title_or_body = 1
'''
this function is to get term information from database
two cases: 1. phase term 2.single term
'''
def getListFromDataBase(element_list):
	element_list =  [deBracket(element_list[0])]
	result = []
	position_postings = []

	try:
		cur = connection.cursor()
	except Exception as e:
		exit("Error occurs when connect to database")

	if " " in element_list[0]:
		#remove " and break phrase into tokens
		terms = element_list[0].split()
		count = 1
		for token in terms:
			if token in stop_words:
				count+=1
			else:
				token = wnl.lemmatize(token.lower())
				position_posting = []
				last_doc = -1
				a_list = []	
				if title_or_body:				
					for (doc,pos) in cur.execute("SELECT doc,pos FROM body_posting  WHERE word = ? order by doc ASC, pos ASC",(token,)):
						# if doc = last doc => doc id same
						if doc == last_doc:
							# add position to a_list
							a_list.append(pos)
						# if old doc end and begin new doc
						else:
							# if it is not the frist doc
							if last_doc != -1:
								# add list into position_posting 1261
								position_posting.append(a_list)
							# add doc id in list so that each list struct as following: [doc,pos,pos,pos]
							a_list = [doc,pos]
							last_doc = doc
				else:
					for (doc,pos) in cur.execute("SELECT doc,pos FROM title_posting  WHERE word = ? order by doc ASC, pos ASC",(token,)):
						# if doc = last doc => doc id same
						if doc == last_doc:
							# add position to a_list
							a_list.append(pos)
						# if old doc end and begin new doc
						else:
							# if it is not the frist doc
							if last_doc != -1:
								# add list into position_posting 1261
								position_posting.append(a_list)
							# add doc id in list so that each list struct as following: [doc,pos,pos,pos]
							a_list = [doc,pos]
							last_doc = doc


				position_posting.append(a_list)
				position_postings.append(position_posting)	

		# if only stop word
		if count >= len(terms):
			return None
		#else find result	
		length = len(position_postings)	
		result = position_postings[0]
		for i in range(length):
			if i+1 <= (length-1): 
				result = (positionCheck(result,position_postings[i+1]))
		result = [ r[0] for r in result]
	else:
		a_word = element_list[0]
		if a_word == "OR" or a_word == 'AND' or a_word =="NOT":
			sys.exit("Illegal query!")
		a_word = wnl.lemmatize(a_word.lower())
		if a_word in stop_words:
			result = None
		else:
			result = []
			if title_or_body:
				for (doc,) in  cur.execute("SELECT distinct doc FROM body_posting WHERE word = ?",(a_word,)):
					result.append(doc)
			else:
				for (doc,) in  cur.execute("SELECT distinct doc FROM title_posting WHERE word = ?",(a_word,)):
					result.append(doc)				
	return result
'''
when phase term, go to check its position and find result
'''
def positionCheck(p1,p2): 
	result = []
	if p1 == [[]] or p2 == [[]]:
		return result
	for p1_list in p1:
		for p2_list in p2:
			if p1_list[0] == p2_list[0]: # doc same go to check
				p1_positions = p1_list[1:]
				p2_positions = p2_list[1:]
				a_list = [p1_list[0]] #add doc id
				for p1_pos in p1_positions:
					for p2_pos in p2_positions:
						if (p1_pos+1) == p2_pos:
							a_list.append(p2_pos)
				if len(a_list) > 1:
					result.append(a_list)
				a_list = []
	return result
'''
this function is to calcuate a binary operator with most 2 terms
None => when the term is a stop word
''' 	
def getAndOrNot(a,t,b):
	if a == None :
		return b
	if b == None :
		return a
	a = set(a)
	b = set(b)

	if t == "AND":
		return list(a.intersection(b))

	elif t == "OR":
		return list(a.union(b))
	elif t == "NOT":
		return list(a.difference(b))
	
	sys.exit("Error")
	return

'''
main recursive function
first check if quert_list only contains one term(or one phase term)
if not go to calcuate result ex: A AND B
if yes go to database to get result ex: A
do calculate from left side to right side if they are at same level
'''
def getResult(query_list):
	result = None
	if len(query_list) == 1:
		query_list = breakQuery(query_list[0])
		if len(query_list) == 1:
			return getListFromDataBase(query_list)
	index = 0 #""
	count = 0 # avoid "a and and a"
	for t in query_list:
		if t in ["AND","OR","NOT"]:
			count = 0
			if index == 1 :
				sub_query = query_list[index-1]
				result = getResult([sub_query])

			sub_query = query_list[index+1]
			right = getResult([sub_query])
			if index == 0 and t =="NOT" and right != None:
				result = getRootList()
			elif index == 0 and(t =="AND" or t =="OR"):
				sys.exit("Illegal query!")
			result = getAndOrNot(result,t,right)
		else:
			count += 1
			if count > 1:
				sys.exit("Illegal query!")

		index += 1
	return result
'''
replace all " or '  with ( and )
check input query is legal or not
'''
def replaceQuot(query):
	flag = -1
	output = ""
	count = 0
	a_list = query.split('"')
	for e in a_list:
		if flag == -1:
			output+=e
			flag = 0
		elif flag == 0: # find first "
			output+= " ( "+e
			count+=1
			flag = 1

			if " NOT " in e or " OR " in e or " AND " in e:
				sys.exit("Illegal query!")

		elif flag == 1:
			output+= " ) "+e
			count+=1
			flag = 0
	if count%2 != 0:
		sys.exit("Illegal query!")
	return output
#connect to database
def connectionDataBase(data_file_name):
	#create a connection to database with file name "data_file_name", if error print it out
	try:
		connection = sqlite3.connect(data_file_name)
		return connection
	except Error as e:
		exit("Error, can not connect to database")

def removeEmpty(query_list):
	out = []
	notEmpty = 0
	for i in query_list:
		for j in range(0,len(i)):
			if i[j] != ' ' and i[j] != '':
				notEmpty = 1
		if notEmpty:
			out.append (i)
		notEmpty = 0
	return out
'''
shrink oversized blanks
ex: "A   AND B"=> "A AND B"
'''
def  resetBlank(query):
	flag = 0
	out =""
	for i in query:
		if i == "(" or i == ")":
			out += " "
			flag = 1
		out += i
		if flag :
			out+=" "
			flag = 0
	query = out

	flag = 0
	first = 1
	out = ""
	for e in query:
		if e != " ":
			out+=e
			first = 0
			flag = 1
		else:
			if first == 0 and flag == 1 :
				out+=e
				flag = 0
	if out[-1] == " ":
		return out[:-1]
	else:
		return out

'''
#get all doc ids in database
'''
def getRootList():
	try:
		cur = connection.cursor()
	except Exception as e:
		raise

	return [ i for (i, ) in  cur.execute("SELECT distinct(doc) FROM body_posting ")]

'''
prune pointless brackets
ex: (A AND B) => A tAND B
'''
def deBracket(query):
	flag = 1 
	temp_query_list = tokenize(query)
	if len(temp_query_list)!= 1:
		return query

	while( len(temp_query_list) == 1 and flag) :
		temp_query = temp_query_list[0]
		if temp_query[0]=="(" and temp_query[-1]==")":
			left_sum = 0
			right_sum = 0
			end_point = 0
			for end_point in range(0,len(temp_query)):
				if temp_query[end_point] == "(":
					left_sum += 1
				elif temp_query[end_point] == ")":
					right_sum += 1
				if left_sum == right_sum:
					break
			if end_point == len(temp_query)-1 :
				temp_query_list = [temp_query[1:-1]]
			else:
				return temp_query_list[0]
		elif temp_query[0] == " " :
			temp_query_list = [temp_query[1:]]
		elif temp_query[-1] == " " :
			temp_query_list = [temp_query[:-1]]
		else:
			flag = 0
	return temp_query_list[0]
 
'''
two cases two make a query split into list
1. query has subquery 
2. query is composed of terms(phase or normal)
'''
def breakQuery(query):
	if " AND " in query or " NOT " in query or " OR " in query or "(" in query[1:-1] or ")" in query[1:-1]:
		sub_query = deBracket(query)
		query_list = tokenize(sub_query)
		query_list = removeEmpty(query_list)
		return query_list
	else:
		return tokenize(query)
'''
splite query according to bracket
only split the hightest level brackets
'''
def tokenize(query):
	a_query = query + " ()"
	a_list = SExprTokenizer().tokenize(a_query)
	return a_list[:-1]


def theMain(input_title_or_body,input_query,input_connection):
	global path,connection,wnl,stop_words,title_or_body
	
	title_or_body = input_title_or_body

	query = input_query

	#connect to database
	connection = input_connection

	
	#init tokenlization
	wnl = WordNetLemmatizer()
	stop_words = set(stopwords.words("english"))#stopwords


	try:
		#handle query
		query = replaceQuot(query)
		query = resetBlank(query)
		query_list = breakQuery(query) 
		result = getResult(query_list)
	except IndexError:
		sys.exit("Illegal query!")
	except ValueError:
		sys.exit("Illegal query!")
	#compute result
	
	if result!=None:
		result.sort()
	else:
		result = []

	return result





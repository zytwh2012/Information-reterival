#!/usr/bin/env python3 
import sys
import os
import sqlite3
import os.path
import math
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

dict_tf = None
path = None
k = None
score = None
query_terms = None
count_dict = None
score_rank = None
stop_words = set(stopwords.words("english"))


def main():
    if not check_argv():
        print("Error(please try one of ways to run program):")
        print("\t$ python3 query_lms.py path k 'term1 term2 ...' ")
        return -1

    if not os.path.isfile(path):
        print("Error no index file ")
        return -1

    # begin connection
    connection = connection_data_base(path)
    # create user define function log in sqlite3
    connection.create_function("log", 1, find_log)

    result_getter(connection)

    show_result(connection)

    # close conncount_dictection
    connection.close()

    return 1


def check_argv():
    global path, k, query_terms, score_rank
    if len(sys.argv) != 4:
        return False
    else:
        path = sys.argv[1]

        try:
            k = int(sys.argv[2])
        except ValueError as e:
            print("Error\nk should be integer")
            return False
        wnl = WordNetLemmatizer()
        query_terms = []
        terms = sys.argv[3].split()
        if len(terms) < 1:
            print("query is none")
            return False
        for i in terms:
            lower_term = i.lower()
            if lower_term not in stop_words:
                lema_term = wnl.lemmatize(lower_term)
                query_terms.append(lema_term)
        score_rank = {}
    return True


def connection_data_base(data_file_name):
    # create a connection to database with file name "data_file_name", if error print it out
    try:
        connection = sqlite3.connect(data_file_name)
        return connection
    except Exception as e:
        print(e)
        return


def smoothing(document_probability, collection_probability):
    # lambda
    lam = 0.5
    d_given_md = document_probability
    t_given_d = lam * d_given_md + (1-lam) * collection_probability
    return find_log(t_given_d)


def find_log(x):
    return math.log(x, 10)


def result_getter(connection):
    global path, k, query_terms, score_rank,count_dict
    try:
        cur = connection.cursor()
    except Exception as e:
        print(e)
        raise
    
    count_dict = dict()
    query = '''
            WITH t(le) as(
                SELECT SUM(c.c)
                FROM countt c)
            SELECT m.term, SUM(m.probability*c.c)/t.le
                FROM countt c, models m, t
                WHERE c.doc = m.doc
                GROUP BY m.term
            '''
    for (t,p) in cur.execute(query):
        count_dict[t] = p


    query = ''' 
                SELECT m.doc,m.term, m.probability
                FROM models m
                WHERE 
            '''

    for i in range(len(query_terms)):
        if i == 0:
            query += " term = '" + str(query_terms[i])+"'"
        else:
            query += " OR term = '"+ str(query_terms[i])+"'"
    query+=" group by m.doc, term order by m.doc"


    
    doc_list =[]
    q = "select doc from countt "
    for (item,) in cur.execute(q):
        doc_list.append(item)

    last_doc = None
    product = None
    full_list = list(query_terms)
    for (doc,term,prob) in cur.execute(query):
        
        if doc in doc_list:
            doc_list.remove(doc)
        count = query_terms.count(term)

        for i in range(count):
            if doc == last_doc:
                full_list.remove(term)
                product += smoothing(prob,count_dict[term])
            else:
                if last_doc is not None:
                    for fl in full_list:
                        try:
                            product += smoothing(0,count_dict[fl])
                        except KeyError as e:
                            product += 0
                    score_rank[last_doc] = product
                    last_doc = doc
                    product = smoothing(prob,count_dict[term])
                    full_list = list(query_terms)
                    full_list.remove(term)
                else:
                    last_doc = doc
                    product = smoothing(prob,count_dict[term])
                    full_list.remove(term)

    if last_doc :
        score_rank[doc] = product
    
    for i in doc_list:
        product = 0
        for j in query_terms:
            try:
                product += smoothing(0,count_dict[j])
            except KeyError as e:
                product += 0
        score_rank[i] = product

    return

def show_result(connection):
    i = 0
    flag = 0
    if k <=0:
        return
    for v in reversed(sorted(score_rank.values())):
        for key in score_rank:
            if score_rank[key] == v:
                print("%s\t%lf" %(key,v))
                i+=1

                if i == k or i == len(score_rank):
                    flag = 1
                    break
        if flag == 1:
            break

    if i < k:
        try:
            cur = connection.cursor()
        except Exception as e:
            print(e)
            raise

        q = "select doc from countt "
        for (item,) in cur.execute(q):
            if item not in score_rank.keys():
                if i < k:
                    print(item,"\t",float(0))
                    i += 1
    if i < k :
        exit("The k value is bigger than numebr of docs..")

    return


if __name__ == "__main__":
	main()
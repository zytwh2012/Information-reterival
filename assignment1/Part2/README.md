### HOW TO RUN PROGRAMS:

#### 1. boolean_query.py

```bash
$ chmod +x boolean_query.py
$ ./boolean_query.py the_path_to_database query
```

or 

```bash
$ python3 boolean_query.py the_path_to_database query 
```

PS: Query has to be enclosed by ''. Otherwise, the query will produce undesirable result.
    Ex: 'A AND C' , '"a phase term" OR term ', ' "a phase term"  '
    
    assumptions: 
    1. If there are no parentheses in a query operator are processed in sequential order.
    2. Dual NOT without parrenthese are not allowed.(Ex: 'NOT NOT A' is not allowed,however 'NOT (NOT A)' is allowed)
    3. Operator is not allowed in a phrase query.

### WHAT DATABASE CONTAIN

The  documents number(0,3,6,9,...,27,30) from "2k movies" on e-class.
table schema:CREATE TABLE posting (doc INT, word TEXT, position INT);



#### OUR UNIT TESTS

```bash
$ python3 test.py
```

We have 9 different unit tests for  program in part3:

**Note**:  Make sure that you have boolean.py ,test.py and data.db in the same directory.

query1: surprise
answer1:[0, 21]

query2: surprise OR version
answer2:[0, 21, 24]

query3: surprise AND version
answer3:[]

query4: (surprise AND montage) OR version
answer4:[21, 24]

query5: surprise OR duffle OR version
answer5:[0, 12, 21, 24]

query6: important AND film AND story
answer6:[9]

query7: important OR film OR duffle AND surprise OR story
answer7:[0, 9, 21, 24]

query8: 'Dominic Toretto' AND 'US Customs agents'
answer8:[12]

query9: 'Ming the Merciless' OR 'US Customs agents'
answer9:[12, 24]

[Back to main page](../)



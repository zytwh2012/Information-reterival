### HOW TO RUN PROGRAMS:

#### 1. create_zone_index.py

```bash
$ chmod +x create_zone_index.py 
$ ./create_zone_index.py the_path_to_directory the_path_to_database
```

or 

```bash
$ python3 create_zone_index.py the_path_to_input_directory the_path_to_index_directory
```

#### 2. zone_scorer.py

```bash
$ chmod +x zone_scorer.py 
$ ./zone_scorer.py index_dir k g q
```

or 

```bash
$ python3 zone_scorer.py index_dir k g q
```

PS: 
    
    utils.py and zone_scorer.py have to be in the same directory
    k is the number of documents displayed
    g critical value between 0 to 1
    q is boolean query
    Query has to be enclosed by ''. 
    Ex: 'A AND C' , '"a phase term" OR term ', ' "a phase term"  '
    

### WHAT DATABASE CONTAIN

The  documents from "2k movies" on e-class.

table schema:

    CREATE TABLE body_posting (doc INT, word TEXT, pos INT);
    CREATE TABLE title_posting (doc INT, word TEXT, pos INT);


#### OUR UNIT TESTS

```bash
$ python3 test.py
```

We have 3 different unit tests for  program in part4:

**Note**:  Make sure that you have zone_scorer.py ,test.py and zdata.db in the same directory.

input1: k = 5, g = 0.3, query = Absence 

answer1:

    57 1.000000
    19 0.300000
    71 0.300000
    126 0.300000
    218 0.300000
  

input2 k = 4, g = 0.4, query = Malice

answer2:

    57 0.600000
    391 0.400000
    0 0.000000
    1 0.000000

input3 k = 2, g = 0.7, query = "Air America"

answer3:

    72 1.000000
    0 0.000000

[Back to main page](../)

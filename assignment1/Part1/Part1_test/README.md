### WHAT DOCUMENTS CONTAIN

The source of documents in folder Documents is from "2k movies" in e-class.



#### OUR UNIT TESTS

We have different unit test files for two program in part1:

**Note**:  Make sure that run program under Part1_test

You can run our unit test by 

```bash
$ cd the_path_to_Part1_test_folder
$ python3 create_index_unit_test.py
```

the result looks like(if pass):

```
The documents and python script are correct...
checking...
test_checkLemmatize (__main__.TestStringMethods) ... ok
test_checkStopWords (__main__.TestStringMethods) ... ok
test_format (__main__.TestStringMethods) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

```



#### create_index_unit_test.py

In this unit test file, we have three test functions:

1.  check if there is a stopword in database.
2.  check if a noun word is be lemmatized
3.  check if data form is correct 


#### print_index_unit_test.py

In this unit test file, we have three test functions:

1. check if all words in database been printed
2. check if the word "angle" is printed correctly
3. check if the word "year" is printed correctly



 [back to main page](../../)

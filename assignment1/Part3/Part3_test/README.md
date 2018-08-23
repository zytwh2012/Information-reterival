### WHAT DOCUMENTS CONTAIN

Documents contains 4 documents created by 

- doc1: one two three four five six seven
- doc2: one three five seven
- doc3: one six six six two



#### OUR UNIT TESTS

In Part3_test, there is a data.db which contains the inverted index information.

**Note**:  Make sure that run program under Part3_test

You can run our unit test by 

```bash
$ cd the_path_to_Part3_test_folder
$ python3 vs_query_unit_test.py
```

If you want to create index file again

```bash
$ python3 create_index.py ../Part3/Part3_test/Documents/
```

To print the index file:

```bash
$ python3 print_index.py ../Part3/Part3_test/Documents/
```

the result looks like(if pass):

```
The documents and python script are correct...
checking...
test_illegalInput (__main__.TestStringMethods) ... ok
test_query_one (__main__.TestStringMethods) ... ok
test_query_three (__main__.TestStringMethods) ... ok
test_query_two (__main__.TestStringMethods) ... ok

----------------------------------------------------------------------
Ran 4 tests in 8.132s

OK

```



In this unit test file, we have three test queries:

1. input: "one" 
2. input:"ten", "NINE" 
3. input: two three
4. illegal command line input




 [back to main page](../../)

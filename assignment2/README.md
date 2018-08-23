# Assignment 2 README:

Please do not change structure of the folder of assignment2



#### Part1



##### create_lms:

create_lms.py in folder /assignment2/create_lms

under creat_lms folder:

```bash
$ python3 create_lms.py [path to Documents folder] [path to output folder]
```

Note: we assume documents' formates are same as last assignment moves_2k_source. For example, doc_1_haha_haha.txt, we only save doc id which in this example is 1.

##### unit test:

test_create_lms.py in folder /assignment2/create_lms

under creat_lms folder:

```bash
$ python3 create_lms.py ./Documents ./Documents
$ python3 test_create_lms.py
```



##### print_lms:

print_lms.py in folder /assignment2/print_lms

under print_lms folder:

```bash
$ python3 print_lms.py [path to database file]
```

Path to document which contains database file

##### unit_test:

test_print_lms.py in folder /assignment2/create_lms

under print_lms folder:

```bash
$ python3 ../create_lms/create_lms.py ../create_lms/Documents ../create_lms/Documents
$ python3 test_print_lms.py
```



##### query_lms:

query_lms.py in folder /assignment2/query_lms

under query_lms folder:

```bash
$ python3 query_lms.py [path to data file] [k] ['term1 term2 term3']
```

Note: whole terms should be inclose by quote

##### unit_test:

under query_lms folder:

```bash
$ python3 ../create_lms/create_lms.py ../create_lms/Documents ../create_lms/Documents
$ python3 query_lms_test.py
```



#### Part2

Note: this program costs about a half hour in my macbook pro.

Here is my example running test:

```bash
$ time python3 nb_classifier.py ~/Downloads/trec-397/data/train ~/Downloads/trec-397/data/test
Training Accuracy:  0.7595
Testing Accuracy:  0.771
python3 nb_classifier.py ~/Downloads/trec-397/data/train   548.48s user 523.38s system 91% cpu 19:26.71 total
```



How to run our program:

under nb_classifier folder

```bash
$ python3 nb_classifier.py [path to training folder] [path to test folder]
```



##### unit_test:

under nb_classifier folder 

```bash
$ python3 nb_classifier_test.py
```





**IMPORTANT**:

Please download NLTK 3.2.5. and install all packages [click here to see how to download](http://www.nltk.org/data.html) and use python3 to run our programs

- Tokenlization Library used: NLTK 3.2.5.  And we use Lemmatize to tokenize word, we only tokenize noun words.
- Stop word list used for Tokenlization:["you've", "mustn't", 'in', 'between', 'during', 'these', 'over', 'that', 'as', 'for', "hasn't", 'having', 'will', 'wasn', 'theirs', 'my', 'into', 'very', 'yourselves', 'who', 't', 'd', 'her', 'doing', 'm', 'should', 'only', 'if', 'wouldn', 'it', 'just', 'by', 'doesn', 'above', 'whom', 'isn', 'them', 'or', 'me', 'yourself', 'after', 'did', 'weren', "you'll", 'herself', 'the', 'once', 'he', 've', 'hers', 'own', 'mustn', 'does', 'hadn', "needn't", 'has', 'being', 'their', 'had', 'do', 'of', "couldn't", "shouldn't", 'didn', 'while', 'can', 'down', 'himself', 'have', 'his', 'been', "that'll", 'because', 'to', "don't", 'and', 'its', 'are', 'other', 'no', 'aren', 'why', 'this', 'from', 'ain', 'such', 'which', 'she', 'won', "wasn't", "didn't", 'ourselves', 'be', 'shan', 'but', 'themselves', "won't", 'o', 'on', 'each', 'under', 'some', 'they', "doesn't", 'y', 'you', 'll', "hadn't", 'couldn', 'a', 'here', "she's", 'any', 'haven', 'how', 's', "should've", 'too', 'not', 'through', "you'd", 'up', 'again', 'were', "you're", 'am', "mightn't", 'is', 'before', 'few', 'an', 'i', 'yours', 'until', 'we', 'your', 'mightn', 'itself', 'nor', 'below', 'off', 'at', 'than', 'out', 'more', 're', "isn't", 'was', 'there', 'him', "it's", 'most', 'all', 'what', 'about', "aren't", 'myself', 'those', 'shouldn', 'ours', 'so', 'needn', 'when', 'both', 'ma', 'with', 'further', 'hasn', "shan't", 'same', "weren't", "wouldn't", 'where', 'then', 'don', 'now', 'our', "haven't", 'against'](deafult english stop list from NLTK)
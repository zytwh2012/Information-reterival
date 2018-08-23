import unittest,os,io,sys,subprocess

class Test_boolean_query(unittest.TestCase):
    def test_query1(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "surprise"],)
        self.assertEqual(result,b'Here are the documents satisfy the query [0, 21]\n')

    def test_query2(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "surprise OR version"],)
        self.assertEqual(result,b'Here are the documents satisfy the query [0, 21, 24]\n')
    
    def test_query3(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "surprise AND version"],)
        self.assertEqual(result,b'Here are the documents satisfy the query []\n')
    def test_query4(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "(surprise AND montage) OR version"],)
        self.assertEqual(result,b'Here are the documents satisfy the query [21, 24]\n')
    def test_query5(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "surprise OR duffle OR version"],)
        self.assertEqual(result,b'Here are the documents satisfy the query [0, 12, 21, 24]\n')
    def test_query6(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "important AND film AND story"],)
        self.assertEqual(result,b'Here are the documents satisfy the query [9]\n')
    def test_query7(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", "important OR film OR duffle AND surprise OR story"],)
        self.assertEqual(result,b'Here are the documents satisfy the query [0, 9, 21, 24]\n')
    def test_query8(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", '"Dominic Toretto" AND "US Customs agents"'],)
        self.assertEqual(result,b'Here are the documents satisfy the query [12]\n')
    def test_query9(self):
        result = subprocess.check_output(["python3", "boolean_query.py", "./data.db", '"Ming the Merciless" OR "US Customs agents"'],)
        self.assertEqual(result,b'Here are the documents satisfy the query [12, 24]\n')
                               
if __name__ == '__main__':
    unittest.main()

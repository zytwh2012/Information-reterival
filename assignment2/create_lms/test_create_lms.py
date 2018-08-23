import create_lms
import sys
import unittest


class TestCreateLms(unittest.TestCase):
    def test_checkArgv(self):
        sys.argv = [sys.argv[0],None,None]
        sys.argv[1] = "./Documents"
        sys.argv[2] = "./Documents"
        self.assertEqual(create_lms.checkArgv(),True)

    def test_connectionDataBase(self):
        data_file_name = "./Documents/data.db"
        self.assertIsNot(create_lms.connectionDataBase(data_file_name),None)

    def test_findDocName(self):
        filepath = "doc_1200_a_name_10002.txt"
        self.assertEqual(create_lms.findDocName(filepath),"1200")


if __name__ == '__main__':
    unittest.main()

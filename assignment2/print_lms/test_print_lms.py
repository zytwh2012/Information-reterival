import print_lms
import sys
import unittest



class TestPrintLms(unittest.TestCase):
    def test_connectionDataBase(self):
        data_file_name = "../create_lms/Documents/data.db"
        self.assertIsNot(print_lms.connectionDataBase(data_file_name),None)

    def test_checkArgv(self):
        if len(sys.argv) <3 :
            sys.argv = [sys.argv[0],None]
        sys.argv[1] = "../create_lms/Documents/data.db"
        self.assertEqual(print_lms.checkArgv(),True)

    def test_print_index(self):
        path = "../create_lms/Documents/data.db"
        connection = print_lms.connectionDataBase(path)
        self.assertEqual(print_lms.printIndex(connection),True)

if __name__ == '__main__':
    unittest.main()
import query_lms
import sys
import unittest


class TestQueryLms(unittest.TestCase):
    def test_check_argv(self):
        if len(sys.argv) <4 :
            sys.argv = [sys.argv[0],None,None,None]
        sys.argv[1] = "../create_lms/Documents/data.db"
        sys.argv[2] = 3
        sys.argv[3] = "one"
        self.assertEqual(query_lms.check_argv(),True)

    def test_connectionDataBase(self):
        data_file_name = "../create_lms/Documents/data.db"
        self.assertIsNot(query_lms.connection_data_base(data_file_name),None)

    def test_smoothing(self):
        self.assertIsNot(query_lms.smoothing(0.5,0.5), 0)

    def test_find_log(self):
        self.assertIsNot(query_lms.find_log(1), 0)


if __name__ == '__main__':
        unittest.main()
import nb_classifier
import sys
import unittest


class TestNbLms(unittest.TestCase):
    def test_check_argv(self):
        if len(sys.argv) < 4 :
            sys.argv = [sys.argv[0],None,None]
        sys.argv[1] = "../trec-397/data/train"
        sys.argv[2] = "../trec-397/data/test"

        self.assertEqual(nb_classifier.check_argv(),True)

    def test_get_accuracy(self):

        spam_result = [1]
        ham_result = [2]
        test_spam_set = []
        test_ham_set = []

        for i in range(9999):
            test_spam_set.append(i)

        for i in range(9999, 9999):
            test_ham_set.append(i)

        spam_result = set(spam_result)
        ham_result = set(ham_result)
        test_spam_set = set(test_spam_set)
        test_ham_set = set(test_ham_set)

        self.assertEqual(nb_classifier.get_accuracy(spam_result,ham_result,test_spam_set,test_ham_set), 1)

    def test_handle_data(self):
        test = nb_classifier.MyHTMLParser()
        self.assertEqual(test.handle_data("test"), True)



if __name__ == '__main__':

        unittest.main()

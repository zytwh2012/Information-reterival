import unittest,os,io,sys,subprocess

class Test_boolean_query(unittest.TestCase):
	

	def test_query1(self):
			result = subprocess.check_output(["python3", "zone_scorer.py", "./zdata.db", "5", "0.3", "Absence"])
			answer =b"57 0.700000\n19 0.300000\n71 0.300000\n126 0.300000\n218 0.300000\n"
			self.assertEqual(result,answer)


	def test_query2(self):
			result = subprocess.check_output(["python3", "zone_scorer.py", "./zdata.db", "4", "0.4", "Malice"])
			answer =b"57 0.600000\n391 0.400000\n0 0.000000\n1 0.000000\n"
			self.assertEqual(result,answer)

	def test_query3(self):
			result = subprocess.check_output(["python3", "zone_scorer.py", "./zdata.db", "2", "0.7", '"Air America"'])
			answer =b"72 1.000000\n0 0.000000\n"
			self.assertEqual(result,answer)
   
							   
if __name__ == '__main__':
	unittest.main()



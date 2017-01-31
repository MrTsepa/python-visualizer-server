import unittest

from evaldontevil import execute_python


class TestExecutePython(unittest.TestCase):
    def test_list_index_out_of_range(self):
        execution = execute_python('a=input()', '5', True)
        print(execution.result)


if __name__ == '__main__':
    unittest.main()

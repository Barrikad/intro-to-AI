import unittest

from bot import *

class TestFrontier(unittest.TestCase):
    
    def test_insert_extract_1(self):
        node = Node(0,{},[],0)
        frontier = Frontier()
        frontier.insert(node)
        self.assertEqual(node,frontier.extract())

if __name__ == '__main__':
    unittest.main()
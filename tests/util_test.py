import unittest

import random

from util import binarySearch

def slowSup(list,element):
    for i in range(len(list)):
        if list[i] >= element:
            return (list[i],i)
    return None

def slowInf(list,element):
    for i in range(len(list)):
        if list[len(list) - i - 1] <= element:
            return (list[len(list) - i - 1],len(list) - i - 1)
    return None

class TestBinarySearch(unittest.TestCase):
    #bad test design but whatever 
    def test_random_search(self):
        for i in range(5):
            count = 0
            list = []
            for _ in range(i * 11):
                count += random.randint(1,10)
                list.append(count)
        
            for i in range(10):
                element = random.randint(-10,count + 10)
                sup = slowSup(list,element)
                inf = slowInf(list,element)
                self.assertEqual(sup,binarySearch(list,element,"sup"))
                self.assertEqual(inf,binarySearch(list,element,"inf"))
                if sup == inf:
                    self.assertEqual(sup,binarySearch(list,element,"eq"))

    def test_find_piece_1(self):
        board = [(4,5,0,"k","1"),(1,5,1,"l","1"),(6,7,2,"t","2"),(1,1,0,"d","2"),(0,8,3,"d","1"),(5,2,1,"l","2")]
        board.sort()
        board = tuple(board)
        coords = (3,4)
        self.assertEqual((4,5,0,"k","1"),binarySearch(board,coords,"sup")[0])
        coords = (6,7)
        self.assertEqual((6,7,2,"t","2"),binarySearch(board,coords,"sup")[0])

    
    def test_find_piece_2(self):
        board = [(6,7,2,"t","2")]
        board.sort()
        board = tuple(board)
        coords = (3,4)
        self.assertEqual((6,7,2,"t","2"),binarySearch(board,coords,"sup")[0])
        coords = (6,7)
        self.assertEqual((6,7,2,"t","2"),binarySearch(board,coords,"sup")[0])
        
    def test_find_piece_3(self):
        board = [(4,5,0,"k","1"),(1,5,1,"l","1"),(6,7,2,"t","2"),(1,1,0,"d","2"),(0,8,3,"d","1")]
        board.sort()
        board = tuple(board)
        coords = (3,4)
        self.assertEqual((4,5,0,"k","1"),binarySearch(board,coords,"sup")[0])
        coords = (0,8)
        self.assertEqual((0,8,3,"d","1"),binarySearch(board,coords,"sup")[0])
        coords = (0,1)
        self.assertEqual((0,8,3,"d","1"),binarySearch(board,coords,"sup")[0])
        
if __name__ == '__main__':
    unittest.main()
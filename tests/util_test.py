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

#bad test design but whatever
class TestBinarySearch(unittest.TestCase):
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

        
if __name__ == '__main__':
    unittest.main()
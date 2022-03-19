import unittest

from bot import *
from frontiers import *
import reach15 as r15

class TestBotDry(unittest.TestCase):
    def test_small_tree(self):
        pass

class TestBotGameReach15(unittest.TestCase):
    #test bot on reach15 game
    
    def test_first_calculation(self):
        bot = r15.makeReach15Bot("p1",Queue())
        bot.calculate()
        self.assertEqual(("p2",2),bot.tree.children[1].state)

    def test_chooses_right_action(self):
        bot = r15.makeReach15Bot("p1",Queue())
        for i in range(10000):
            bot.calculate()
        self.assertEqual(2,bot.bestAction())

class TestBotGameReach15Heap(unittest.TestCase):
    #test bot on reach15 game
    
    def test_first_calculation(self):
        ourTurn = lambda state : state[0] == "p1"
        bot = r15.makeReach15Bot("p1",Heap(ourTurn))
        bot.calculate()
        self.assertEqual(("p2",2),bot.tree.children[1].state)

    def test_chooses_right_action(self):
        ourTurn = lambda state : state[0] == "p1"
        bot = r15.makeReach15Bot("p1",Heap(ourTurn))
        for i in range(10000):
            bot.calculate()
        self.assertEqual(2,bot.bestAction())
        
if __name__ == '__main__':
    unittest.main()
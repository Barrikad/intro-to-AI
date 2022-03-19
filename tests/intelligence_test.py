import unittest

from frontiers import Heap
import laserchess as lc
import lc_bot as lcb

class TestScenarios(unittest.TestCase):
    def test_wins_in_1_by_capture(self):
        king1 = (4,4,0,"k","1")
        king2 = (4,5,0,"k","2")
        board = [king1,king2]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
        for i in range(200):
            bot1.calculate()
        act = bot1.bestAction()
        self.assertEqual("c",lc.actionName(act))
        self.assertEqual((4,4),lc.actionCoords(act))
        self.assertEqual(0,lc.actionMove(act))
        
    def test_wins_in_1_by_laser(self):
        king1 = (0,0,0,"k","1")
        king2 = (4,4,0,"k","2")
        laser = (4,0,3,"l","1")
        board = [king1,king2,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
        for i in range(200):
            bot1.calculate()
        act = bot1.bestAction()
        self.assertEqual("f",lc.actionName(act))
        self.assertEqual(0,act[1])
        
    def test_avoids_laser(self):
        king1 = (0,0,0,"k","2")
        king2 = (4,4,0,"k","1")
        laser = (4,0,3,"l","2")
        board = [king1,king2,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
        for i in range(1000):
            bot1.calculate()
        act = bot1.bestAction()
        self.assertEqual("m",lc.actionName(act))
        self.assertEqual((4,4),lc.actionCoords(act))
        self.assertNotEqual(0,lc.actionMove(act))
        self.assertNotEqual(2,lc.actionMove(act))

        
    def test_shifts_search_center(self):
        pass


import unittest

from frontiers import Heap
import laserchess as lc
import lc_bot as lcb

class TestScenarios(unittest.TestCase):
    def test_mate_in_1_by_capture(self):
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
        
    def test_mate_in_1_by_laser(self):
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

    #test that the bot will center frontier around new state after action
    def test_shifts_search_center(self):
        king1 = (0,0,0,"k","2")
        king2 = (7,4,0,"k","1")
        laser = (4,0,3,"l","2")
        rot1 = ("r",4,0,0)
        rot2 = ("r",4,0,3)
        board = [king1,king2,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
        for i in range(200):
            bot1.calculate()
        state = lc.performAction(state,("m",7,4,0,3))
        bot1.updateState(state)
        for i in range(200):
            bot1.calculate()
        state = lc.performAction(state,rot1)
        bot1.updateState(state)
        for i in range(200):
            bot1.calculate()
        state = lc.performAction(state,("m",6,4,0,3))
        bot1.updateState(state)
        for i in range(200):
            bot1.calculate()
        state = lc.performAction(state,rot2)
        bot1.updateState(state)
        for i in range(200):
            bot1.calculate()
        state = lc.performAction(state,("m",5,4,0,3))
        bot1.updateState(state)
        for i in range(200):
            bot1.calculate()
        state = lc.performAction(state,rot1)
        bot1.updateState(state)
        for i in range(200):
            bot1.calculate()
        for i in range(2000):
            bot1.calculate()
        act = bot1.bestAction()
        self.assertEqual("m",lc.actionName(act))
        self.assertEqual((4,4),lc.actionCoords(act))
        self.assertNotEqual(0,lc.actionMove(act))
        self.assertNotEqual(2,lc.actionMove(act))

    def test_mate_in_2_by_rotation(self):
        king1 = (0,1,0,"k","1")
        king2 = (8,8,0,"k","2")
        laser = (0,1,3,"l","1")
        splitter = (7,1,3,"s","1")
        mirror1 = (8,0,1,"t","1")
        mirror2 = (7,0,0,"t","1")
        board = [king1,king2,laser,splitter,mirror1,mirror2]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
        for i in range(3000): #if you give too much power here it might cause to bot to pick a later mate
            bot1.calculate()
        act = bot1.bestAction()
        self.assertEqual(("r",8,0,3),(act[0],act[1],act[2],act[3]))
    
    def test_mate_in_2_by_capture(self):
        king1 = (0,2,0,"k","1")
        king2 = (0,0,0,"k","2")
        block1 = (1,1,1,"b","1")
        block2 = (2,0,0,"b","1")
        board = [king1,king2,block1,block2]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
        bot2 = lcb.makeLaserChessBot("2",Heap(lambda state : state[0] == "2"),state)
        bot2.calculate()
        bot2.calculate()
        for i in range(4000): #if you give too much power here it might cause the bot to pick a later mate
            bot1.calculate()
        act = bot1.bestAction()
        state = lc.performAction(state,act)
        bot1.updateState(state)
        bot2.updateState(state)
        bot1.calculate()
        bot1.calculate()
        for i in range(1000):
            bot2.calculate()
        act = bot2.bestAction()
        state = lc.performAction(state,act)
        bot1.updateState(state)
        for i in range(1000):
            bot1.calculate()
        act = bot1.bestAction()
        self.assertEqual("c",act[0])

    # def test_mate_in_3_by_sacrifice(self):
    #     king1 = (0,1,0,"k","1")
    #     king2 = (8,8,0,"k","2")
    #     block1 = (8,6,0,"b","1")
    #     block2 = (8,5,0,"b","1")
    #     laser = (0,1,3,"l","1")
    #     splitter = (7,1,3,"s","1")
    #     mirror1 = (8,0,3,"t","1")
    #     mirror2 = (7,0,0,"t","1")
    #     board = [king1,king2,laser,splitter,mirror1,mirror2,block1,block2]
    #     board.sort()
    #     board = tuple(board)
    #     state = ("1",board)
    #     bot1 = lcb.makeLaserChessBot("1",Heap(lambda state : state[0] == "1"),state)
    #     for i in range(20000): #if you give too much power here it might cause to bot to pick a later mate
    #         bot1.calculate()
    #     act = bot1.bestAction()
    #     self.assertEqual("f",act)
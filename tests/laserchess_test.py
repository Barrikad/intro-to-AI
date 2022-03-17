import unittest

from laserchess import beamHits, board, getActions, hitResult, mrPiece, performAction, pieceOrient, rotatePiece, startState


class TestHitResults(unittest.TestCase):
    def test_hit_result_king(self):
        piece = (0,0,0,"k","1")
        hr = hitResult(piece,0)
        self.assertEqual(("c",),hr)
        hr = hitResult(piece,3)
        self.assertEqual(("c",),hr)
        piece = rotatePiece(piece,3)
        hr = hitResult(piece,0)
        self.assertEqual(("c",),hr)
        hr = hitResult(piece,2)
        self.assertEqual(("c",),hr)

    def test_hit_result_block(self):
        piece = (0,0,0,"b","2")
        for i in [3,0,1]:
            hr = hitResult(piece,i)
            self.assertEqual(("c",),hr)
        piece = (0,0,3,"b","2")
        for i in [3,0,2]:
            hr = hitResult(piece,i)
            self.assertEqual(("c",),hr)
        
        for i in range(4):
            piece = rotatePiece(piece,i)
            hr = hitResult(piece,(i - 2) % 4)
            self.assertEqual(("r",i),hr)
    
    def test_hit_result_split(self):
        piece = (0,0,0,"s","1")
        hr = hitResult(piece,3)
        self.assertEqual(("r",0),hr)
        hr = hitResult(piece,1)
        self.assertEqual(("r",0),hr)
        hr = hitResult(piece,2)
        self.assertEqual(("s",1,3),hr)
        hr = hitResult(piece,0)
        self.assertEqual(("c",),hr)
    
    def test_hit_result_diagonal(self):
        piece = (3,6,3,"d","2")
        hr = hitResult(piece,3)
        self.assertEqual(("r",2),hr)
        hr = hitResult(piece,2)
        self.assertEqual(("r",3),hr)
        hr = hitResult(piece,1)
        self.assertEqual(("r",0),hr)
        hr = hitResult(piece,0)
        self.assertEqual(("r",1),hr)
    
    def test_hit_result_triangular(self):
        piece = (3,6,3,"t","2")
        hr = hitResult(piece,3)
        self.assertEqual(("c",),hr)
        hr = hitResult(piece,2)
        self.assertEqual(("r",3),hr)
        hr = hitResult(piece,1)
        self.assertEqual(("r",0),hr)
        hr = hitResult(piece,0)
        self.assertEqual(("c",),hr)


class TestLaserBeam(unittest.TestCase):
    def test_direct_hit_king(self):
        king = (3,6,3,"k","2")
        board = (king,)
        bh = beamHits(board,(3,3),0)
        self.assertEqual([(king,0)],bh)

    def test_1_diagonal_mirror_to_king(self):
        king = (6,2,3,"k","2")
        diagonal = (2,2,0,"d","2")
        board = (diagonal,king)
        bh = beamHits(board,(2,5),2)
        self.assertEqual([(king,1)],bh)

    def test_2_diagonal_mirrors_to_king(self):
        diagonal1 = (2,2,0,"d","2")
        diagonal2 = (6,2,3,"d","2")
        king = (6,5,3,"k","2")
        block1 = (8,8,3,"b","2")
        block2 = (8,6,3,"b","2")
        board = (diagonal1,diagonal2,king,block1,block2)
        bh = beamHits(board,(2,5),2)
        self.assertEqual([(king,2)],bh)

    def test_beam_splitter(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","2")
        king2 = (6,6,3,"k","2")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (4,2,0,"s","1")
        board = [diagonal1,diagonal2,king1,king2,block1,block2,splitter]
        board.sort()
        board = tuple(board)
        bh = beamHits(board,(4,5),2)
        bh.sort()
        expected = [(king2,board.index(king2)),(block2,board.index(block2))]
        expected.sort()
        self.assertEqual(expected,bh)
        

class TestPerformAction(unittest.TestCase):
    def test_rotate_diagonal(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","2")
        king2 = (6,6,3,"k","2")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (4,2,0,"s","1")
        board = [diagonal1,diagonal2,king1,king2,block1,block2,splitter]
        board.sort()
        board = tuple(board)
        state = ("1",board)

        action = ("r",2,2,2)

        eboard = [
            rotatePiece(diagonal1,2),
            diagonal2,
            king1,
            king2,
            block1,
            block2,
            splitter
            ]
        eboard.sort()
        eboard = tuple(eboard)
        expected = ("2",eboard)

        self.assertEqual(expected,performAction(state,action))
        
    def test_move_king(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","2")
        king2 = (6,6,3,"k","2")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (4,2,0,"s","1")
        board = [diagonal1,diagonal2,king1,king2,block1,block2,splitter]
        board.sort()
        board = tuple(board)
        state = ("1",board)

        action = ("m",6,6,1,1)

        eboard = [
            diagonal1,
            diagonal2,
            king1,
            mrPiece(king2,(7,6),1),
            block1,
            block2,
            splitter
            ]
        eboard.sort()
        eboard = tuple(eboard)
        expected = ("2",eboard)

        self.assertEqual(expected,performAction(state,action))

    def test_fire_laser(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","2")
        king2 = (6,6,3,"k","2")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (4,2,0,"s","1")
        laser = (4,5,3,"l","1")
        board = [diagonal1,diagonal2,king1,king2,block1,block2,splitter,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)

        action = ("f",2)

        eboard = [
            diagonal1,
            diagonal2,
            king1,
            block1,
            block2,
            splitter,
            ]
        eboard.sort()
        eboard = tuple(eboard)
        expected = ("2",eboard)

        self.assertEqual(expected,performAction(state,action))

    def test_capture(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","1")
        king2 = (6,6,3,"k","2")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (4,2,0,"s","1")
        laser = (4,5,3,"l","1")
        board = [diagonal1,diagonal2,king1,king2,block1,block2,splitter,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)

        action = ("c",4,7,1,2)

        eboard = [
            diagonal1,
            diagonal2,
            mrPiece(king1,(4,6),1),
            king2,
            block1,
            splitter,
            laser
            ]
        eboard.sort()
        eboard = tuple(eboard)
        expected = ("2",eboard)

        self.assertEqual(expected,performAction(state,action))


class TestGetActions(unittest.TestCase):
    def test_both_kings_present(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","1")
        king2 = (6,6,3,"k","2")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (0,2,0,"s","1")
        laser = (4,5,3,"l","1")
        board = [diagonal1,diagonal2,king1,king2,block1,block2,splitter,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        actual = getActions(state)

        #king can move and capture
        self.assertIn(("c",4,7,0,2),actual)
        self.assertIn(("m",4,7,1,3),actual)
        self.assertIn(("m",4,7,2,0),actual)
        self.assertIn(("m",4,7,3,0),actual)
        self.assertIn(("m",4,7,0,1),actual)
        self.assertIn(("c",4,7,1,2),actual)
        self.assertIn(("m",4,7,2,3),actual)

        #splitter can move
        self.assertIn(("m",0,2,1,1),actual)
        self.assertIn(("m",0,2,0,2),actual)
        self.assertIn(("m",0,2,3,0),actual)

        #laser can rotate and fire
        self.assertIn(("f",0),actual)
        self.assertIn(("f",2),actual)
        self.assertIn(("f",3),actual)

        #splitter can rotate
        self.assertIn(("r",0,2,1),actual)

        #splitter can't rotate to current orientation
        self.assertNotIn(("r",0,2,0),actual)

        #opponent can't move
        self.assertNotIn(("c",4,6,0,2),actual)
        self.assertNotIn(("m",4,6,0,1),actual)

        #laser can't capture
        self.assertNotIn(("c",4,5,0,0),actual)
        self.assertNotIn(("m",4,5,0,0),actual)

        #splitter is blocked by wall
        self.assertNotIn(("m",0,2,0,3),actual)
        self.assertNotIn(("m",0,2,2,3),actual)
        self.assertNotIn(("m",0,2,1,3),actual)

    def test_one_king_missing(self):
        diagonal1 = (2,2,0,"t","2")
        diagonal2 = (6,2,3,"t","2")
        king1 = (4,7,3,"k","1")
        block1 = (2,6,2,"b","2")
        block2 = (4,6,0,"b","2")
        splitter = (0,2,0,"s","1")
        laser = (4,5,3,"l","1")
        board = [diagonal1,diagonal2,king1,block1,block2,splitter,laser]
        board.sort()
        board = tuple(board)
        state = ("1",board)
        actual = getActions(state)

        self.assertEqual([],actual)

    def test_start_position(self):
        state = startState()
        state = performAction(state,("r",4,0,3))
        actual = getActions(state)
        self.assertNotIn(("m",6,7,1,0),actual)
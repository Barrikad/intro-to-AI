import unittest
import random
from frontiers import Heap
from util import MAX_INT

def mockOurTurn(state):
    return state == "1"

class MockNode:
    def __init__(self):
        self.heapIndex = None
        self.value = 0
        self.steps = 0
        self.state = "1"
        self.parents = []
        self.children = {}

class TestMockNodes(unittest.TestCase):
    def setUp(self):
        self.frontier = Heap(mockOurTurn)

    def test_insert_node(self):
        self.assertTrue(self.frontier.empty())
        self.frontier.insert(MockNode())
        self.assertFalse(self.frontier.empty())

    def test_insert_extract_node(self):
        n = MockNode()
        self.frontier.insert(n)
        m = self.frontier.extract()
        self.assertEqual(n,m)
        self.assertTrue(self.frontier.empty())

    def test_sorts_child_value(self):
        p = MockNode()
        c1 = MockNode()
        c2 = MockNode()
        c3 = MockNode()
        c1.parents = [p]
        c2.parents = [p]
        c3.parents = [p]
        p.children = {"a":c1,"b":c2,"c":c3}
        c1.value = 100
        c2.value = 200
        c3.value = 300
        c1.steps = 1
        c2.steps = 1
        c3.steps = 1
        self.frontier.insert(c1)
        self.frontier.insert(c2)
        self.frontier.insert(c3)
        ce = self.frontier.extract()
        self.assertEqual(ce,c3)
    
    def test_sorts_child_steps(self):
        p = MockNode()
        c1 = MockNode()
        c2 = MockNode()
        c3 = MockNode()
        c1.parents = [p]
        c2.parents = [c1]
        c3.parents = [p]
        p.children = {"a":c1,"c":c3}
        c1.children = {"b":c2}
        c1.value = 200
        c2.value = 200
        c3.value = 200
        c1.steps = 1
        c2.steps = 2
        c3.steps = 1
        self.frontier.insert(c2)
        self.frontier.insert(c3)
        ce = self.frontier.extract()
        self.assertEqual(ce,c3)

    def test_bubble(self):
        self.frontier.nodes = [(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode()),(0,MockNode())]
        self.frontier.nodes[10] = (100,MockNode())
        self.frontier.bubbleUp(10)
        self.assertEqual(self.frontier.nodes[0][0],100)
        self.frontier.nodes[10] = (200,MockNode())
        self.frontier.bubbleUp(10)
        self.assertEqual(self.frontier.nodes[0][0],200)
        self.frontier.nodes[10] = (150,MockNode())
        self.frontier.bubbleUp(10)
        self.frontier.nodes[10] = (170,MockNode())
        self.frontier.bubbleUp(10)
        self.frontier.nodes[10] = (140,MockNode())
        self.frontier.bubbleUp(10)
        self.assertEqual(self.frontier.nodes[0][0],200)
        self.frontier.nodes[0] = (0,MockNode())
        self.frontier.bubbleDown(0)
        self.assertEqual(self.frontier.nodes[0][0],170)

    def test_sort(self):
        stateMap = {}
        for i in range(200):
            mnode = MockNode()
            mnode.steps = random.randint(0,1000)
            self.frontier.insert(mnode)
            stateMap[i] = mnode
        for i in range(10):
            self.frontier.extract()
        for i in range(20):
            mnode = MockNode()
            mnode.steps = random.randint(0,1000)
            self.frontier.insert(mnode)
            stateMap[200 + i] = mnode
        for i in range(10):
            self.frontier.extract()

        for i in range(len(self.frontier.nodes)):
            self.assertGreaterEqual(self.frontier.nodes[0][0],self.frontier.nodes[i][0])
        
        for state in stateMap:
            node = stateMap[state]
            node.steps = MAX_INT
            if self.frontier.contains(node):
                self.frontier.reset(node)

        for i in stateMap:
            stateMap[i].steps = random.randint(0,1000)
            if self.frontier.contains(stateMap[i]):
                self.frontier.reevaluate(stateMap[i])

        for i in range(len(self.frontier.nodes)):
            self.assertGreaterEqual(self.frontier.nodes[0][0],self.frontier.nodes[i][0])

    def test_rebase(self):
        p = MockNode()
        c1 = MockNode()
        c2 = MockNode()
        c3 = MockNode()
        c4 = MockNode()
        c1.parents = [p]
        c2.parents = [c1]
        c3.parents = [p]
        c4.parents = [c1]
        p.children = {"a":c1,"c":c3}
        c1.children = {"b":c2,"d":c4}
        c1.value = 200
        c2.value = 300
        c3.value = 200
        c4.value = 200
        c1.steps = 1
        c2.steps = 2
        c3.steps = 1
        c4.steps = 2
        self.frontier.insert(c2)
        self.frontier.insert(c3)
        self.frontier.insert(c4)
        self.assertEqual(self.frontier.extract(),c3)
        self.frontier.insert(c3)
        #rebase to c1
        for c in [c2,c3,c4]:
            self.frontier.reset(c)
        c1.steps = 0
        c2.steps = 1
        c3.steps = 9999
        c4.steps = 1
        for c in [c2,c3,c4]:
            self.frontier.reevaluate(c)
        self.assertEqual(self.frontier.extract(),c2)
        

        
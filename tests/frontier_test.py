import unittest

from frontiers import Heap

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
        c2.value = 200
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
        
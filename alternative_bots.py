import bot 
import frontiers

#heap with lower punishment for steps
class Heap2(frontiers.Heap):
    def evaluate(self, node):
        iv = super().evaluate(node)
        iv += 1000 * node.steps
        return iv
    

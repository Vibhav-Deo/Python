from typing import List
from node import Node

class StackFrontier:
    def __init__(self):
        self.frontier = [];

    def add(self, node:Node):
        self.frontier.append(node);

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier);

    def is_empty(self):
        return len(self.frontier) == 0;

    def remove(self):
        if(self.is_empty()):
            raise Exception("Nothing to remove frontier is empty");
        
        return self.frontier.pop();
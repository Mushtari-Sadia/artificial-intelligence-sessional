import copy
class Node :
    best_child = None
    is_leaf = False
    def __init__(self, agent, move_name):
        self.agent = copy.deepcopy(agent)
        self.move_name = move_name
        self.children = []
        self.value = 0

    def set_board(self,agent):
        self.agent = copy.deepcopy(agent)

    def add_child(self,child):
        self.children.append(child)
        child.set_parent(self)

    def set_height(self,height):
        self.height = height

    def set_parent(self,parent):
        self.parent = parent
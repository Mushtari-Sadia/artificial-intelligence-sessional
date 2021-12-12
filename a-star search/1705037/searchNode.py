import queue
import copy
import heapq

class SearchNode:
    def __init__(self, board, moves, prev, blank):
        self.board = board
        self.moves = moves
        self.prev = prev
        self.blank = blank

    def add_distance(self, distance):
        self.distance = distance

    def __lt__(self, other):
        return self.distance <= other.distance

    def printNode(self):
        for i in self.board:
            for j in i:
                if j==0:
                    print("*", end=" ")
                else:
                    print(j, end=" ")
            print()
        print()





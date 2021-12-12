import heapq
import copy
import time
from searchNode import SearchNode


class AStarSearch:
    def __init__(self, k):
        self.k = k

    def count_inversions(self, flat_matrix):
        k = self.k
        total = 0
        for i in range(k * k):
            for j in range(i + 1, k * k):
                if flat_matrix[i] > flat_matrix[j] != 0 and flat_matrix[i] != 0:
                    # print("inversion : ", flat_matrix[i], flat_matrix[j])
                    total += 1
        # print("total inversions ", total)
        return total

    def check_solvability(self, flat_matrix, blank_position):
        k = self.k
        inversions = self.count_inversions(flat_matrix)
        if k % 2 == 1:
            if inversions % 2 == 1:
                return False
            else:
                return True
        else:
            if (k - blank_position[0]) % 2 == 0 and inversions % 2 == 1:
                return True
            elif (k - blank_position[0]) % 2 == 1 and inversions % 2 == 0:
                return True
            else:
                return False

    def hamming_distance(self, initial_node, goal, n):
        count = 0
        flat_initial = self.flatten(initial_node.board)
        for i in range(n - 1):
            if goal[i] != flat_initial[i]:
                count += 1

        # print("Node :")
        # initial_node.printNode()
        # print("hamming distance is", count)

        return count

    def manhattan_distance(self, node, goal_dict):
        k = self.k
        board = node.board
        total_distance = 0
        for i in range(k):
            for j in range(k):
                if board[i][j] != 0:
                    row_distance = abs(goal_dict[board[i][j]][0] - i)
                    col_distance = abs(goal_dict[board[i][j]][1] - j)
                    total_distance += row_distance + col_distance
        # print("Manhattan distance :",total_distance)
        return total_distance

    def linear_conflict(self, node, goal_dict):
        k = self.k
        linear_conflicts = 0
        potentials = []
        for i in range(k):
            for j in range(k):
                if goal_dict[node.board[i][j]][0] == i and node.board[i][j] != 0:
                    potentials.append(node.board[i][j])
        n = len(potentials)

        for i in range(n):
            for j in range(i, n):
                if potentials[i] > potentials[j]:
                    linear_conflicts += 1
        return linear_conflicts

    def board_to_string(self, node):
        k = self.k
        board = node.board
        str_board = ""
        for i in range(k):
            for j in range(k):
                str_board += str(board[i][j]) + ','
        return str_board

    def get_goal_board_and_dict(self, goal):
        k = self.k
        goal_board = []
        goal_dict = {}
        for i in range(0, k * k, k):
            row = []
            for j in range(k):
                goal_dict[goal[i + j]] = [int(i / k), j]
                row.append(goal[i + j])
            goal_board.append(row)
        return goal_board, goal_dict

    def neighbouring_nodes(self, searchnode):
        k = self.k
        left, right, up, down = (True,) * 4
        if searchnode.blank[0] == 0:
            up = False
        elif searchnode.blank[0] == k - 1:
            down = False
        if searchnode.blank[1] == 0:
            left = False
        elif searchnode.blank[1] == k - 1:
            right = False

        neighbors = []
        if up:
            up_neighbor = self.get_each_neighbor(searchnode, -1, 0)
            neighbors.append(up_neighbor)
        if down:
            down_neighbor = self.get_each_neighbor(searchnode, 1, 0)
            neighbors.append(down_neighbor)
        if left:
            left_neighbor = self.get_each_neighbor(searchnode, 0, -1)
            neighbors.append(left_neighbor)
        if right:
            right_neighbor = self.get_each_neighbor(searchnode, 0, 1)
            neighbors.append(right_neighbor)

        return neighbors

    def get_each_neighbor(self, sn, i_change, j_change):
        searchnode = copy.deepcopy(sn)
        board = searchnode.board
        i = searchnode.blank[0]
        j = searchnode.blank[1]
        t = board[i + i_change][j + j_change]
        board[i + i_change][j + j_change] = board[i][j]
        board[i][j] = t
        neighbor = SearchNode(board, searchnode.moves + 1, sn, [i + i_change, j + j_change])

        return neighbor

    # change loop to O(1) in set
    def isInClosedList(self, node, closed_list):
        str_board = self.board_to_string(node)
        if str_board in closed_list:
            return True
        return False

    def flatten(self, matrix):
        flat_matrix = []
        for row in matrix:
            for item in row:
                flat_matrix.append(item)
        return flat_matrix

    def a_star_search(self, initial_searchnode, goal, heuristic):
        closed_list = set()
        k = self.k
        n = len(goal)
        goal_board, goal_dict = self.get_goal_board_and_dict(goal)

        open_list = [initial_searchnode]
        heapq.heapify(open_list)
        node = initial_searchnode

        while node.board != goal_board:
            node = heapq.heappop(open_list)
            str_board = self.board_to_string(node)
            closed_list.add(str_board)
            # node.printNode()
            neighbors_list = self.neighbouring_nodes(node)
            for neighbor in neighbors_list:
                if not self.isInClosedList(neighbor, closed_list):
                    distance = neighbor.moves
                    if heuristic == "hamming":
                        distance += self.hamming_distance(neighbor, goal, n)
                    elif heuristic == "manhattan":
                        distance += self.manhattan_distance(neighbor, goal_dict)
                    elif heuristic == "linear":
                        distance += self.manhattan_distance(neighbor, goal_dict) + 2 * self.linear_conflict(
                            neighbor, goal_dict)
                    neighbor.add_distance(distance)
                    heapq.heappush(open_list, neighbor)
        print("Expanded nodes =", len(closed_list))
        print("Explored nodes =", len(open_list) + len(closed_list))
        return node

    def printPath(self, node):
        path = []
        print("Optimal cost = ", node.moves)
        while node != None:
            path.append(copy.deepcopy(node))
            node = node.prev
        for i in range(len(path) - 1, -1, -1):
            path[i].printNode()
            if i != 0:
                print("->")


# main
start_time = time.time()

try:
    f = open('input.txt', 'r')
except:
    print("could not open file")
    exit()
k = int(f.readline())
A = AStarSearch(k)

matrix = []
for i in range(k):
    row = f.readline().rstrip('\n')
    row = row.split(" ")
    row2 = []
    for item in row:
        print(item, end=" ")
        if item=='*':
            item = 0
        item = int(item)
        row2.append(item)
    matrix.append(row2)
    print()

matrix_dict = {}
for i in range(k):
    for j in range(k):
        x = matrix[i][j]
        matrix_dict[x] = [i, j]


flat_matrix = []
for row in matrix:
    for item in row:
        flat_matrix.append(item)

if AStarSearch.check_solvability(A, flat_matrix, matrix_dict[0]):
    print("solvability of puzzle = solvable")
else:
    print("solvability of puzzle = unsolvable")
    exit()

initial = flat_matrix.copy()
flat_matrix.remove(0)
flat_matrix.sort()
flat_matrix.append(0)
goal = flat_matrix

initial_searchnode = SearchNode(matrix, 0, None, matrix_dict[0])

print("\nA* search with Hamming distance heuristic:")
hamming_node = AStarSearch.a_star_search(A, initial_searchnode, goal, "hamming")
AStarSearch.printPath(A, hamming_node)

print("\nA* search with Manhattan distance heuristic:")
manhattan_node = AStarSearch.a_star_search(A, initial_searchnode, goal, "manhattan")
AStarSearch.printPath(A, manhattan_node)

print("\nA* search with Manhattan distance heuristic(with linear conflict) :")
linear_node = AStarSearch.a_star_search(A, initial_searchnode, goal, "linear")
AStarSearch.printPath(A, linear_node)

print("--- %s seconds ---" % (time.time() - start_time))

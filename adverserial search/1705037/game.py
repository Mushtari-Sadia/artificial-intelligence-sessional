import math
from agent import Agent
from node import Node
import copy


class Game:
    heuristic = [1, 1]
    moves = ['a', 'b', 'c', 'd', 'e', 'f']

    def generate_game_tree(self, depth, node, original_turn):
        if depth==0 or node.agent.if_one_side_is_empty():
            node.is_leaf = True
            if self.heuristic[node.agent.turn] == '1':
                node.value = node.agent.evaluate_1(original_turn)
            elif self.heuristic[node.agent.turn] == '2':
                node.value = node.agent.evaluate_2(original_turn)
            elif self.heuristic[node.agent.turn] == '3':
                node.value = node.agent.evaluate_3(original_turn)
            elif self.heuristic[node.agent.turn] == '4':
                node.value = node.agent.evaluate_4(original_turn)
            elif self.heuristic[node.agent.turn] == '5':
                node.value = node.agent.evaluate_5(original_turn)
            elif self.heuristic[node.agent.turn] == '6':
                node.value = node.agent.evaluate_6(original_turn)
            return
        agent = copy.deepcopy(node.agent)
        # agent.print_board()
        agent.change_turn()

        for i in self.moves:
            child_agent = copy.deepcopy(agent)
            # print("height:",height,"turn:",child_agent.turn)
            child_agent.generate_board_from_move(i)
            if child_agent.player_bonus_turn:
                child_agent.change_turn()
                child_agent.player_bonus_turn = False
            if not child_agent.zero_ball_bin_chosen:
                child = Node(child_agent, i)
                node.add_child(child)
            else:
                # if height==0:
                #     print("move ",i," has zero bin")
                child_agent.zero_ball_bin_chosen = False
                continue
        # if height == 0:
        #     # print("children of node are ",len(node.children))
        for child in node.children:
            self.generate_game_tree(depth-1, child, original_turn)

    def print_game_tree(self, h, d, root):
        if h == d:
            return
        print("\n\n\n---")
        print("parent :")
        print("value :", root.value)
        root.agent.print_board()
        print("height", h)
        for child in root.children:
            print("value :", child.value)
            child.agent.print_board()
        print("\n\n\n---\n")
        for child in root.children:
            # child.agent.print_board()
            self.print_game_tree(h + 1, d, child)

    def minimax(self, node, turn, alpha, beta):
        # print(turn)
        if node.is_leaf:
            return node.value
        if turn == 1-node.agent.turn:
            best = -math.inf
            for child in node.children:
                val = self.minimax(child, turn, alpha, beta)
                if val > best:
                    best = val
                    node.best_child = child
                alpha = max(alpha, best)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best

        else:
            best = math.inf
            for child in node.children:
                val = self.minimax(child, turn, alpha, beta)
                # val = self.minimax(child, True, alpha, beta)
                if val < best:
                    best = val
                    node.best_child = child
                beta = min(beta, best)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best

    def get_next_move(self, root, max_depth):
        original_turn = root.agent.turn
        node = copy.deepcopy(root)
        #because the last board was opponent's. This wont change turn of root node
        node.agent.change_turn()
        self.generate_game_tree(max_depth, node, original_turn)
        val = self.minimax(node, original_turn, -math.inf, math.inf)
        # print(val)

        return node.best_child.move_name


# win-loss ratio
# if __name__ == "__main__":
#     win_count = [{'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0},
#                  {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}]
#     h0 = input("Please input heuristic for computer 0 : (1-6) :")
#     h1 = input("Please input heuristic for computer 1 : (1-6) :")
#     # f = open("h"+h0+"_h"+h1+"_id.txt", "w")
#     f = open("h"+h0+"_h"+h1+"_d5_mo.csv", 'w')
#
#     # create the csv writer
#     writer = report.writer(f)
#     writer.writerow(["Game","Max depth","Move Order","Winner"])
#     all_games = []
#     for i in range(100):
#         game = Game()
#         game_dict = {}
#         root = Node(Agent(0), 0)
#         game.heuristic[0] = h0
#         game.heuristic[1] = h1
#         random.shuffle(game.moves)
#         depth = (i % 4) + 2
#         game_dict["Max Depth"] = depth
#         game_dict["Move order"] = copy.copy(game.moves)
#         # d=1
#         while True:
#             # choice = game.get_next_move(root, d)
#             choice = game.get_next_move(root, depth)
#             # print("computer", root.agent.turn, "played :", choice)
#             root.agent.generate_board_from_move(choice)
#             # check if chosen bin had 0 balls
#             if root.agent.zero_ball_bin_chosen:
#                 # print("turn:",root.agent.turn)
#                 # print("\nCannot choose bin with 0 balls")
#                 root.agent.zero_ball_bin_chosen = False
#                 continue
#
#             if root.agent.if_one_side_is_empty():
#                 if root.agent.player_bonus_turn:
#                     root.agent.change_turn()
#                 b = root.agent.board
#                 if b[13] > b[6]:
#                     # print("player 1 has won!")
#                     game_dict['winner'] = 1
#                     all_games.append(game_dict)
#                     win_count[1][game.heuristic[1]] += 1
#                 elif b[13] < b[6]:
#                     # print("player 0 has won!")
#                     game_dict['winner'] = 0
#                     all_games.append(game_dict)
#                     win_count[0][game.heuristic[0]] += 1
#                 else:
#                     if root.agent.draw_for_player == 0:
#                         game_dict['winner'] = 1
#                         win_count[1][game.heuristic[1]] += 1
#                     elif root.agent.draw_for_player == 1:
#                         game_dict['winner'] = 0
#                         win_count[0][game.heuristic[0]] += 1
#                     all_games.append(game_dict)
#                 # root.agent.print_board()
#                 row = []
#                 row.append(str(i))
#                 for key in game_dict:
#                     row.append(str(game_dict[key]))
#                 writer.writerow(row)
#                 break
#
#             root.agent.change_turn()
#             if root.agent.player_bonus_turn:
#                 root.agent.change_turn()
#                 # print("Bonus turn! player", root.agent.turn, "gets to go again!")
#                 root.agent.player_bonus_turn = False
#             # if root.agent.turn == 1:
#             #     d = d%5 +1
#             # root.agent.print_board()
#
#     writer.writerow(["Games won","by player 0","with heuristic"+str(h0)+": ",win_count[0][h0]])
#     writer.writerow(["Games won","by player 1","with heuristic"+str(h1)+": ",win_count[1][h1]])
#     j = 1
#     for i in all_games:
#         print(j, end='\t\t\t')
#         for key in i:
#             print(i[key], end='\t\t\t')
#         print()
#         j += 1
#     print("Win count of player 0 with heuristics 1-6 :"+ str(win_count[0])+"\n")
#     print("Win count of player 1 with heuristics 1-6 :"+ str(win_count[1])+"\n")
#     f.close()
#     # print(draw_count)

if __name__ == "__main__":

    c = input("1. computer vs computer\n2. human vs computer")
    if c == '1':
        game = Game()
        root = Node(Agent(0), 0)
        game.heuristic[0] = input("Please input heuristic for computer 0 : (1-6) :")
        game.heuristic[1] = input("Please input heuristic for computer 1 : (1-6) :")
        depth = int(input("Please input depth :"))
        root.agent.print_board()
        while True:
            choice = game.get_next_move(root, depth)
            print("computer", root.agent.turn, "played :", choice)
            root.agent.generate_board_from_move(choice)
            # check if chosen bin had 0 balls
            if root.agent.zero_ball_bin_chosen:
                # print("turn:",root.agent.turn)
                print("\nCannot choose bin with 0 balls")
                root.agent.zero_ball_bin_chosen = False
                continue

            if root.agent.if_one_side_is_empty():
                if root.agent.player_bonus_turn:
                    root.agent.change_turn()
                b = root.agent.board
                if b[13] > b[6]:
                    print("player 1 has won!")
                elif b[13] < b[6]:
                    print("player 0 has won!")
                else:
                    if root.agent.draw_for_player == 0:
                        print("player 1 has won!")
                    else:
                        print("player 0 has won!")
                root.agent.print_board()
                break

            root.agent.change_turn()
            if root.agent.player_bonus_turn:
                root.agent.change_turn()
                print("Bonus turn! player", root.agent.turn, "gets to go again!")
                root.agent.player_bonus_turn = False

            root.agent.print_board()
    elif c == '2':
        game = Game()
        root = Node(Agent(0), 0)
        game.heuristic[1] = input("Please input heuristic for computer : (1-6) :")
        root.agent.print_board()
        while True:
            if root.agent.turn == 0:
                choice = input("Please input the bin number that you want to choose :")
            elif root.agent.turn == 1:
                choice = game.get_next_move(root, 6)
                print("computer played :", choice)
            root.agent.generate_board_from_move(choice)
            # check if chosen bin had 0 balls
            if root.agent.zero_ball_bin_chosen:
                # print("turn:",root.agent.turn)
                print("\nCannot choose bin with 0 balls")
                root.agent.zero_ball_bin_chosen = False
                continue

            if root.agent.if_one_side_is_empty():
                if root.agent.player_bonus_turn:
                    root.agent.change_turn()
                b = root.agent.board
                if b[13] > b[6]:
                    print("computer has won!")
                elif b[13] < b[6]:
                    print("you won!")
                else:
                    if root.agent.draw_for_player == 0 :
                        print("computer has won!")
                    else :
                        print("you won!")
                root.agent.print_board()
                break

            root.agent.change_turn()
            if root.agent.player_bonus_turn:
                root.agent.change_turn()
                print("Bonus turn! player", root.agent.turn, "gets to go again!")
                root.agent.player_bonus_turn = False

            root.agent.print_board()

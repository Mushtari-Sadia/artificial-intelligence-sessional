import numpy as np
import copy
from node import Node


class Agent:
    binDict = {0: {'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1, 'f': 0},
               1: {'a': 7, 'b': 8, 'c': 9, 'd': 10, 'e': 11, 'f': 12}}
    oppositeBinDict = {0: 12, 1: 11, 2: 10, 3: 9, 4: 8, 5: 7,
                       7: 5, 8: 4, 9: 3, 10: 2, 11: 1, 12: 0}
    zero_ball_bin_chosen = False
    player_bonus_turn = False
    bonus_moves_earned = [0, 0]
    captured_stones = [0, 0]
    draw_for_player = -1

    def __init__(self, turn):
        self.turn = turn
        self.board = np.empty([14]).astype(int)
        for i in range(14):
            if i != 6 and i != 13:
                self.board[i] = 4
            else:
                self.board[i] = 0

        # ##TODO test, delete later
        # # for i in range(14):
        # #     self.board[i] = 0
        # # self.board[4] = 1
        # # for i in range(7, 13):
        # #     self.board[i] = i
        # # self.board[13] = 2
        # # self.board[6] = 30
        # ##
        #
        # ##TODO test, delete later
        # for i in range(14):
        #     self.board[i] = 0
        # self.board[11] = 1
        # for i in range(0, 6):
        #     self.board[i] = i
        # self.board[13] = 2
        # self.board[6] = 30
        # ##

    def print_board(self):
        if self.turn == 0:
            print(" " * 5, end="")
            for bin in ['a', 'b', 'c', 'd', 'e', 'f']:
                print(" " + bin + " " * 2, end="")
            print()

        # first border
        for i in range(8):
            print("+---", end="")
        print("+", end="")
        print()
        # first row
        print("|   | ", end="")
        for i in range(5, -1, -1):
            if self.board[i] <= 9:
                print(self.board[i], end=" | ")
            else:
                print(self.board[i], end="| ")
        print("  | ", end="")
        print()

        # middle
        if self.board[6] > 9:
            print("|" + str(self.board[6]), "|", end="")
        else:
            print("|", self.board[6], "|", end="")
        for i in range(5):
            print("---+", end="")
        print("---", end="")
        if self.board[13] > 9:
            print("|" + str(self.board[13]), "|", end="")
        else:
            print("|", self.board[13], "|", end="")
        print()

        # bottom row
        print("|   | ", end="")
        for i in range(7, 13, 1):
            if self.board[i] <= 9:
                print(self.board[i], end=" | ")
            else:
                print(self.board[i], end="| ")
        print("  | ", end="")
        print()

        # last border
        for i in range(8):
            print("+---", end="")
        print("+", end="")
        print()

        if self.turn == 1:
            print(" " * 5, end="")
            for bin in ['a', 'b', 'c', 'd', 'e', 'f']:
                print(" " + bin + " " * 2, end="")
            print()

    def check_if_last_ball_is_in_big_bin(self, chosenBin, nextBin):
        if self.board[chosenBin] == 0:
            if nextBin == 6 and self.turn == 0:
                return True
            if nextBin == 13 and self.turn == 1:
                return True
        return False

    def if_last_ball_is_in_empty_bin(self, chosenBin, nextBin):
        if self.board[chosenBin] == 0:
            if self.board[nextBin] == 1 and self.turn == 0:
                if nextBin >= 0 and nextBin <= 5:  # own bin
                    # get opponent opposite bin balls
                    opponentBin = self.oppositeBinDict[nextBin]
                    if self.board[opponentBin] != 0:
                        self.captured_stones[0] += self.board[opponentBin] + 1
                        self.board[6] += self.board[opponentBin] + 1
                        self.board[opponentBin] -= self.board[opponentBin]
                        self.board[nextBin] = 0
                    return
            if self.board[nextBin] == 1 and self.turn == 1:
                if nextBin >= 7 and nextBin <= 12:  # own bin
                    # get opponent opposite bin balls
                    opponentBin = self.oppositeBinDict[nextBin]
                    if self.board[opponentBin] != 0:
                        self.captured_stones[1] += self.board[opponentBin] + 1
                        self.board[13] += self.board[opponentBin] + 1
                        self.board[opponentBin] -= self.board[opponentBin]
                        self.board[nextBin] = 0
                    return

    def if_one_side_is_empty(self):
        b = copy.copy(self.board)
        sum_0 = 0
        for i in range(6):
            sum_0 += b[i]
            b[i] -= b[i]
        sum_1 = 0
        for i in range(7, 13):
            sum_1 += b[i]
            b[i] -= b[i]
        if sum_0 == 0:
            self.draw_for_player = 0
            b[13] += sum_1
        elif sum_1 == 0:
            self.draw_for_player = 1
            b[6] += sum_0
        else:
            return False
        self.board = b
        return True

    def generate_board_from_move(self, choice):
        chosenBin = self.binDict[self.turn][choice]
        nextBinIterator = 0

        # check if chosen bin had 0 balls
        if self.board[chosenBin] == 0:
            self.zero_ball_bin_chosen = True

        while self.board[chosenBin] != 0:
            nextBinIterator += 1
            nextBin = (chosenBin + nextBinIterator) % 14
            self.board[nextBin] += 1
            self.board[chosenBin] -= 1

            if self.check_if_last_ball_is_in_big_bin(chosenBin, nextBin):
                self.player_bonus_turn = True
                self.bonus_moves_earned[self.turn] += 1

            self.if_last_ball_is_in_empty_bin(chosenBin, nextBin)

    # def evaluate_1(self, turn):
    #     stones_in_my_storage, stones_in_opponents_storage = None, None
    #     if turn == 0:
    #         stones_in_my_storage = self.board[6]
    #         stones_in_opponents_storage = self.board[13]
    #     elif turn == 1:
    #         stones_in_my_storage = self.board[13]
    #         stones_in_opponents_storage = self.board[6]
    #     return stones_in_my_storage - stones_in_opponents_storage
    #
    # def evaluate_2(self, turn):
    #     heuristic = 0
    #     W1, W2 = 2, 3
    #     heuristic += W1 * self.evaluate_1(turn)
    #
    #     stones_in_my_side, stones_in_opponents_side = 0, 0
    #     if turn == 0:
    #         for i in range(0, 6):
    #             stones_in_my_side += self.board[i]
    #             stones_in_opponents_side += self.board[i + 7]
    #     elif turn == 1:
    #         for i in range(0, 6):
    #             stones_in_my_side += self.board[i + 7]
    #             stones_in_opponents_side += self.board[i]
    #     heuristic += W2 * (stones_in_my_side - stones_in_opponents_side)
    #     return heuristic
    #
    # def evaluate_3(self, turn):
    #     W3 = 4
    #     heuristic = self.evaluate_2(turn) + W3 * self.bonus_moves_earned[turn]
    #     return heuristic

    # def evaluate_4(self, turn):
    #     return self.evaluate_3(turn) + self.captured_stones[turn]
    #
    # def evaluate_5(self, turn):
    #     opponents_stone = None
    #     if turn == 1:
    #         opponents_stone = self.board[6]
    #     elif turn == 0:
    #         opponents_stone = self.board[13]
    #     return self.evaluate_4(turn) +(24-opponents_stone)
    #
    # def evaluate_6(self, turn):
    #     sum = 0
    #     if turn == 0:
    #         for i in range(6):
    #             sum += self.board[i]
    #     elif turn == 1:
    #         for i in range(7, 13):
    #             sum += self.board[i]
    #     return self.evaluate_3(turn) + sum

    def evaluate_1(self,turn):
        stones_in_my_storage, stones_in_opponents_storage = None, None
        if self.turn == 0:
            stones_in_my_storage = self.board[6]
            stones_in_opponents_storage = self.board[13]
        elif self.turn == 1:
            stones_in_my_storage = self.board[13]
            stones_in_opponents_storage = self.board[6]
        return stones_in_my_storage - stones_in_opponents_storage

    def evaluate_2(self,turn):
        heuristic = 0
        W1, W2 = 2, 3
        heuristic += W1 * self.evaluate_1(turn)

        stones_in_my_side, stones_in_opponents_side = 0, 0
        if self.turn == 0:
            for i in range(0, 6):
                stones_in_my_side += self.board[i]
                stones_in_opponents_side += self.board[i + 7]
        elif self.turn == 1:
            for i in range(0, 6):
                stones_in_my_side += self.board[i + 7]
                stones_in_opponents_side += self.board[i]
        heuristic += W2 * (stones_in_my_side - stones_in_opponents_side)
        return heuristic

    def evaluate_3(self,turn):
        W3 = 4
        heuristic = self.evaluate_2(turn) + W3 * self.bonus_moves_earned[self.turn]
        return heuristic

    def evaluate_4(self, turn):
        return self.evaluate_1(turn) + self.captured_stones[self.turn]

    def evaluate_5(self, turn):
        opponents_stone = None
        if self.turn == 1:
            opponents_stone = self.board[6]
        elif self.turn == 0:
            opponents_stone = self.board[13]
        return self.evaluate_4(turn) +(24-opponents_stone)

    def evaluate_6(self, turn):
        sum = 0
        if self.turn == 0:
            for i in range(6):
                sum += self.board[i]
        elif self.turn == 1:
            for i in range(7, 13):
                sum += self.board[i]
        return self.evaluate_3(turn) + sum

    def change_turn(self):
        self.turn = 1 - self.turn

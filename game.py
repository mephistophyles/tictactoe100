import numpy as np

class Board(object):

    def __init__(self):
        self.board = np.zeros((3,3))

    def check_winner(self):
        for player in xrange(2,4):
            for i in xrange(3):
                if self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player:
                    return player
                if self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player:
                    return player
            if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
                return player
            if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
                return player
        return 0

    def add_position(self, x, y, player):
        if self.board[x][y] == 0:
            self.board[x][y] = player
            return True
        else:
            print "position already taken, try again"
            return False

    def __str__(self):
        return "{}\n{}\n{}\n".format(str(self.board[0]),str(self.board[1]),str(self.board[2]))


class Player(object):

    def __init__(self, id, balance=100):
        self.id = id
        self.balance = balance

    def check_balance(self, n):
        return n <= self.balance


class Game(object):

    def __init__(self):
        self.players = [Player(1), Player(2)]
        self.board = Board()

    def round(self):
        bet = [None, None, None]
        for player in self.players:
            while bet[player.id] is None:
                attempted_bet = int(raw_input("Player {} please place bet:\t".format(player.id)))
                if player.check_balance(attempted_bet):
                    bet[player.id] = attempted_bet
        if bet[1] > bet[2]:
            winning_bet = bet[1]
            self.players[0].balance -= winning_bet
            self.players[1].balance += winning_bet
            while True:
                position = raw_input("Player 1, please give your desired position:\t").split()
                # TODO parse position validity
                wanted_position = (int(position[0]), int(position[1]))
                if self.board.add_position(wanted_position[0], wanted_position[1], 1):
                    break
        elif bet[2] > bet[1]:
            winning_bet = bet[2]
            self.players[1].balance -= winning_bet
            self.players[0].balance += winning_bet
            while True:
                position = raw_input("Player 2, please give your desired position:\t").split()
                # TODO parse position validity
                wanted_position = (int(position[0]), int(position[1]))
                if self.board.add_position(wanted_position[0], wanted_position[1], 2):
                    break
        else:
            print "bets tied, no winner this round"


    def over(self):
        return self.board.check_winner() != 0

if __name__ == "__main__":
    g = Game()
    while True:
        print "Player 1: {}\t\tPlayer 2: {}".format(g.players[0].balance, g.players[1].balance)
        print g.board
        g.round()
        if g.over():
            print g.board
            print "congratulation Player {}".format(g.board.check_winner())
            break

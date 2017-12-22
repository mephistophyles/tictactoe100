import sys

allowed_gamemodes = [1, 2, 3]
players = [1, 2]


class Board(object):

    def __init__(self):
        self.board = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]

    def check_open(self, positions):
        return self.board[int(positions[0])][int(positions[1])] == " "

    def check_winner(self):
        for player in players:
            # check horizontal and vertical alignments
            for i in range(3):
                if self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player:
                    return player
                if self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player:
                    return player
            # check diagonals
            if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
                return player
            if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
                return player
        return 0

    def add_position(self, x, y, player):
        self.board[x][y] = player

    def __str__(self):
        return "{}\n{}\n{}\n".format(str(self.board[0]), str(self.board[1]), str(self.board[2]))


class Player(object):

    def __init__(self, id, balance=100):
        self.id = id
        self.balance = balance

    def check_balance(self, n):
        return n <= self.balance


class Game(object):

    def __init__(self, mode=1):
        self.players = [Player(1), Player(2)]
        self.board = Board()
        self.mode = mode

    def process_bets(self, winner, loser, bets):
        self.players[winner-1].balance -= bets[winner]
        if self.mode == 2:
            self.players[loser-1].balance -= bets[loser]
        if self.mode == 3:
            self.players[loser-1].balance += bets[winner]
        return

    def round(self):
        bet = [None, None, None]  # hack to keep player id and indexes the same
        for player in self.players:
            while bet[player.id] is None:
                attempted_bet = int(input("Player {} please place bet:\t".format(player.id)))
                if player.check_balance(attempted_bet):
                    bet[player.id] = attempted_bet
                else:
                    print("You can't bet more than your balance.")
        if bet[1] == bet[2]:
            print("bets tied, no winner this round")
            return
        if bet[1] > bet[2]:
            winning_player = 1
            losing_player = 2
        else:
            winning_player = 2
            losing_player = 1
        self.process_bets(winning_player, losing_player, bet)
        valid_pos = False
        while not valid_pos:
            position = input("Player {}, please give your desired position:\t".format(winning_player)).split()
            valid_pos = self.board.check_open(position)
        self.board.add_position(int(position[0]), int(position[1]), winning_player)

    def over(self):
        return self.board.check_winner() != 0

if __name__ == "__main__":
    gamemode_set = False
    try:
        gamemode = sys.argv[1]
        gamemode_set = True
    except Exception:
        pass

    if not gamemode_set:
        print("Choose a game mode:")
        print("1: House takes winning bid, losing bid isn't taken")
        print("2: House takes both bids")
        print("3: Winning bid played to other player (no house)")
        while True:
            gamemode = int(input())
            if gamemode in allowed_gamemodes:
                break

    g = Game(gamemode)
    while True:
        print("Player 1: {}\t\tPlayer 2: {}".format(g.players[0].balance, g.players[1].balance))
        print(g.board)
        g.round()
        if g.over():
            print(g.board)
            print("congratulation Player {}".format(g.board.check_winner()))
            break

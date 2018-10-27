#!/usr/bin/env python
import random
class TicTacToe():
    def __init__(self, board, player, is_max_player, move=None):
        self._board = board
        self._player = player
        self._is_max_player = is_max_player
        self._move = move
        self._flag = 0
        print("--NEXT MOVE--", self._move, self._player, self.is_max_player())

    def children(self):
        player = 'X' if self._player == 'O' else 'O'
        is_max_player = not self._is_max_player

        for r in range(3):
            for c in range(3):
                if self._board[r][c] == '_':
                    board = [[x for x in row] for row in self._board]
                    board[r][c] = self._player
                    yield TicTacToe(board, player, is_max_player, [r, c])

    def payoff(self):
        winner = self._winner()

        if winner is None:
            return 0

        # Either previous min-player won (-1) or previous max-player won (+1).
        return -1 if self._is_max_player else 1

    def payoff_lower(self):
        return -1

    def payoff_upper(self):
        return 1

    def is_terminal(self):
        if self._winner() is not None:
            return True

        for r in range(3):
            for c in range(3):
                if self._board[r][c] == '_':
                    return False

        return True

    def is_max_player(self):
        return self._is_max_player

    def move(self):
        '''Returns the move used to transition to this state.'''
        return self._move

    def _winner(self):
        '''Returns the current winner, if one exists.'''
        board = self._board

        for i in range(3):
            # Check rows...
            if board[i][0] != '_' and \
               board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]

            # Check columns...
            if board[0][i] != '_' and \
               board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]

        # Check diagonals...
        if board[0][0] != '_' and \
           board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]

        if board[2][0] != '_' and \
           board[2][0] == board[1][1] == board[0][2]:
            return board[2][0]

        return None

    def empty_spaces(self):
        count = 0
        for i in range(3):
            count += self._board[i].count('_')
        return count

def alphabeta(state, alpha, beta):
    print("Entered pruning function")
    if state.is_terminal():
        val = state.payoff()
        print("Terminal state", state._board)
        return val

    for next_state in state.children():
        val = alphabeta(next_state, alpha, beta)
        if state.is_max_player():
            if val > alpha:
                alpha = val
            if alpha >= beta:
                return beta
        else:
            if val < beta:
                beta = val
            if beta <= alpha:
                return alpha

    if state.is_max_player():
        return alpha
    else:
        return beta

def determine(state):
    a = -2
    choices = []

    if state.empty_spaces() == 9:
        print('Board Empty')
        return 4

    for nextstate in state.children():
        print("Decision: ", nextstate._board, nextstate._player)
        val = alphabeta(nextstate, -999, 999)
        print("RETURN VAL: ", val, nextstate._move)
        if val > a:
            a = val
            choices = [nextstate._move]
        elif val == a:
            choices.append(nextstate._move)
    print("CHOICES: ", choices)
    return random.choice(choices)


def main():
    # player = input()
    # board = [list(input()) for _ in range(3)]
    player = 'X'
    # board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['_', '_', '_']]
    board = [['_', '_', '_'], ['_', '_', '_'], ['_', 'X', 'O']]
    state = TicTacToe(board, player, True)
    print("--------------------------------------")
    move = determine(state)
    print("OUTPUT MOVE: ", move)
    # print('%d %d' % state.move())



if __name__ == '__main__':
    main()

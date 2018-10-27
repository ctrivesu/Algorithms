#!/usr/bin/env python


class State:
    def children(self):
        '''Returns an iterator over child states.
        NOTE: Valid only if NOT is_terminal().
        '''
        raise NotImplementedError()

    def payoff(self):
        '''Returns the payoff of the state.
        NOTE: Valid only if is_terminal().
        '''
        raise NotImplementedError()

    def payoff_lower(self):
        '''Returns a lower bound on the payoff.'''
        raise NotImplementedError()

    def payoff_upper(self):
        '''Returns an upper bound on the payoff.'''
        raise NotImplementedError()

    def is_terminal(self):
        '''Checks if the state is terminal.'''
        raise NotImplementedError()

    def is_max_player(self):
        '''Checks if the current state is a max player's turn.'''
        raise NotImplementedError()


class TicTacToe(State):
    def __init__(self, board, player, is_max_player, alpha, beta, move=None):
        self._board = board
        self._player = player
        self._is_max_player = is_max_player
        self._move = move
        self.next_move = (-1, -1)
        self._alpha = alpha
        self._beta = beta

        if is_max_player:
            self.best = -9999
        else:
            self.best = 9999

    def children(self):
        player = 'X' if self._player == 'O' else 'O'
        is_max_player = not self._is_max_player
        print(is_max_player)
        t = []
        for r in range(3):
            for c in range(3):
                if self._board[r][c] == '_':
                    board = [[x for x in row] for row in self._board]
                    board[r][c] = self._player
                    t.append(TicTacToe(board, player, is_max_player, self._alpha, self._beta, (r, c)))
        return t

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

        #Check among winner combinations
        if self._winner() is not None:
            print("Winner found")
            return True

        #Check if no empty space left on the board
        for r in range(3):
            for c in range(3):
                if self._board[r][c] == '_':
                    print("sEmpty found")
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



def alpha_beta_minimax(state):
    print("AB VAL: ", state._alpha, state._beta)
    if state.is_terminal():
        #state._move = (-1,-1)
        print(state._board, state._player)
        print("Terminal State Reached", state.move(), "for player ", state._player)
        state.best = state.payoff()
        best_state = state
    else:
        print("---------------------------------------------------------------")
        print("Starting loop for state ", state.move(), " for player : ", state._player)
        chil = state.children()
        if state.is_max_player():  #MAX PLAYER
            for next_state in chil:
                score = alpha_beta_minimax(next_state)
                if (score > state.alpha):
                    state._alpha = score
                if (state._alpha >= state._beta):
                    break
            return state._alpha
        else:
            for next_state in chil:
                score = alpha_beta_minimax(next_state)
                if (score < state._beta):
                    state._beta = score
                if (state._alpha >= state._beta):
                    break
            return state._beta


'''
        for next_state in state.children():
            print("Current - child Player: ", next_state._player)
            score = alpha_beta_minimax(next_state).best
            if state.is_max_player():
                if score > state.best:
                    state.best = score
                    state.next_move = next_state.move()
                    best_state = next_state
                if score > state.alpha:
                    state._alpha = score
                if state._alpha >= state._beta:
                    return -

            else:
                if score < state.best:
                    state.best = score
                    state.next_move = next_state.move()
                    best_state = next_state
        print("endling loop for state ---------- ", state.move(), " for player : ", state._player)
'''
    #return state
    #return 1

def main():
    #player = input()
    #board = [list(input()) for _ in range(3)]
    player = 'O'
    board = [['X', '_', 'X'], ['O', 'X', 'O'], ['_', '_', '_']]
    print(board)
    state = TicTacToe(board, player, True, -9999, 9999)
    print("STATE COMPLETED")
    next_state = alpha_beta_minimax(state)
    #print('%d %d' % state.move())
    print('%d %d' % state.next_move,"for player ", state._player)
    #print('%d %d' % next_state.move(), "for player ", next_state._player)



if __name__ == '__main__':
    main()
"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

import math

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass



def heuristic_1(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 1.4*opp_moves)


def heuristic_2(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    list_center = [(2,2),(2,3),(2,4),(3,2),(3,3),(3,4),(4,2),(4,3),(4,4)]
    list_middle = [(2,1),(3,1),(4,1),(1,2),(1,3),(1,4),(2,5),(3,5),(4,5),(5,2),(5,3),(5,4)]
    list_outside = [(0,0),(0,6),(6,0),(6,6)]

    a=1

    if game.get_player_location(player) in list_center:
        a=1.5
    elif game.get_player_location(player) in list_middle:
        a=1.3
    elif game.get_player_location(player) in list_outside:
        a=1
    else:
        a=1.2

    return float(a*(own_moves - 1.4*opp_moves))


def heuristic_3a(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    blank_spaces = len(game.get_blank_spaces())

    if blank_spaces >= 39:
        a=1
    elif blank_spaces >=20:
        a=2.0
    else:
        a=1.4


    return float(own_moves - a*opp_moves)


def heuristic_3b(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    blank_spaces = len(game.get_blank_spaces())

    if blank_spaces >= 39:
        a=1
    elif blank_spaces >=20:
        a=2.5
    else:
        a=1.4


    return float(own_moves - a*opp_moves)




def heuristic_3c(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    blank_spaces = len(game.get_blank_spaces())

    if blank_spaces >= 39:
        a=1
    elif blank_spaces >=20:
        a=2.8
    else:
        a=1.4


    return float(own_moves - a*opp_moves)




def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    return heuristic_3c(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth: object = 3, score_fn: object = custom_score,
                 iterative: object = True, method: object = 'minimax', timeout: object = 10.) -> object:
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        if len(legal_moves)==0:
            return (-1.0,-1.0)

        best_move = (-1.0,-1.0)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if self.method == 'alphabeta':
                if not self.iterative:
                    best_move = self.alphabeta(game, self.search_depth, maximizing_player=True)[1]
                else:
                    d=1
                    best_score = float("-inf")
                    while True:
                        v,m = self.alphabeta(game, d,  alpha=float("-inf"), beta=float("inf"), maximizing_player=True)
                        if v>best_score:
                            best_score = v
                            best_move = m
                        d += 1

            if self.method == 'minimax':
                if not self.iterative:
                    best_move = self.minimax(game, self.search_depth, maximizing_player=True)[1]
                else:
                    d=1
                    best_score = float("-inf")
                    while True :
                        v,m = self.minimax(game, d, maximizing_player=True)
                        if v>best_score:
                            best_score = v
                            best_move = m
                        d += 1
            pass

        except Timeout:
            return best_move # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!

        legal_moves = game.get_legal_moves()
        if len(legal_moves)==0:
            return self.score(game, self), (-1.0,-1.0)
        elif depth==0:
            return self.score(game, self), (-1.0,-1.0)


        if maximizing_player:
            result = [-math.inf,(-1.0,-1.0)]
            for m in legal_moves:
                v = self.minimax(game.forecast_move(m), depth-1, maximizing_player=False)
                if v[0]>result[0]:
                    result=[v[0],m]
            return result[0],result[1]

        if not maximizing_player:
            result = [math.inf, (-1.0, -1.0)]
            for m in legal_moves:
                v = self.minimax(game.forecast_move(m), depth-1, maximizing_player=True)
                if v[0]<result[0]:
                    result=[v[0],m]
            return result[0],result[1]



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!

        legal_moves = game.get_legal_moves()
        if len(legal_moves)==0:
            return self.score(game, self), (-1.0,-1.0)
        elif depth==0:
            return self.score(game, self), (-1.0,-1.0)


        if maximizing_player:
            result = [-math.inf,(-1.0,-1.0)]
            for m in legal_moves:
                v = self.alphabeta(game.forecast_move(m), depth-1, alpha, beta, maximizing_player=False)
                if v[0] > result[0]:
                    result = [v[0],m]
                if v[0] >= beta:
                    return result[0],result[1]
                alpha = max(alpha, v[0])
            return result[0],result[1]

        if not maximizing_player:
            result = [math.inf, (-1.0, -1.0)]
            for m in legal_moves:
                v = self.alphabeta(game.forecast_move(m), depth-1, alpha, beta, maximizing_player=True)
                if v[0] < result[0]:
                    result = [v[0], m]
                if v[0] <= alpha:
                    return result[0], result[1]
                beta = min(beta, v[0])
            return result[0], result[1]
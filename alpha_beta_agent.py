import math
import agent


###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)

        self.max_depth = max_depth
        self.me = None
        self.you = None

    # ISAAC: we should add a heuristic here that gives/removes value states
    #        that have more in a row
    def heuristic(self, brd):
        """Assign a heuristic value to the current state of the board"""

        if "defensive": 
            # This simply causes the ai to play defensively:
            #   if the AI can win, play that move
            #   else if the other player is about to win, block it
            if brd.get_outcome() == self.me and brd.player == self.you:
                return math.inf

            if brd.get_outcome() == self.you and brd.player == self.me:
                return -math.inf

            value = 0
            for x in range(0, brd.w):
                for y in range(0, brd.h):
                    if brd.board[y][x] != 0:
                        if brd.is_any_line_at(x, y):
                            if brd.board[y][x] == self.you:
                                value -= 10
                            elif brd.board[y][x] == self.me:
                                value += 1
                            else:
                                value += 0
        return value

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        self.me = brd.player
        self.you = (not (brd.player-1))+1
        alpha = -math.inf
        beta = math.inf
        ((b,c),v) = self.max(brd, self.max_depth, alpha, beta)
        return c
    
    def max(self, brd, n, alpha, beta):
        if n == 0:
            return ((brd, None), self.heuristic(brd))
        
        best_value = -math.inf
        best_brd = None
        best_col = None

        successors = self.get_successors(brd)
        for (board, column) in successors:
            ((b, c), value) = self.min(board, n-1, alpha, beta)
            if value > best_value:
                best_brd = board
                best_col = column
                best_value = value
            if best_value >= beta:
                return ((best_brd, best_col), best_value)
            alpha = max(alpha, best_value)
        return ((best_brd, best_col), best_value)

    def min(self, brd, n, alpha, beta):
        if n == 0:
            return ((brd, None), self.heuristic(brd))
        
        best_value = math.inf
        best_brd = None
        best_col = None

        successors = self.get_successors(brd)
        for (board, column) in successors:
            ((b, c), value) = self.max(board, n-1, alpha, beta)
            if value < best_value:
                best_brd = board
                best_col = column
                best_value = value
            if best_value <= alpha:
                return ((best_brd, best_col), best_value)
            beta = min(beta, best_value)
        return ((best_brd, best_col), best_value)

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ
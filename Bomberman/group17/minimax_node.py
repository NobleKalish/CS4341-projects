class MinimaxNode(object):
    # Class constructor.
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int]         col: column where last token was added
    # PARAM [int]         evaluation: The evaluation score.
    def __init__(self, world, move, evaluation):
        # Board used in node
        self.world = world
        # column where last token was added
        self.move = move
        # evaluation value given by the alphaBetaAgent evaluation function
        self.evaluation = evaluation

from math import sqrt, log
import copy

class Node:
    def __init__(self, state, piece, column=None, parent=None):
        self.column = column
        self.parent = parent
        self.player_piece = piece
        self.untried_moves = state.coups_possibles()
        self.children = list()
        self.wins = 0
        self.visits = 0

    def uct_select_child(self):
        best, best_child = -1, None
        c = sqrt(2)
        for child in self.children:
            score = child.wins / child.visits + c * sqrt(2*log(self.visits) / child.visits)
            if score > best:
                best_child = child
                best = score
        return best_child

    def add_child(self, col, state):
        node = Node(copy.deepcopy(state), self.get_next_piece(self.player_piece), column=col, parent=self)
        self.untried_moves.remove(col)
        self.children.append(node)
        return node

    def update(self, result):
        self.visits += 1
        self.wins += result

    def get_next_piece(self, piece):
        if piece == 'X':
            return '0'
        return 'X'
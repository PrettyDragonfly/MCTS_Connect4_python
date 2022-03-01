import random
from node import Node
import copy
import time

class MCTS():
    def __init__(self, state, piece, timer, last_node=None):
        if last_node is not None:
            self.root = last_node
        else:
            self.root = Node(copy.deepcopy(state), piece)
        self.original_state = state
        self.timer = timer

    def get_move(self):
        best_ratio = -1
        best_column = None
        node = self.root
        end_time = time.time() + self.timer
        ite = 0
        while time.time() < end_time:
            node = self.root
            state = copy.deepcopy(self.original_state)
            node = self.select(node, state)
            node = self.expand(node, state)
            state = self.rollout(state)
            self.backpropagate(node, state)
            ite += 1
        print("Nombre d'itérations: {}".format(ite))
        for i in iter(self.root.children):
            if (i.wins / i.visits) * 100 > best_ratio:
                best_ratio = (i.wins / i.visits) * 100
                best_column = i.column
        if best_column is not None:
            print("La colonne [{}] a le meilleur ratio: [{:.2f}%]".format(best_column+1, best_ratio))

        return node, best_column

    def select(self, node, state):
        while len(node.untried_moves) == 0 and len(node.children) !=0:
            node = node.uct_select_child()
            state.jouer_coup(node.player_piece, node.column)
        return node

    def expand(self, node, state):
        if len(node.untried_moves) != 0:
            col = random.choice(node.untried_moves)
            state.jouer_coup(node.player_piece, col)
            node = node.add_child(col, state)
        return node

    def rollout(self, state):
        while len(state.coups_possibles()) != 0:
            col = random.choice(state.coups_possibles())
            piece = self.get_next_piece(state.plateau[state.last_row][state.last_column])
            state.jouer_coup(piece, col)
        return state

    def backpropagate(self, node, state):
        while node is not None:
            node.update(state.get_result(node.player_piece))
            node = node.parent

    def get_next_piece(self, piece):
        if piece == 'X':
            return 'O'
        return 'X'
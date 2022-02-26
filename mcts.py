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
        while node.parent is not None:
            node = node.parent
        print('Estimation de la probabilité de victoire: %.2f%%' % (100 * node.wins / node.visits))
        return self.root, sorted(self.root.children, key=lambda c: c.wins/c.visits)[-1].column

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
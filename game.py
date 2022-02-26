from board import Board
from node import Node
from mcts import MCTS
import copy

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = None
        self.advance_turn()

    def play(self):
        self.current_player = int(input("Qui commence? (0 pour l'ordinateur, 1 pour l'humain)"))
        if self.current_player == 0:
            node = Node(self.board, 'O')
            print("C'est l'ordinateur qui commence")
        else:
            node = Node(self.board, 'X')
            print("C'est l'humain qui commence")
        self.board.affiche_jeu()

        while True:
            if self.current_player == 1:
                column = self.get_move()

                while not self.board.jouer_coup('X', column):
                    print("Colonne invalide")
                    column = self.get_move()
            else:
                print("L'ordinateur réfléchi")
                node, column = MCTS(copy.deepcopy(self.board), '0', 10, last_node=node).get_move()
                self.board.jouer_coup('O', column)

            self.board.affiche_jeu()
            node = self.navigate_to_node_for_move(node, column, self.board)
            if self.board.is_winner():
                if self.current_player == 0:
                    print("L'ordinateur a gagné!")
                    break
                else:
                    print("L'humain a gagné!")
                    break

            if self.board.is_tie_game():
                print("Match nul...")
                break

            self.advance_turn()

    def get_move(self):
        col = input("Quelle colonne?")
        return int(col)-1

    def advance_turn(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    def navigate_to_node_for_move(self, node, column, board):
        for child in node.children:
            if child.column == column:
                return child
        return Node(board, node.player_piece)
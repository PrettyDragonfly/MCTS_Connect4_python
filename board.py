import numpy as np
import copy

class Board():
    def __init__(self):
        self.last_row = 0
        self.last_column = 0
        self.plateau = np.full((6, 7), None)

    def affiche_jeu(self):
        print('  -----------------------------')
        for i in range(6):
            print('  | ', end='')
            for j in range(7):
                if self.plateau[i][j] is None:
                    print(' ' + ' | ', end='')
                else:
                    print(self.plateau[i][j], end='')
                    print(' | ', end='')
            if i != 5:
                print('\n  |---+---+---+---+---+---+---|')
        print('\n---------------------------------')
        print('    1   2   3   4   5   6   7')
        print('---------------------------------')

    def jouer_coup(self, piece, column):
        if self.plateau[0][column] is not None:
            # La colonne est pleine
            return False
        # On cherche la ligne la plus basse
        line = 5
        while self.plateau[line][column] is not None:
            line -= 1
        self.plateau[line][column] = piece
        self.last_row = line
        self.last_column = column
        return True

    def get_result(self, piece):
        if self.plateau[self.last_row][self.last_column] == piece:
            return 1.0
        else:
            return 0.0

    def is_winner(self):
        row = self.last_row
        column = self.last_column
        return self.vertical_winner(column) or self.horizontal_winner(row) or self.diagonal_winner(row, column)

    def is_tie_game(self):
        res = True
        # je vérifie si le plateau est plein
        for i in range(7):
            if self.plateau[0][i] is None:
                return False
        return res

    def coups_possibles(self):
        if self.is_winner():
            return []
        return [i for i in range(7) if self.plateau[0][i] is None]

    def vertical_winner(self, column):
        for row in range(len(self.plateau) - 3):
            if self.plateau[row][column] == 'X' and self.plateau[row + 1][column] == 'X' and self.plateau[row + 2][column] == 'X' \
                    and self.plateau[row + 3][column] == 'X':
                return True
            if self.plateau[row][column] == 'O' and self.plateau[row + 1][column] == 'O' and self.plateau[row + 2][column] == 'O' \
                    and self.plateau[row + 3][column] == 'O':
                return True
        return False

    def horizontal_winner(self, row):
        for col in range(len(self.plateau[row]) - 3):
            if self.plateau[row][col] == 'X' and self.plateau[row][col + 1] == 'X' and self.plateau[row][col + 2] == 'X' \
                    and self.plateau[row][col + 3] == 'X':
                return True
            if self.plateau[row][col] == 'O' and self.plateau[row][col + 1] == 'O' and self.plateau[row][col + 2] == 'O' \
                    and self.plateau[row][col + 3] == 'O':
                return True
        return False

    def diagonal_winner(self, row, column):
        return self.check_diago_haut_droite(row, column) or self.check_diago_haut_gauche(row, column)

    def check_diago_haut_gauche(self, row, column):
        tmp_row, tmp_col = row, column
        run = []
        while tmp_row < 5 and tmp_col < 6:
            tmp_row += 1
            tmp_col += 1
        while tmp_col >= 0 and tmp_row >= 0:
            run.append(self.plateau[tmp_row][tmp_col])
            tmp_row -= 1
            tmp_col -= 1
        return self.check_rangee(run)

    def check_diago_haut_droite(self, row, column):
        tmp_row, tmp_col = row, column
        run = []
        while tmp_col < 7 - 1 and tmp_row > 0:
            tmp_col += 1
            tmp_row -= 1

        while tmp_col >= 0 and tmp_row < 6:
            run.append(self.plateau[tmp_row][tmp_col])
            tmp_row += 1
            tmp_col -= 1
        return self.check_rangee(run)

    def check_rangee(self, run):
        if len(run) < 4:
            return False

        for i in range(len(run) - 3):
            if run[i] == 'X' and run[i + 1] == 'X' and run[i + 2] == 'X' and run[i + 3] == 'X':
                return True
            if run[i] == 'O' and run[i + 1] == 'O' and run[i + 2] == 'O' and run[i + 3] == 'O':
                return True
        return False

    def check_coup_gagnant(self, current_player):
        # Pour chaque colonne on vérifie la victoire
        tableau_test = copy.deepcopy(self)
        if current_player == 0:
            piece_test = 'O'
        else:
            piece_test = 'X'
        for col in range(7):
            # Si la colonne n'est pas remplie alors on teste la potentielle victoire
            if tableau_test.jouer_coup(piece_test, col):
                if tableau_test.is_winner():
                    print("L'ordinateur gagne s'il joue en colonne [{}]".format(col))
                    return col
                else:
                    # Recharge le tableau pour tester la colonne suivante:
                    tableau_test = copy.deepcopy(self)

        tableau_test = copy.deepcopy(self)
        # Si la colonne n'est pas remplie alors on teste la potentielle défaite si l'adversaire le joue le coup suivant
        if piece_test == 'X':
            piece_test = 'O'
        else:
            piece_test = 'X'
        for col in range(7):
            if tableau_test.jouer_coup(piece_test, col):
                if tableau_test.is_winner():
                    print("Le joueur a une possibilité de gagner qu'il faut contrer en colonne [{}]".format(col))
                    return col
                else:
                    # Recharge le tableau pour tester la colonne suivante:
                    tableau_test = copy.deepcopy(self)

        # Si aucun coup vainqueur ou perdant absolu alors on ne retourne rien
        return None
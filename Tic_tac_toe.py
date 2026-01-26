import math
import copy
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('normal', 20), height=2, width=5,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row, col):
        if self.buttons[row][col]['text'] == '' and not self.is_game_over():
            self.buttons[row][col]['text'] = self.current_player
            if self.is_winner(self.current_player):
                self.display_winner()
            elif self.is_board_full():
                self.display_tie()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O' and not self.is_game_over():
                    self.ai_make_move()

    def ai_make_move(self):
        move = self.find_best_move()
        self.buttons[move[0]][move[1]]['text'] = self.current_player
        if self.is_winner(self.current_player):
            self.display_winner()
        elif self.is_board_full():
            self.display_tie()
        else:
            self.current_player = 'X'

    def is_winner(self, player):
        for i in range(3):
            if all(self.buttons[i][j]['text'] == player for j in range(3)) or all(
                    self.buttons[j][i]['text'] == player for j in range(3)):
                return True
        if all(self.buttons[i][i]['text'] == player for i in range(3)) or all(
                self.buttons[i][2 - i]['text'] == player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(self.buttons[i][j]['text'] != '' for i in range(3) for j in range(3))

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_board_full()

    def find_best_move(self):
        best_val = -math.inf
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == '':
                    self.buttons[i][j]['text'] = 'O'
                    move_val = self.minimax(0, False, -math.inf, math.inf)
                    self.buttons[i][j]['text'] = ''
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (i, j)

        return best_move

    def minimax(self, depth, maximizing_player, alpha, beta):
        if self.is_winner('X'):
            return -1
        elif self.is_winner('O'):
            return 1
        elif self.is_board_full():
            return 0

        if maximizing_player:
            max_eval = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j]['text'] = 'O'
                        eval = self.minimax(depth + 1, False, alpha, beta)
                        self.buttons[i][j]['text'] = ''
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = math.inf
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j]['text'] = 'X'
                        eval = self.minimax(depth + 1, True, alpha, beta)
                        self.buttons[i][j]['text'] = ''
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def display_winner(self):
        self.winner = self.current_player
        messagebox.showinfo("Game Over", f"{self.winner} wins!")
        self.root.quit()

    def display_tie(self):
        self.winner = 'Tie'
        messagebox.showinfo("Game Over", "It's a tie!")
        self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()

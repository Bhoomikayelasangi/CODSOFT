import tkinter as tk
from tkinter import messagebox
import math

# Minimax algorithm to determine the best move
def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    winner = check_winner(board)
    if winner == "O":
        return 10 - depth
    elif winner == "X":
        return depth - 10
    elif is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Find the best move for the AI
def best_move(board):
    best_val = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                move_val = minimax(board, 0, False)
                board[i][j] = " "
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# Check for a win
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

# Check if the board is full
def is_full(board):
    return all(cell != " " for row in board for cell in row)

# GUI Application
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_ui()
        self.human = "X"
        self.ai = "O"

    def create_ui(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text=" ", font=("Arial", 24), height=2, width=5, 
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_click(self, i, j):
        if self.board[i][j] == " " and not check_winner(self.board):
            self.board[i][j] = self.human
            self.buttons[i][j].config(text=self.human)
            winner = check_winner(self.board)
            if winner or is_full(self.board):
                self.end_game(winner)
                return
            self.ai_turn()

    def ai_turn(self):
        move = best_move(self.board)
        if move != (-1, -1):
            self.board[move[0]][move[1]] = self.ai
            self.buttons[move[0]][move[1]].config(text=self.ai)
        winner = check_winner(self.board)
        if winner or is_full(self.board):
            self.end_game(winner)

    def end_game(self, winner):
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.reset_board()

    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

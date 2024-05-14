import tkinter as tk
from tkinter import messagebox


Me = 'x'
Com = 'o'

board = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]


# Print the board
def print_board(board):
    for row in board:
        print(' '.join(row))
    print()
    

# Check if there are any remaining possible moves on the board
def is_moves_left(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == '_':
                return True
    return False



# Check for a win for a specific player
def check_win(board, player):
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] == player) or (board[0][i] == board[1][i] == board[2][i] == player):
            return True

    if (board[0][0] == board[1][1] == board[2][2] == player) or (board[0][2] == board[1][1] == board[2][0] == player):
        return True

    return False

# Evaluate the current state of the board for the computrer


def evaluate(board):
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]):
            if board[i][0] == Com:
                return 10
            elif board[i][0] == Me:
                return -10

        if (board[0][i] == board[1][i] == board[2][i]):
            if board[0][i] == Com:
                return 10
            elif board[0][i] == Me:
                return -10

    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]):
        if board[1][1] == Com:
            return 10
        elif board[1][1] == Me:
            return -10


# Minimax algorithm to choose the best possible move


def minimax(board, depth, is_max):
    score = evaluate(board)

    if score == 10 or score == -10:
        return score

    if not is_moves_left(board):
        return 0

    if is_max:
        best = -1000

        for row in range(3):
            for col in range(3):
                if board[row][col] == '_':
                    board[row][col] = Com
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[row][col] = '_'
        return best
    else:
        best = 1000

        for row in range(3):
            for col in range(3):
                if board[row][col] == '_':
                    board[row][col] = Me
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[row][col] = '_'
        return best

# Find the best move using the Minimax algorithm


def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)

    for row in range(3):
        for col in range(3):
            if board[row][col] == '_':
                board[row][col] = Com
                move_val = minimax(board, 0, False)
                board[row][col] = '_'

                if move_val > best_val:
                    best_move = (row, col)
                    best_val = move_val

    return best_move

# Start the game


def play_game():
    current_player = Me
    print("Tic-Tac-Toe Game")
    print_board(board)

    while is_moves_left(board):
        if current_player == Me:
            row = int(input("Choose row (0, 1, 2): "))
            col = int(input("Choose column (0, 1, 2): "))

            if 0 <= row <= 2 and 0 <= col <= 2:
                if board[row][col] == '_':
                    board[row][col] = Me
                    print_board(board)
                    if check_win(board, Me):
                        print(f"Player '{Me}' wins!")
                        return
                    current_player = Com
                else:
                    print("Invalid move. Please choose another move.")

        else:
            best_move = find_best_move(board)
            print(
                f"Player '{Com}' makes move: ROW: {best_move[0]}, COL: {best_move[1]}")
            board[best_move[0]][best_move[1]] = Com
            print_board(board)
            if check_win(board, Com):
                print(f"Player '{Com}' wins!")
                return
            current_player = Me

    print("It's a tie!")# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe Game")

# Create labels for each cell in the GUI
labels = [[None, None, None] for _ in range(3)]

# Function to handle button click events


def button_click(row, col):
    if board[row][col] == '_':
        labels[row][col].config(text=Me)
        board[row][col] = Me
        if check_win(board, Me):
            messagebox.showinfo("Game Over", f"Player '{Me}' wins!")
            root.destroy()
        elif not is_moves_left(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            root.destroy()
        else:
            play_com_move()

# Function to handle the computer's move


def play_com_move():
    best_move = find_best_move(board)
    board[best_move[0]][best_move[1]] = Com
    labels[best_move[0]][best_move[1]].config(text=Com)
    if check_win(board, Com):
        messagebox.showinfo("Game Over", f"Player '{Com}' wins!
from tkinter import *

# Initialize the game window
root = Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#333333")

# Game Variables
board = [" " for _ in range(9)]
player = "X"
ai = "O"
game_over = False

# Create the game board UI
buttons = []

def create_buttons():
    for index in range(9):
        button = Button(board_frame, text=" ", font=("Arial", 20), width=5, height=2, 
                        bg="#f0f0f0", fg="#333333", 
                        command=lambda idx=index: player_move(idx))
        button.grid(row=index//3, column=index%3, padx=5, pady=5)
        buttons.append(button)

def reset_board():
    global board, game_over
    board = [" " for _ in range(9)]
    game_over = False
    for button in buttons:
        button.config(text=" ", bg="#f0f0f0")

# Check for win or draw
def check_win(b, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if b[condition[0]] == b[condition[1]] == b[condition[2]] == player:
            for idx in condition:
                buttons[idx].config(bg="#ffcccb")
            return True
    return False

def check_draw(b):
    return " " not in b

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win(board, ai):
        return 1
    elif check_win(board, player):
        return -1
    elif check_draw(board):
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = ai
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = " "
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = " "
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move():
    best_value = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            move_value = minimax(board, 0, False, -float('inf'), float('inf'))
            board[i] = " "
            if move_value > best_value:
                best_value = move_value
                move = i
    return move

# Handle player and AI moves
def player_move(index):
    global game_over
    if board[index] == " " and not game_over:
        board[index] = player
        buttons[index].config(text=player, fg="#007bff")
        if check_win(board, player):
            game_over = True
            display_result("You Win!")
        elif check_draw(board):
            game_over = True
            display_result("Draw!")
        else:
            ai_move()

def ai_move():
    global game_over
    index = best_move()
    board[index] = ai
    buttons[index].config(text=ai, fg="#ff5733")
    if check_win(board, ai):
        game_over = True
        display_result("AI Wins!")
    elif check_draw(board):
        game_over = True
        display_result("Draw!")

# Display the game result
def display_result(result):
    result_label.config(text=result)
    root.after(2000, reset_board)

# UI Elements for displaying result and reset button
board_frame = Frame(root, bg="#333333")
board_frame.pack(pady=20)

create_buttons()

result_label = Label(root, text="", font=("Arial", 20), bg="#333333", fg="#ffffff")
result_label.pack(pady=10)

reset_button = Button(root, text="Restart Game", font=("Arial", 15), bg="#007bff", fg="#ffffff", command=reset_board)
reset_button.pack(pady=10)

# Start the game
root.mainloop()

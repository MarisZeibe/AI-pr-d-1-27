import tkinter as tk
from tkinter import messagebox, simpledialog
from enum import Enum

class Algorithm(Enum):
    MINIMAX = 1
    ALPHA_BETA = 2

class Player(Enum):
    Lietotajs = 1
    Dators = 2

class State:
    def __init__(self, number, points, bank, level):
        self.number = number
        self.points = points
        self.bank = bank
        self.level = level
        self.children = []

def choose_starting_player():
    choice = simpledialog.askstring("Player Choice", "Choose starting player: (Lietotajs or Dators)")
    if choice.lower() == "lietotajs":
        return Player.Lietotajs
    elif choice.lower() == "dators":
        return Player.Dators
    else:
        messagebox.showerror("Error", "Invalid choice. Please choose 'Lietotajs' or 'Dators'.")
        return choose_starting_player()

def choose_algorithm():
    choice = simpledialog.askstring("Algorithm Choice", "Choose algorithm: (Minimaksa algoritms or Alfa-beta algoritms)")
    if choice.lower() == "minimaksa algoritms":
        return Algorithm.MINIMAX
    elif choice.lower() == "alfa-beta algoritms":
        return Algorithm.ALPHA_BETA
    else:
        messagebox.showerror("Error", "Invalid choice. Please choose 'Minimaksa algoritms' or 'Alfa-beta algoritms'.")
        return choose_algorithm()

def int_input(message: str, number_range: range) -> int:
    while True:
        try:
            input_number = int(simpledialog.askstring("Input", message))
            if input_number in number_range:
                return input_number
            else:
                messagebox.showerror("Error", "Invalid input. Please enter a number between 20 and 30.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

def generate_tree(index: int):
    global gameTree
    if gameTree[index].number > 3000:
        return
    for n in range(3, 6):
        new_state = State(
            gameTree[index].number * n,
            gameTree[index].points + (1 if gameTree[index].number % 2 == 0 else -1),
            gameTree[index].bank + (1 if gameTree[index].number % 5 == 0 else 0),
            gameTree[index].level + 1
        )
        if new_state.number > 3000:
            new_state.points += bank * (-1 if new_state.points % 2 == 0 else 1)
        if new_state not in gameTree:
            gameTree.append(new_state)
            gameTree[index].children.append(len(gameTree) - 1)
            generate_tree(len(gameTree) - 1)
        else:
            gameTree[index].children.append(gameTree.index(new_state))

def start_game():
    global points, bank, number, gameTree
    points = 0
    bank = 0
    number = int_input('Enter a number from 20 to 30: ', range(20, 31))

    player = choose_starting_player()
    algorithm = choose_algorithm()

    gameTree = [State(number, points, bank, 0)]
    generate_tree(0)

    while number < 3000:
        if player == Player.Lietotajs:
            multiplier = int_input('Enter a multiplier (3, 4, or 5): ', range(3, 6))
            # Update moves log
            moves_log.insert(tk.END, f"Lietotajs: {multiplier}\n")
            number *= multiplier
        else:
            if algorithm == Algorithm.MINIMAX:
                available_moves = [3, 4, 5]
                best_value = float('-inf')
                best_move = None
                for move in available_moves:
                    new_number = number * move
                    new_points = points + (1 if new_number % 2 == 0 else -1)
                    new_bank = bank + (1 if new_number % 5 == 0 else 0)
                    new_level = gameTree[0].level + 1
                    child_state = State(new_number, new_points, new_bank, new_level)
                    value = minimax_search(child_state, player)
                    if value > best_value:
                        best_value = value
                        best_move = move

                number *= best_move
                # Update moves log
                moves_log.insert(tk.END, f"Dators: {best_move}\n")
            elif algorithm == Algorithm.ALPHA_BETA:
                available_moves = [3, 4, 5]
                best_value = float('-inf')
                best_move = None
                for move in available_moves:
                    new_number = number * move
                    new_points = points + (1 if new_number % 2 == 0 else -1)
                    new_bank = bank + (1 if new_number % 5 == 0 else 0)
                    new_level = gameTree[0].level + 1
                    child_state = State(new_number, new_points, new_bank, new_level)
                    value = alpha_beta_search(child_state, float('-inf'), float('inf'), player)
                    if value > best_value:
                        best_value = value
                        best_move = move

                number *= best_move
                # Update moves log
                moves_log.insert(tk.END, f"Dators: {best_move}\n")
        
        points += 1 if number % 2 == 0 else -1
        bank += 1 if number % 5 == 0 else 0
        player = Player.Lietotajs if player == Player.Dators else Player.Dators

        # Update labels during the game
        number_label.config(text=f"Skaitlis: {number}")
        points_label.config(text=f"Punkti: {points}")
        bank_label.config(text=f"Banka: {bank}")

    points += bank * (-1 if points % 2 == 0 else 1)
    winner = "Lietotajs" if player == Player.Dators else "Dators"
    messagebox.showinfo("Game Over", f"Spēle beidzās, gala punkti: {points}\nUzvar {winner}.")

def minimax_search(state, player):
    if state.number > 3000:
        return evaluate_state(state)

    if player == Player.Lietotajs:
        best_value = float('-inf')
        for child_index in state.children:
            child_value = minimax_search(gameTree[child_index], Player.Dators)
            best_value = max(best_value, child_value)
        return best_value
    else:
        best_value = float('inf')
        for child_index in state.children:
            child_value = minimax_search(gameTree[child_index], Player.Lietotajs)
            best_value = min(best_value, child_value)
        return best_value

def alpha_beta_search(state, alpha, beta, player):
    if state.number > 3000:
        return evaluate_state(state)

    if player == Player.Lietotajs:
        value = float('-inf')
        for child_index in state.children:
            child_value = alpha_beta_search(gameTree[child_index], alpha, beta, Player.Dators)
            value = max(value, child_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child_index in state.children:
            child_value = alpha_beta_search(gameTree[child_index], alpha, beta, Player.Lietotajs)
            value = min(value, child_value)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def evaluate_state(state):
    distance_to_goal = abs(3000 - state.number)
    points = state.points
    bank_points = state.bank
    return distance_to_goal * 0.3 + points * 0.5 + bank_points * 0.2

# Create Tkinter window
root = tk.Tk()
root.title("Number Game")

# Create GUI elements
start_button = tk.Button(root, text="Start Game", command=start_game)
number_label = tk.Label(root, text="Skaitlis: ")
points_label = tk.Label(root, text="Punkti: ")
bank_label = tk.Label(root, text="Banka: ")
moves_label = tk.Label(root, text="Moves:")
moves_log = tk.Text(root, width=30, height=10)

# Grid positioning
start_button.grid(row=0, column=0, columnspan=2)
number_label.grid(row=1, column=0, columnspan=2)
points_label.grid(row=2, column=0, columnspan=2)
bank_label.grid(row=3, column=0, columnspan=2)
moves_label.grid(row=4, column=0)
moves_log.grid(row=4, column=1)

root.mainloop()

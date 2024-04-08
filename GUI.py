import tkinter as tk
from tkinter import simpledialog, messagebox
from enum import Enum

GUI_MODE = True
DEBUG = True
SEARCH_DEPTH = 2
END_NUMBER = 3000
MIN_START_NUMBER = 20
MAX_START_NUMBER = 30
MIN_MULTIPLIER = 3
MAX_MULTIPLIER = 5


class Algorithm(Enum):
    MINIMAX = 1
    ALPHA_BETA = 2


class Player(Enum):
    USER = 1
    COMPUTER = 2


class State:
    number: int
    points: int
    bank: int
    level: int
    children: list
    value: float | None

    def __init__(self, number, points, bank, level) -> None:
        self.number = number
        self.points = points
        self.bank = bank
        self.level = level
        self.children = []
        self.value = None

    def __eq__(self, other) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        return ((self.number, self.points, self.bank, self.level) ==
                (other.number, other.points, other.bank, other.level))

    def next_state(self, multiplier: int) -> 'State':
        new_state = State(
            self.number * multiplier,
            self.points + (1 if (self.number * multiplier) % 2 == 0 else -1),
            self.bank + (1 if (self.number * multiplier) % 5 == 0 else 0),
            self.level + 1
        )
        if new_state.number >= END_NUMBER:
            new_state.points += new_state.bank * (-1 if new_state.points % 2 == 0 else 1)
        return new_state

    def evaluate_state(self) -> float:
        max_number = END_NUMBER * MAX_MULTIPLIER
        # Vai stāvoklis ir labvēlīgs pirmajam spēlētājam (maksimizētājam) vai otrajam spēlētājam (minimizētājam)
        k = 1 if (((self.bank if self.number < END_NUMBER else 0) + self.points) % 2 == 0) else -1
        # Vai spēles banka ir lielāka par 0
        x1 = min(self.bank, 1)
        # Ja ir spēles beigu stāvoklis, mazākam skaitlim ir lielāka vērtība
        x2 = (1 if self.number >= END_NUMBER else 0) * (max_number - self.number) / (max_number - 20)
        # Ja nav spēles beigu stāvoklis, lielākam skaitlim ir lielāka vērtība
        x3 = (0 if self.number >= END_NUMBER else 1) * self.number / (max_number - 20)

        return k * (100*x1 + 10*x2 + 1*x3)


def generate_tree(tree: list[State], index=0, depth=SEARCH_DEPTH) -> list[State]:
    tree[index].children = []
    if tree[index].number >= END_NUMBER:
        return tree
    for multiplier in range(MIN_MULTIPLIER, MAX_MULTIPLIER + 1):
        new_state = tree[index].next_state(multiplier)
        if new_state not in tree:
            tree.append(new_state)
            tree[index].children.append(len(tree) - 1)
            if depth > 1:
                tree = generate_tree(tree, len(tree) - 1, depth - 1)
        else:
            tree[index].children.append(tree.index(new_state))
    return tree


def print_tree(tree: list[State], algorithm: Algorithm | None = None, index=0) -> None:
    if algorithm == Algorithm.MINIMAX:
        minimax_search(tree)
    elif algorithm == Algorithm.ALPHA_BETA:
        alpha_beta_search(tree)
    print('\t' * tree[index].level, end='')
    print(f'number: {tree[index].number:<5}', end=' ')
    print(f'points: {tree[index].points:<2}', end=' ')
    print(f'bank: {tree[index].bank}', end=' ')
    print(f'value: {tree[index].evaluate_state():<9.4f}', end=' ')
    if tree[index].value is not None:
        print(f'algorithm: {tree[index].value:.4f}', end='')
    print()
    for state_index in tree[index].children:
        print_tree(tree, None, state_index)


def minimax_search(tree: list[State], index=0) -> dict[str, float]:
    if len(tree[index].children) == 0:
        return {'value': tree[index].evaluate_state()}

    if tree[index].level % 2 == 0:
        best = {'value': float('-inf')}
        for child_index in tree[index].children:
            child = {'value': minimax_search(tree, child_index)['value'],
                     'index': tree[index].children.index(child_index)}
            if child['value'] > best['value']:
                best = child
                tree[child_index].value = best['value']
    else:
        best = {'value': float('inf')}
        for child_index in tree[index].children:
            child = {'value': minimax_search(tree, child_index)['value'],
                     'index': tree[index].children.index(child_index)}
            if child['value'] < best['value']:
                best = child
                tree[child_index].value = best['value']
    tree[index].value = best['value']
    return best


def alpha_beta_search(tree: list[State], index=0, alpha=float('-inf'), beta=float('inf')) -> dict[str, float]:
    if len(tree[index].children) == 0:
        return {'value': tree[index].evaluate_state()}

    if tree[index].level % 2 == 0:
        best = {'value': float('-inf')}
        for child_index in tree[index].children:
            child = {'value': alpha_beta_search(tree, child_index, alpha, beta)['value'],
                     'index': tree[index].children.index(child_index)}
            if child['value'] > best['value']:
                best = child
                tree[child_index].value = best['value']
            alpha = max(alpha, best['value'])
            if alpha >= beta:
                break
    else:
        best = {'value': float('inf')}
        for child_index in tree[index].children:
            child = {'value': alpha_beta_search(tree, child_index, alpha, beta)['value'],
                     'index': tree[index].children.index(child_index)}
            if child['value'] < best['value']:
                best = child
                tree[child_index].value = best['value']
            beta = min(beta, best['value'])
            if alpha >= beta:
                break
    tree[index].value = best['value']
    return best


class Game:
    state: State
    algorithm: Algorithm
    players: list[Player]

    def __init__(self, starting_player: Player, algorithm: Algorithm, starting_number: int) -> None:
        self.state = State(starting_number, 0, 0, 0)
        self.algorithm = algorithm
        if starting_player == Player.USER:
            self.players = [Player.USER, Player.COMPUTER]
        else:
            self.players = [Player.COMPUTER, Player.USER]
        if DEBUG:
            print_tree(generate_tree([self.state], 0, 10 ** 5), algorithm)

    def user_move(self, multiplier: int) -> None:
        self.state = self.state.next_state(multiplier)

    def computer_move(self) -> int:
        tree = generate_tree([self.state])
        if self.algorithm == Algorithm.MINIMAX:
            multiplier = int(minimax_search(tree)['index']) + MIN_MULTIPLIER
        else:
            multiplier = int(alpha_beta_search(tree)['index']) + MIN_MULTIPLIER
        self.user_move(multiplier)
        if DEBUG:
            print_tree(tree, self.algorithm)
        return multiplier

    def get_current_player(self) -> Player:
        return self.players[self.state.level % 2]

    def is_game_finished(self) -> bool:
        return self.state.number >= END_NUMBER

    def get_winner(self) -> Player:
        return self.players[self.state.points % 2]


def int_input(message: str, number_range: range) -> int:
    print(message, end='')
    while True:
        try:
            input_number = int(input())
            if input_number in number_range:
                return input_number
            else:
                print('Nepareiz skaitlis, mēģiniet vēlreiz: ', end='')
        except ValueError:
            print('Kļūda, mēģiniet vēlreiz: ', end='')


def choose_starting_player() -> Player:
    while True:
        print("Izvēlieties, kurš sāks spēli:")
        print("Lietotājs vai dators")
        choice = input("Ievadiet izvēlēto spēlētāju (l vai d): ")
        if choice == "l":
            return Player.USER
        elif choice == "d":
            return Player.COMPUTER
        else:
            print("Nepareiza izvēle. Mēģiniet vēlreiz.")


def choose_algorithm() -> Algorithm:
    while True:
        print("Izvēlieties algoritmu, kuru izmantos dators:")
        print("Minimaksa algoritms vai Alfa-beta algoritms")
        choice = input("Ievadiet izvēlēto algoritmu (m vai a): ")
        if choice == "m":
            return Algorithm.MINIMAX
        elif choice == "a":
            return Algorithm.ALPHA_BETA
        else:
            print("Nepareiza izvēle. Mēģiniet vēlreiz.")


def choose_starting_number() -> int:
    return int_input(f'Ievadiet skaitli no {MIN_START_NUMBER} līdz {MAX_START_NUMBER}: ',
                     range(MIN_START_NUMBER, MAX_START_NUMBER + 1))

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spēle")
        self.geometry("500x250")

        self.game_frame = tk.Frame(self)
        self.game_frame.pack()

        self.game_label = tk.Label(self.game_frame, text="27. komanda")
        self.game_label.pack()

        self.number_label = tk.Label(self.game_frame, text="Skaitlis: ")
        self.number_label.pack()

        self.points_label = tk.Label(self.game_frame, text="Punkti: ")
        self.points_label.pack()

        self.bank_label = tk.Label(self.game_frame, text="Banka: ")
        self.bank_label.pack()

        self.start_game()

    def start_game(self):
        self.start_frame = tk.Frame(self)
        self.start_frame.pack()

        self.player_label = tk.Label(self.start_frame, text="Izvēlieties, kurš sāks spēli:")
        self.player_label.grid(row=0, column=0)

        self.player_var = tk.StringVar(self.start_frame, value="user")
        self.player_radio_user = tk.Radiobutton(self.start_frame, text="Lietotājs", variable=self.player_var, value="user")
        self.player_radio_user.grid(row=0, column=1)

        self.player_radio_computer = tk.Radiobutton(self.start_frame, text="dators", variable=self.player_var, value="computer")
        self.player_radio_computer.grid(row=0, column=2)

        self.algorithm_label = tk.Label(self.start_frame, text="Izvēlieties algoritmu, kuru izmantos dators")
        self.algorithm_label.grid(row=1, column=0)

        self.algorithm_var = tk.StringVar(self.start_frame, value="minimax")
        self.algorithm_radio_minimax = tk.Radiobutton(self.start_frame, text="Minimax", variable=self.algorithm_var, value="minimax")
        self.algorithm_radio_minimax.grid(row=1, column=1)

        self.algorithm_radio_alpha_beta = tk.Radiobutton(self.start_frame, text="Alpha-Beta", variable=self.algorithm_var, value="alpha_beta")
        self.algorithm_radio_alpha_beta.grid(row=1, column=2)

        self.start_num_label = tk.Label(self.start_frame, text="Ievadiet skaitli (no 20 līdz 30):")
        self.start_num_label.grid(row=2, column=0)

        self.start_num_entry = tk.Entry(self.start_frame)
        self.start_num_entry.grid(row=2, column=1)

        self.start_button = tk.Button(self.start_frame, text="Sākt spēli", command=self.initialize_game)
        self.start_button.grid(row=3, columnspan=3)

    def initialize_game(self):
        starting_player = Player.USER if self.player_var.get() == "user" else Player.COMPUTER
        algorithm_choice = Algorithm.MINIMAX if self.algorithm_var.get() == "minimax" else Algorithm.ALPHA_BETA
        starting_number = int(self.start_num_entry.get())

        self.game = Game(starting_player, algorithm_choice, starting_number)
        self.current_player = starting_player

        self.start_frame.pack_forget()
        self.game_frame.pack()

        self.show_turn_widgets()

    def show_turn_widgets(self):
        self.number_label.config(text=f"Skaitlis: {self.game.state.number}")
        if self.current_player == Player.USER:
            if not hasattr(self, 'turn_label'):
                self.turn_label = tk.Label(self.game_frame, text="Ievadiet reizinātāju:")
                self.turn_label.pack()

            if not hasattr(self, 'turn_entry'):
                self.turn_entry = tk.Entry(self.game_frame)
                self.turn_entry.pack()

            if not hasattr(self, 'turn_button'):
                self.turn_button = tk.Button(self.game_frame, text="Ok", command=self.user_move)
                self.turn_button.pack()
        else:
            self.computer_turn()

    def user_move(self):
        multiplier = int(self.turn_entry.get())
        self.game.user_move(multiplier)
        self.update_game_info()
        self.play_turn()

    def play_turn(self):
        if not self.game.is_game_finished():
            if self.current_player == Player.USER:
                self.current_player = Player.COMPUTER
            else:
                self.current_player = Player.USER

            self.show_turn_widgets()
        else:
            self.end_game()

    def computer_turn(self):
        multiplier = self.game.computer_move()
        messagebox.showinfo("Computer Turn", f"Computer chose multiplier: {multiplier}")
        self.update_game_info()
        self.play_turn()

    def update_game_info(self):
        self.number_label.config(text=f"Skaitlis: {self.game.state.number}")
        self.points_label.config(text=f"Punkti: {self.game.state.points}")
        self.bank_label.config(text=f"Banka: {self.game.state.bank}")

    def end_game(self):
        points = self.game.state.points
        points += self.game.state.bank * (-1 if points % 2 == 0 else 1)
        winner = "lietotajs" if self.game.get_winner() == Player.USER else "dators"
        messagebox.showinfo("Game Over", f"Spēle beidzās, gala punkti: {points}\nUzvar {winner}.")

        self.restart_game()

    def restart_game(self):
        self.game_frame.pack_forget()
        self.start_game()


if GUI_MODE:
    root = GUI()
    root.mainloop()
else:
    while True:
        game = Game(choose_starting_player(), choose_algorithm(), choose_starting_number())
    
        while not game.is_game_finished():
            if game.get_current_player() == Player.USER:
                print('Lietotāja gājiens:')
                input_multiplier = int_input(f'Ievadiet reizinātāju no {MIN_MULTIPLIER} līdz {MAX_MULTIPLIER}: ',
                                             range(MIN_MULTIPLIER, MAX_MULTIPLIER + 1))
                game.user_move(input_multiplier)
            else:
                print('Datora gājiens:')
                print('Dators izvēlējās skaitli:', game.computer_move())
    
            print('skailtis:', game.state.number, '| punkti:', game.state.points, '| banka:', game.state.bank)
    
        print('Spēle beidzās, gala punkti:', game.state.points)
        print('Uzvarēja', 'lietotājs' if game.get_winner() == Player.USER else 'dators')
    
        play_again = input("Vai vēlaties spēlēt vēlreiz? (j/n): ")
        if play_again.lower() != "j":
            break

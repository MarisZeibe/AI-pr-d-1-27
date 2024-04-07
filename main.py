import random
from enum import Enum


class Algorithm(Enum):
    MINIMAX = 1
    ALPHA_BETA = 2


class Player(Enum):
    Lietotajs = 1
    Dators = 2


def choose_starting_player() -> Player:
    while True:
        print("Izvēlieties, kurš sāks spēli:")
        print("Lietotājs vai dators")
        choice = input("Ievadiet izvēlēto spēlētāju (l vai d): ")
        if choice == "l":
            return Player.Lietotajs
        elif choice == "d":
            return Player.Dators
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


def evaluate_state(state):
    # distance_to_goal = abs(3000 - state.number)
    # points = state.points
    # bank_points = state.bank
    # return distance_to_goal * 0.3 + points * 0.5 + bank_points * 0.2
    # return 1 if (state.points + ((state.bank * (-1 if state.points % 2 == 0 else 1)) if state.number > 3000 else 0)) % 2 == 0 else -1
    k = 1 if ((state.bank + state.points) % 2 == 0) else -1
    x1 = k * min(state.bank, 1)
    x2 = k * (1 if state.number >= 3000 else 0) * (3000 * 5 - state.number) / (3000 * 5 - 20) #k * (1 if state.number > 3000 else 0) * (15000 - state.number) / (15000 - 20)
    x3 = k * (0 if state.number >= 3000 else 1) * state.number / (3000 * 5 - 20)
    return 100*x1 + 10*x2 + 1*x3


def minimax_search(state, player):
    if state.number >= 3000:
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
    if state.number >= 3000:
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


class State:
    number: int
    points: int
    bank: int
    level: int
    children: list

    def __init__(self, number, points, bank, level):
        self.number = number
        self.points = points
        self.bank = bank
        self.level = level
        self.children = []

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.number, self.points, self.bank, self.level) == (other.number, other.points, other.bank, other.level)


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


def generate_tree(index=0):
    global gameTree
    if gameTree[index].number > 3000:
        return
    for n in range(3, 6):
        new_state = State(
            gameTree[index].number * n,
            gameTree[index].points + (1 if (gameTree[index].number*n) % 2 == 0 else -1),
            gameTree[index].bank + (1 if (gameTree[index].number*n) % 5 == 0 else 0),
            gameTree[index].level + 1
        )
        if new_state.number >= 3000:
            new_state.points += bank * (-1 if new_state.points % 2 == 0 else 1)
        if new_state not in gameTree:
            gameTree.append(new_state)
            gameTree[index].children.append(len(gameTree) - 1)
            generate_tree(len(gameTree) - 1)
        else:
            gameTree[index].children.append(gameTree.index(new_state))


def print_tree(generate_values=False, index=0):
    print('\t' * gameTree[index].level, end='')
    print(f'number: {gameTree[index].number:<5}', end=' ')
    print(f'points: {gameTree[index].points:<2}', end=' ')
    print(f'bank: {gameTree[index].bank}', end=' ')
    if generate_values:
        print(f'value: {evaluate_state(gameTree[index]):<9.4f}', end=' ')
        current_player = player.Lietotajs if gameTree[index].level % 2 == 0 else player.Dators
        print(f'minimax: {minimax_search(gameTree[index], current_player):.4f}', end='')
    print()
    for state_index in gameTree[index].children:
        print_tree(generate_values, state_index)


while True:
    points = 0
    bank = 0
    player = choose_starting_player()
    algorithm = choose_algorithm()
    number = int_input('Ievadiet skaitli no 20 līdz 30: ', range(20, 31))

    gameTree = [State(number, points, bank, 0)]
    generate_tree()
    print_tree(True)

    while number <= 3000:
        print(player, '. spēlētāja gājiens', sep='')
        if player == Player.Lietotajs:
            number *= int_input('Ievadiet reizinātāju (3, 4 vai 5): ', range(3, 6))
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
                print('Datora gājiens. Izvēlēts skaitlis:', best_move)
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
                print('Datora gājiens. Izvēlēts skaitlis:', best_move)

        points += 1 if number % 2 == 0 else -1
        bank += 1 if number % 5 == 0 else 0
        # player = (player % 2) + 1
        player = Player.Lietotajs if player == Player.Dators else Player.Dators
        print('skailtis:', number, '| punkti:', points, '| banka:', bank)

    points += bank * (-1 if points % 2 == 0 else 1)
    print('Spēle beidzās, gala punkti:', points)
    print('Uzvar ', (points % 2) + 1, '. spēlētājs', sep='')

    play_again = input("Vai vēlaties spēlēt vēlreiz? (j/n): ")
    if play_again.lower() != "j":
        break

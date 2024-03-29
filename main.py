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

def minimax_search(state, player):
  if state.number > 3000:
      return state.points

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
      return state.points

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


def print_tree(index=0):
    print('.' * gameTree[index].level, gameTree[index].number, gameTree[index].points, gameTree[index].bank)
    for x in gameTree[index].children:
        print_tree(x)


while True:
    points = 0
    bank = 0
    player = choose_starting_player()
    algorithm = choose_algorithm()
    number = int_input('Ievadiet skaitli no 20 līdz 30: ', range(20, 31))

    gameTree = [State(number, points, bank, 0)]
    generate_tree(0)
    print_tree()
    
    while number < 3000:
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
        #player = (player % 2) + 1
        player = Player.Lietotajs if player == Player.Dators else Player.Dators
        print('skailtis:', number, '| punkti:', points, '| banka:', bank)
    
    points += bank * (-1 if points % 2 == 0 else 1)
    print('Spēle beidzās, gala punkti:', points)
    print('Uzvar ', (points % 2) + 1, '. spēlētājs', sep='')

    play_again = input("Vai vēlaties spēlēt vēlreiz? (j/n): ")
    if play_again.lower() != "j":
        break

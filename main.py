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


while True:  # Viens no uzdevumiem ir "uzsākt spēli atkārtoti pēc kārtējās spēles pabeigšanas."
    points = 0
    bank = 0
    player = 1
    number = int_input('Ievadiet skaitli no 20 līdz 30: ', range(20, 31))

    gameTree = [State(number, points, bank, 0)]
    generate_tree(0)
    print_tree()
    
    while number < 3000:
        print(player, '. spēlētāja gājiens', sep='')
        number *= int_input('Ievadiet reizinātāju (3, 4 vai 5): ', range(3, 6))
        points += 1 if number % 2 == 0 else -1
        bank += 1 if number % 5 == 0 else 0
        player = (player % 2) + 1
        print('skailtis:', number, '| punkti:', points, '| banka:', bank)
    
    points += bank * (-1 if points % 2 == 0 else 1)
    print('Spēle beidzās, gala punkti:', points)
    print('Uzvar ', (points % 2) + 1, '. spēlētājs', sep='')

    # Cikls būs bezgalīgs, taču mēs varam ļaut spēlētājam pašam izlemt, ko darīt tālak
    # play_again = input("Vai vēlaties spēlēt vēlreiz? (j/n): ")
    # if play_again.lower() != "j":
    #     break

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


points = 0
bank = 0
player = 1
number = int_input('Ievadiet skaitli no 20 līdz 30: ', range(20, 31))

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

"""
CIS-15 Monty Hall Paradox
Mike Matera
"""

import random
import os


def pick_random_door():
    """Pick a door."""
    num = random.randrange(1,4)
    if 'DEBUG' in os.environ:
        print(f'DEBUG: pick_random_door() returns {num}')
    return num


def montys_choice(car_door, contestant_door):
    """Monty opens a door."""
    if car_door == 1 and contestant_door == 1:
        monty_door = 2
    elif car_door == 1 and contestant_door == 2:
        monty_door = 3
    elif car_door == 1 and contestant_door == 3:
        monty_door = 2
    elif car_door == 2 and contestant_door == 1:
        monty_door = 3
    elif car_door == 2 and contestant_door == 2:
        monty_door = 3
    elif car_door == 2 and contestant_door == 3:
        monty_door = 1
    elif car_door == 3 and contestant_door == 1:
        monty_door = 2
    elif car_door == 3 and contestant_door == 2:
        monty_door = 1
    elif car_door == 3 and contestant_door == 3:
        monty_door = 2

    if 'DEBUG' in os.environ:
        print(f'DEBUG: montys_choice({car_door}, {contestant_door}) returns {monty_door}')

    return monty_door


def has_won(car_door, contestant_door, switch_or_stay):
    """Did the user win?"""
    if car_door == contestant_door:
        did_win = switch_or_stay == 'stay'
    else:
        did_win = switch_or_stay == 'switch'

    if 'DEBUG' in os.environ:
        print(f'DEBUG: has_won({car_door}, {contestant_door}, {switch_or_stay}) returns {did_win}')

    return did_win


def main():
    car = pick_random_door()
    contestant = int(input('Pick a door: '))
    monty = montys_choice(car, contestant)
    print(f'Monty opens door {monty}')
    sos = input('Switch or stay? ')
    if has_won(car, contestant, sos):
        print("You won a car!")
    else:
        print("You won a goat!")


if __name__ == '__main__':
    main()

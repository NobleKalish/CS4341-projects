import sys
import random
from group17.group17character import Group17Character

sys.path.insert(0, '../bomberman')

# Import necessary stuff
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

step = 1


def variant1(g):
    g.add_character(Group17Character("me",  # name
                                     "C",  # avatar
                                     0, 0,  # position
                                     1  # variant solution
                                     ))
    # Use this if you want to proceed automatically
    g.go(step)
    if g.world.scores["me"] > 0:
        return True


def variant2(g):
    g.add_monster(StupidMonster("stupid",  # name
                                "S",  # avatar
                                3, 9  # position
                                ))

    g.add_character(Group17Character("me",  # name
                                     "C",  # avatar
                                     0, 0,  # position
                                     2
                                     ))

    # Run!
    g.go(step)
    if g.world.scores["me"] > 0:
        return True


def variant3(g):
    g.add_monster(SelfPreservingMonster("selfpreserving",  # name
                                        "S",  # avatar
                                        3, 9,  # position
                                        1  # detection range
                                        ))

    g.add_character(Group17Character("me",  # name
                                     "C",  # avatar
                                     0, 0,  # position
                                     3
                                     ))

    # Run!
    g.go(step)
    if g.world.scores["me"] > 0:
        return True


def variant4(g):
    g.add_monster(SelfPreservingMonster("aggressive",  # name
                                        "A",  # avatar
                                        3, 13,  # position
                                        2  # detection range
                                        ))

    g.add_character(Group17Character("me",  # name
                                     "C",  # avatar
                                     0, 0,  # position
                                     4
                                     ))

    # Run!
    g.go(step)
    if g.world.scores["me"] > 0:
        return True


def variant5(g):
    g.add_monster(StupidMonster("stupid",  # name
                                "S",  # avatar
                                3, 5,  # position
                                ))
    g.add_monster(SelfPreservingMonster("aggressive",  # name
                                        "A",  # avatar
                                        3, 13,  # position
                                        2  # detection range
                                        ))

    g.add_character(Group17Character("me",  # name
                                     "C",  # avatar
                                     0, 0,  # position
                                     5
                                     ))

    # Run!
    g.go(step)
    if g.world.scores["me"] > 0:
        return True


def main():
    test_amount = 10
    wins1 = 0
    wins2 = 0
    wins3 = 0
    wins4 = 0
    wins5 = 0
    for _ in range(test_amount):
        g = Game.fromfile('scenario1/map.txt', sprite_dir="../bomberman/sprites/")
        if variant1(g):
            wins1 += 1
    for _ in range(test_amount):
        g = Game.fromfile('scenario1/map.txt', sprite_dir="../bomberman/sprites/")
        if variant2(g):
            wins2 += 1
    for _ in range(test_amount):
        g = Game.fromfile('scenario1/map.txt', sprite_dir="../bomberman/sprites/")
        if variant3(g):
            wins3 += 1
    for _ in range(test_amount):
        g = Game.fromfile('scenario1/map.txt', sprite_dir="../bomberman/sprites/")
        if variant4(g):
            wins4 += 1
    for _ in range(test_amount):
        g = Game.fromfile('scenario1/map.txt', sprite_dir="../bomberman/sprites/")
        if variant5(g):
            wins5 += 1
    print(f'We won {wins1} out of {test_amount} for variant 1')
    print(f'We won {wins2} out of {test_amount} for variant 2')
    print(f'We won {wins3} out of {test_amount} for variant 3')
    print(f'We won {wins4} out of {test_amount} for variant 4')
    print(f'We won {wins5} out of {test_amount} for variant 5')


if __name__ == "__main__":
    # execute only if run as a script
    main()

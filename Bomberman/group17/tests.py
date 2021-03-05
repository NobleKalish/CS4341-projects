import sys
from bomberman.game import Game
from group17.group17character import Group17Character

sys.path.insert(0, '../bomberman')


def variant1(g):
    g.add_character(Group17Character("me",  # name
                                     "C",  # avatar
                                     0, 0,  # position
                                     1  # variant solution
                                     ))
    # Use this if you want to proceed automatically
    g.go(1)
    if g.world.scores["me"] > 0:
        return True


def variant2():
    pass


def variant3():
    pass


def main():
    g = Game.fromfile('scenario1/map.txt')
    wins1 = 0
    wins2 = 0
    wins3 = 0
    for _ in range(100):
        if variant1(g):
            wins1 += 1
    print(f'We won {wins1} out of 100')


if __name__ == "__main__":
    # execute only if run as a script
    main()

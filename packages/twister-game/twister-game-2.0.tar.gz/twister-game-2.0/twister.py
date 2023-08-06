#!/usr/bin/env python
import sys
import random
from blessings import Terminal

BODY = [
    'Left Hand',
    'Right Hand',
    'Left Foot',
    'Right Foot',
    ]

COLORS = [
    'Red',
    'Green',
    'Blue',
    'Yellow',
    ]

terminal = Terminal()

def choose(name):
    body = random.choice(BODY)
    color = random.choice(COLORS)
    print('%s, put your %s on a %s tile' % (terminal.bold(name),
            terminal.bold(body), getattr(terminal, 'bold_%s' %
                color.lower())(color)))

if __name__ == '__main__':
    names = sys.argv[1:]
    if not names:
        print('Syntax: %s Player1 [Player2 [Player3 [...]]]' % sys.argv[0])
        sys.exit(1)
    while True:
        answer = input('Another round? (Y/n) ')
        if answer.lower() == 'n':
            break
        print()
        for name in names:
            choose(name)
        print()

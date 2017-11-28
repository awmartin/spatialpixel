"""Demonstrates a simple simulation of schooling/swarming behavior.

This simulates a school of fish that exhibit three bottom-up behaviors:

- A fish wants to move towards the center of its neighbors. This encourages them to
get cozy.
- A fish wants to move away from any fish that's encroaching on its personal space.
That is, don't get too cozy.
- A fish wants to turn towards the average direction of its neighbors. This causes
neighbors to swim in the same direction.
"""

import math
import random
from behaviors import *


def setup():
    size(800, 500)

    # How many fish you want in the simulation.
    number_of_fish = 100

    # Add all the fish behaviors and their parameters.
    global behaviors
    behaviors = (
        MoveTowardsCenterOfNearbyFish(closeness=50.0, threshold=25.0, speedfactor=100.0, weight=20.0),
        TurnAwayFromClosestFish(threshold=15.0, speedfactor=5.0, weight=20.0),
        TurnToAverageDirection(closeness=50.0, weight=6.0),
        Swim(speedlimit=3.0, turnratelimit=math.pi / 20.0),
        WrapAroundWindowEdges(),
    )

    # Make some fish!
    global allfishes
    allfishes = []
    for i in xrange(0, number_of_fish):
        allfishes.append(Fish())


def draw():
    background(24)
    for fish in allfishes:
        fish.move()
        fish.draw()


class Fish(object):
    fishcolors = (
        color(255, 145, 8),
        color(219, 69, 79),
        color(255)
    )

    def __init__(self):
        self.position = [random.randrange(0, width), random.randrange(0, height)]
        self.speed = 1
        self.direction = random.random() * 2.0 * math.pi - math.pi
        self.turnrate = 0

        self.fishcolor = Fish.fishcolors[random.randrange(0, len(Fish.fishcolors))]

    def move(self):
        # TODO Globals... Yuck.
        global allfishes, behaviors

        state = {}

        # TODO Make this more efficient.
        for fish in allfishes:
            for behavior in behaviors:
                behavior.setup(self, fish, state)

        for behavior in behaviors:
            behavior.apply(self, state)
            # behavior.draw(self, state)

    def draw(self):
        pushMatrix()

        translate(*self.position)
        rotate(self.direction)

        stroke(self.fishcolor)
        noFill()
        bezier(0, 0, 10, 7, 15, 0, 25, 0)
        bezier(0, 0, 10, -7, 15, 0, 25, 0)
        line(7, 3, 12, 8)
        line(7, -3, 12, -8)

        popMatrix()

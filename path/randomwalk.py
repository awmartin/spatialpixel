"""RandomWalkGenerator

Generates random walks in both 2D and 3D.

The class generates paths as a list of 

"""

import random

class RandomWalkGenerator(object):
    """Generates 2D and 3D random walks, either those that can overlap themselves and those
    which can't.
    
    is3D : Boolean = specifies whether this should be a drawn
    """
    
    def __init__(self, is3D=False, allowOverlap=True):
        self.is3D = is3D
        self.allowOverlap = allowOverlap
        self.path = []
        self.history = []
        
        # State
        self.path = []
        self.history = []
        self.currentStep = 0
        self.totalCount = 0
        self.numSteps = 0

    def getPossibleLocations(self, location):
        """Given a location, just give me the six possible directions I could go."""

        if self.is3D:
            return set([
                (location[0]+1, location[1], location[2]),
                (location[0]-1, location[1], location[2]),
                (location[0], location[1]+1, location[2]),
                (location[0], location[1]-1, location[2]),
                (location[0], location[1], location[2]+1),
                (location[0], location[1], location[2]-1),
            ])
        else:
            return set([
                (location[0]+1, location[1]),
                (location[0]-1, location[1]),
                (location[0], location[1]+1),
                (location[0], location[1]-1),
            ])

    def getAvailableLocations(self, location, denied=None):
        """Given a location, return a set of locations I can go next, but not where I've been before."""

        possibleLocations = self.getPossibleLocations(location)

        if self.allowOverlap:
            return list(possibleLocations)
        else:
            # Remove from the places I could go, the places where I can't go.
            if denied is None:
                return list(possibleLocations.difference(self.path))
            else:
                return list(possibleLocations.difference(self.path).difference(denied))

    def pickNextLocation(self, availableLocations):
        """From the given next available locations, pick one of them."""

        numAvailableLocations = len(availableLocations)
        if not self.allowOverlap and numAvailableLocations == 0:
            return None
        
        pickedLocationIndex = random.randrange(0, numAvailableLocations)
        return availableLocations[pickedLocationIndex]
    
    def generate(self, startLocation, numSteps, seed=None, onStep=None):
        """Given a starting location, return a path with "numSteps" steps."""
        
        self.start(startLocation, numSteps, seed=seed)
        
        while self.currentStep < self.numSteps:
            self.step(onStep)
            self.resetIfNecessary()
    
        return self.path
    
    def start(self, startLocation, numSteps, seed=None):
        random.seed(seed)

        self.path = [startLocation]
        self.history = [None]
        self.numSteps = numSteps
        self.totalCount = 0
        self.currentStep = 0
    
    def step(self, onStep=None):
        if self.currentStep < self.numSteps:
            i = self.currentStep
                
            currentLocation = self.path[i]
            knownBadMoves = self.history[i]
            
            availableLocations = self.getAvailableLocations(currentLocation, knownBadMoves)
            pickedNextLocation = self.pickNextLocation(availableLocations)
            
            if pickedNextLocation is None:
                # You know you've reached a dead end, so remember this for later as a bad move.
                if self.history[i - 1] is None:
                    self.history[i - 1] = [currentLocation]
                else:
                    self.history[i - 1].append(currentLocation)
                
                self.path.pop()
                self.history.pop()
                i -= 1
            else:
                self.path.append(pickedNextLocation)
                self.history.append(None)
                i += 1
            self.currentStep = i
    
        if onStep is not None:
            onStep(self.path)
    
    def resetIfNecessary(self):
        if self.currentStep < self.numSteps:
            # Behavior that takes big steps back when you take a long time.
            self.totalCount += 1
            
            if self.totalCount % (self.numSteps * 2) == 0:
                # print "hmm, taking a while", totalCount, i, numSteps
                # It's taking twice as long as the ideal, so take many steps back instead of just one.
                i = random.randrange(0, self.currentStep)
                self.path = self.path[:i+1]
                self.history = self.history[:i+1]
                self.currentStep = i


if __name__ == "__main__":
    pathFinder = RandomWalkGenerator()
    path = pathFinder.generate((0, 0), 10)
    print path
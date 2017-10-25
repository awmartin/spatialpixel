import math

class Behavior(object):
    def __init__(self, **parameters):
        self.parameters = parameters

    def setup(self, fish, otherfish, state):
        pass

    def apply(self, fish, state):
        pass

    def draw(self, fish, state):
        pass


class MoveTowardsCenterOfNearbyFish(Behavior):
    def setup(self, fish, otherfish, state):
        if fish is otherfish:
            return
        if 'closecount' not in state:
            state['closecount'] = 0.0
        if 'center' not in state:
            state['center'] = [0.0, 0.0]

        closeness = self.parameters['closeness']
        distance_to_otherfish = dist(
            otherfish.position[0], otherfish.position[1],
            fish.position[0], fish.position[1]
            )

        if distance_to_otherfish < closeness:
            if state['closecount'] == 0:
                state['center'] = otherfish.position
                state['closecount'] += 1.0
            else:
                state['center'][0] *= state['closecount']
                state['center'][1] *= state['closecount']

                # state['center'][0] += otherfish.position[0]
                # state['center'][1] += otherfish.position[1]
                state['center'] = [
                    state['center'][0] + otherfish.position[0],
                    state['center'][1] + otherfish.position[1]
                    ]

                state['closecount'] += 1.0

                state['center'][0] /= state['closecount']
                state['center'][1] /= state['closecount']

    def apply(self, fish, state):
        if state['closecount'] == 0:
            return

        center = state['center']
        distance_to_center = dist(
            center[0], center[1],
            fish.position[0], fish.position[1]
            )

        if distance_to_center > self.parameters['threshold']:
            angle_to_center = math.atan2(
                fish.position[1] - center[1],
                fish.position[0] - center[0]
                )
            fish.turnrate += (angle_to_center - fish.direction) / self.parameters['weight']
            fish.speed += distance_to_center / self.parameters['speedfactor']

    def draw(self, fish, state):
        closeness = self.parameters['closeness']
        stroke(200, 200, 255)
        noFill()
        ellipse(fish.position[0], fish.position[1], closeness * 2, closeness * 2)


class TurnAwayFromClosestFish(Behavior):
    def setup(self, fish, otherfish, state):
        if fish is otherfish:
            return
        if 'closest_fish' not in state:
            state['closest_fish'] = None
        if 'distance_to_closest_fish' not in state:
            state['distance_to_closest_fish'] = 1000000

        distance_to_otherfish = dist(
            otherfish.position[0], otherfish.position[1],
            fish.position[0], fish.position[1]
            )

        if distance_to_otherfish < state['distance_to_closest_fish']:
            state['distance_to_closest_fish'] = distance_to_otherfish
            state['closest_fish'] = otherfish

    def apply(self, fish, state):
        closest_fish = state['closest_fish']
        if closest_fish is None:
            return

        distance_to_closest_fish = state['distance_to_closest_fish']
        if distance_to_closest_fish < self.parameters['threshold']:
            angle_to_closest_fish = math.atan2(
                fish.position[1] - closest_fish.position[1],
                fish.position[0] - closest_fish.position[0]
                )
            fish.turnrate -= (angle_to_closest_fish - fish.direction) / self.parameters['weight']
            fish.speed += self.parameters['speedfactor'] / distance_to_closest_fish

    def draw(self, fish, state):
        stroke(100, 255, 100)
        closest = state['closest_fish']
        line(fish.position[0], fish.position[1], closest.position[0], closest.position[1])


class TurnToAverageDirection(Behavior):
    def setup(self, fish, otherfish, state):
        if fish is otherfish:
            return
        if 'average_direction' not in state:
            state['average_direction'] = 0.0
        if 'closecount_for_avg' not in state:
            state['closecount_for_avg'] = 0.0

        distance_to_otherfish = dist(
            otherfish.position[0], otherfish.position[1],
            fish.position[0], fish.position[1]
            )

        closeness = self.parameters['closeness']
        if distance_to_otherfish < closeness:
            if state['closecount_for_avg'] == 0:
                state['average_direction'] = otherfish.direction
                state['closecount_for_avg'] += 1.0
            else:
                state['average_direction'] *= state['closecount_for_avg']
                state['average_direction'] += otherfish.direction
                state['closecount_for_avg'] += 1.0
                state['average_direction'] /= state['closecount_for_avg']

    def apply(self, fish, state):
        if state['closecount_for_avg'] == 0:
            return
        average_direction = state['average_direction']
        fish.turnrate += (average_direction - fish.direction) / self.parameters['weight']


class Swim(Behavior):
    def setup(self, fish, otherfish, state):
        fish.speed = 1
        fish.turnrate = 0

    def apply(self, fish, state):
        # Move forward, but not too fast.
        if fish.speed > self.parameters['speedlimit']:
            fish.speed = self.parameters['speedlimit']
        fish.position[0] -= math.cos(fish.direction) * fish.speed
        fish.position[1] -= math.sin(fish.direction) * fish.speed

        # Turn, but not too fast.
        if fish.turnrate > self.parameters['turnratelimit']:
            fish.turnrate = self.parameters['turnratelimit']
        if fish.turnrate < -self.parameters['turnratelimit']:
            fish.turnrate = -self.parameters['turnratelimit']
        fish.direction += fish.turnrate

        # Fix the angles.
        if fish.direction > math.pi:
            fish.direction -= 2 * math.pi
        if fish.direction < -math.pi:
            fish.direction += 2 * math.pi


class WrapAroundWindowEdges(Behavior):
    def apply(self, fish, state):
        if fish.position[0] > width:
            fish.position[0] = 0
        if fish.position[0] < 0:
            fish.position[0] = width
        if fish.position[1] > height:
            fish.position[1] = 0
        if fish.position[1] < 0:
            fish.position[1] = height

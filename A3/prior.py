
class Prior:

    def __init__(self, states):
        self.states = states

    def __hash__(self):
        total = 1

        for state in self.states:
            total *= state.__hash__()

        return total

    def __eq__(self, other):
        return hash(self) == hash(other)

import random


class Node:
    children = []
    parents = []

    def __init__(self, states, parents, probability_distribution):
        self.probability_distribution = probability_distribution
        self.states = states
        self.parents = parents

        # BELOW THIS IS VALIDATION FOR CORRECT DATA INPUT
        parent_states = []
        for parent in parents:
            for state in parent.states:
                parent_states.append(state)

        for prior in list(probability_distribution.keys()):
            probabilities = probability_distribution[prior]

            # Assert that the dependent states are results of the parents
            for state in prior.states:
                if state not in parent_states and state is not None:
                    print('Unsupported state: ' + str(state))
                    raise ()

            # Assert the sum of probabilities of each prior is 1
            total = 0
            for event in list(probabilities.keys()):
                total += probabilities[event]

                # Ensure that each output is in the node's state
                if event not in self.states:
                    print("State " + str(event) + " not in declared states!")
                    raise()

            if total != 1.0:
                print("Sum of probabilities is not 1!")
                raise ()

    def is_independent(self):
        return len(self.parents) == 0

    def determine_state(self, prior):
        """Calculates the current state given some prior. Returns the current state"""

        outcome_distribution = self.probability_distribution[prior]

        summed_probability = 0.0
        rand_num = random.random()

        for key in list(outcome_distribution.keys()):
            if rand_num <= summed_probability + outcome_distribution[key]:
                return key
            else:
                summed_probability += outcome_distribution[key]

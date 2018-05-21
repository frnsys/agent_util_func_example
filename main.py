import random

# actions
def turn_on_ac(agent_state, world_state):
    agent_state['room_temp'] -= 1
    world_state['temperature'] += 0.1
    return agent_state, world_state

def turn_off_ac(agent_state, world_state):
    agent_state['room_temp'] += 1
    world_state['temperature'] -= 0.1
    return agent_state, world_state


def weighted_choice(choices):
    """randomly select a key from a dictionary,
    where each key's value is its probability weight.
    """
    # randomly select a value between 0 and
    # the sum of all the weights.
    rand = random.uniform(0, sum(choices.values()))

    # seek through the dict until a key is found
    # resulting in the random value.
    summ = 0.0
    for key, value in choices.items():
        summ += value
        if rand < summ: return key

    # shouldn't get here
    raise Exception('Failed to choose from choices')


class Agent:
    def __init__(self):
        # choose non-zero random value in (0, 1]
        self.heat_tolerance = max(1e-6, random.random())
        self.concern_for_environment = max(1e-6, random.random())
        self.state = {
            'room_temp': 20
        }
        self.actions = {
            'turn on ac': turn_on_ac,
            'turn off ac': turn_off_ac
        }

    def utility(self, state, world_state):
        """compute the utility of a given state"""
        # as temperature goes up, utility goes down,
        #   inversely proportional to heat tolerance
        a = -(world_state['temperature']/self.heat_tolerance)

        # as temperature goes up, utility goes down,
        #   proportional to concern for environment
        b = -(world_state['temperature'] * self.concern_for_environment)
        return a + b

    def successor(self, action, world_state):
        """given an action, return the new state
        that would result from executing that action"""
        # work with a copy of the state
        # so we don't mutate the actual state
        state_copy = dict(self.state)
        world_state_copy = dict(world_state)
        return action(state_copy, world_state_copy)

    def decide(self, world_state):
        """decide an action, based on utilities
        resulting from potentially taking those actions"""
        utilities = {}
        for action_name, action in self.actions.items():
            next_state, next_world_state = self.successor(action, world_state)
            utilities[action] = self.utility(next_state, next_world_state)

        # choose action with max utility
        # action = max(utilities, key=lambda k: utilities[k])

        # OR

        # choose actions using utilities as probability distribution
        # first, normalize utilities
        utility_mass = sum(utilities.values())
        utilities = {a: u/utility_mass for a, u in utilities.items()}
        # then randomly choose action
        action = weighted_choice(utilities)
        return action

    def execute(self, action, world_state):
        """executes an action"""
        next_state, next_world_state = self.successor(action, world_state)
        self.state = next_state
        return next_world_state


if __name__ == '__main__':
    # run simulation for 1000 steps
    steps = 1000

    # initial world state
    world = {
        'temperature': 20
    }

    # population of agents
    agents = [Agent() for _ in range(100)]

    # run the simulation
    for _ in range(steps):
        for agent in agents:
            action = agent.decide(world)
            world = agent.execute(action, world)
    print(world)
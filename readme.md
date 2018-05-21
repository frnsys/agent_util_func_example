Simple example of an agent-based simulation using utility functions for decision making.

Code is commented but here's an overview.

## Agents

Two possible actions an agent can take:

- turn on their AC (decreases room temp, increases world temp)
- turn off their AC (increase room temp, decrease world temp)

Agent states are simple, consists of just their `room_temp` (room temperature).

Agent parameters ("personalities") are their `heat_tolerance` and their `concern_for_environment` (these are randomly initialized).

### Decision-making

Agents decide what action take by the following (this is the `Agent.decide` method):

- look at how each action will affect their internal state and the world state
- compute their utility for these states
- if `weighted=True`, randomly choose an action weighted by utility
- if `weighted=False`, choose the action with the highest utility

## World

The world state consists of just a `temperature` variable.
# n-Best Multi-Agent Search

Often times we need good approximate solutions to multi-agent search with
conflicts. For exact solutions it is a np hard problem but often for
applications like game agents, an exact solution is not necessary. Here I
propose a monte-carlo method to get a good approximate solution.

This solution is called n-Best and has significant advantages for multi-processed
hardware to take advantage of parallel processing. The way we do this is based on
multi-agent search based on processing order of the agent. Therefore take a map
with 5 agents and the processing order is (1,2,3,4,5). This means agent 1 will be
processed first (can use whatever pathfinding algorithm like A* or Dijkstra's) without
any restrictions to the other agents except their starting locations. We keep track
of the path the agent takes at every timestep so it is blocked for the other agents
at that timestep. Afterwards, agent two will be processed with the condition that
it cannot conflict with agent 1 at any specific time step to get to a goal. We
keep doing this for all the agents until they are processed. If we process the agents
differently, we might have a different result, for example, (4,2,3,1,5) might have
conditionals such that 1 can no longer take the path it would have taken if it was
processed first.

## Experiment

For these experiments I will test on a grid world with a variable amount of agents
on multi-core processors. Note if there are no conflicts, it will return at once
since the ordering does not matter. This way the time complexity of the best case
will stay at the lower bound.

## Thanks

Template code from [atb033/multi_agent_path_planning](https://github.com/atb033/multi_agent_path_planning/tree/master) on GitHub for CBS
[https://atb033.github.io/multi_agent_path_planning/](https://atb033.github.io/multi_agent_path_planning/)

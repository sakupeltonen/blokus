from agent_interface import AgentInterface
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from game import Game
import random

class MarkovAgent(AgentInterface):
    """
    Markov Agent: Evaluate each action by taking it, followed by
    random plays. Action with most wins is chosen.
    """
    def __init__(self):
        # self.__simulator = Game(RandomAgent(), RandomAgent())
        self.__simulator = Game(GreedyAgent(), GreedyAgent())

    def info(self):
        return {"agent name": "Markov"}

    def decide(self, state, actions):
        if len(actions) == 1:
            yield "pass"
            return
        actions = [a for a in actions if a != "pass"]
        win_counter = [0] * len(actions)
        counter = 0
        while True:
            counter += 1
            for i, action in enumerate(actions):
                if random.random() > 0.01:
                    continue
                state2 = state.successor(action)
                result = self.__simulator.play(output=False, starting_state=state2)
                win_counter[i] += 1 if result == state.player else 0
            yield actions[win_counter.index(max(win_counter))]

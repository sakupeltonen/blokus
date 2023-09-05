import random
from agent_interface import AgentInterface


class RandomAgent(AgentInterface):
    @staticmethod
    def info():
        return {"agent name": "Random"}

    def decide(self, state, actions):
        if len(actions) == 1:
            yield actions[0]
            return
        while True:
            action = random.choice(actions)
            if action != 'pass':
                break
        yield action

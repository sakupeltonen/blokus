from agent_interface import AgentInterface
from blokus import pieces

class GreedyAgent(AgentInterface):
    @staticmethod
    def info():
        return {"agent name": "Greedy"}

    def decide(self, state, actions):
        if len(actions) == 1:
            yield actions[0]
            return

        sizes = {}
        for id in state.freePieces[state.player]:
            sizes[id] = len(pieces[id][0])

        maxSize = 0
        maxAction = None
        for action in actions:
            if action == 'pass': continue
            id, symmetry, place, _ = action

            if sizes[id] > maxSize:
                maxSize = sizes[id]
                maxAction = action

        yield maxAction
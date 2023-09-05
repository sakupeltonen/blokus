from agent_interface import AgentInterface
from blokus import tfPieces, pieces, drawPiece

class HumanAgent(AgentInterface):
    @staticmethod
    def info():
        return {"agent name": "Human"}

    def decide(self, state, actions):
        actions = [a for a in actions if a != "pass"]
        actions.sort(key=lambda action: action[0])
        action_dict = { i: action for i, action in enumerate(actions) }

        def get_input():
            input_ = input("Töttöröö\n")

            cmd = input_.split(" ")

            if cmd[0] == "pass":
                return "pass"

            id = int(cmd[1])

            if cmd[0] == 'view':
                for i in action_dict.keys():
                    action = action_dict[i]
                    if action[0] == id:
                        print(f"{i}: {state.actionStr(action)}")
                        state.successor(action).print()

                return try_get_input()

            elif cmd[0] == 'look':
                if len(cmd) == 3:
                    symmetry = cmd[2]
                    print(f"{pieces[id][2]} ({symmetry})")
                    drawPiece(tfPieces[id][symmetry])
                else:
                    for symmetry in tfPieces[id].keys():
                        print(f"{pieces[id][2]} ({symmetry})")
                        drawPiece(tfPieces[id][symmetry])
                return try_get_input()

            elif cmd[0] == 'place':
                if len(cmd) == 2:
                    actionId = int(cmd[1])
                    action = action_dict[actionId]
                    return action
                else:
                    # TODO
                    # symmetry = cmd[2]
                    # x = int(cmd[3])
                    # y = int(cmd[4])
                    return try_get_input()

            else:
                print("jaa")
                return try_get_input()


        def try_get_input():
            try:
                return get_input()
            except Exception as e:
                print(e)
                return try_get_input()

        yield try_get_input()


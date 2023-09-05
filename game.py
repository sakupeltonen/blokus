from agent_interface import AgentInterface
from blokus import BlokusState
from time_limit import time_limit
import random


class Game:
    def __init__(self, player1, player2):
        self.__players = [None, player1, player2]
        self.marks = [None, 'X', 'O']

    def play(self, output=False, starting_state=BlokusState.initial(), timeout_per_turn=None):
        state, winner = self.__play(output, starting_state, timeout_per_turn)
        if output:
            print("Game ends.")
            player1Info = self.__players[1].info()["agent name"]
            player2Info = self.__players[2].info()["agent name"]
            print(f"Squares left in hand:")
            print(f"\t{player1Info} ({self.marks[1]}): {state.cost()[0]}")
            print(f"\t{player2Info} ({self.marks[2]}): {state.cost()[1]}")
            if winner == 0:
                print("The game ended in a draw!")
            else:
                playerInfo = self.__players[winner].info()["agent name"]
                print(f"{playerInfo} ({self.marks[winner]}) WON!")

        return winner

    def __play(self, output, state, timeout_per_turn):
        while True:
            actions = state.actions()
            if all(state.skips.values()):
                return state, state.winner()
            else:
                if output:
                    playerInfo = self.__players[state.player].info()["agent name"]
                    print(f"{playerInfo}'s ({self.marks[state.player]}) turn")
                action = self.__get_action(self.__players[state.player], state, actions, timeout_per_turn)
                # action = self.__get_action_debug(self.__players[state.player], state, actions)
                action = random.choice(actions) if action is None else action
                sstate = state.successor(action)
            if output:
                print(state.actionStr(action))
                sstate.print()
            state = sstate

    def __get_action(self, player, state, actions, timeout):
        action = None
        try:
            with time_limit(timeout):
                for decision in player.decide(state, actions):
                    action = decision
        except TimeoutError:
            if action is None:
                print(f"Timeout")
        return action

    def __get_action_debug(self, player, state, actions):
        action = None
        for decision in player.decide(state, actions):
            action = decision
        return action

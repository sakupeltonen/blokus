import time
from game import Game
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from human_agent import HumanAgent
from markov_agent import MarkovAgent
# from markov_agent import MarkovAgent
# from minimax_agent import MinimaxAgent
# from senpAI import Agent

def main():
    game = Game(GreedyAgent(), MarkovAgent())
    # game = Game(GreedyAgent(), RandomAgent())
    # game = Game(GreedyAgent(), HumanAgent())
    # game = Game(RandomAgent(), RandomAgent())
    game.play(output=True, timeout_per_turn=5.0)

def clock():
    i = 0
    start = time.time()
    while True:
        game = Game(RandomAgent(), RandomAgent())
        game.play(output=False, timeout_per_turn=1)
        i += 1

        if i % 20 == 0:
            elapsed = time.time() - start
            average = elapsed / i
            print(f"{i} games in {elapsed} with average {average} per game")

if __name__ == "__main__":
    main()

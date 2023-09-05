class AgentInterface:
    @staticmethod
    def info():
        """
        Return the agent's information

        This function returns the agent's information as a dictionary variable.
        The returned dictionary should contain at least the `agent name`.

        Returns
        -------
        Dict[str, str]
        """
        raise NotImplementedError

    def decide(self, state, actions):
        """
        Generate a sequence of increasing good actions form `actions` list

        This is a generator function; it means it should have no return
        statement, but it should yield a sequence of increasing good actions.

        Parameters
        ----------
        state: BlokusState
            Current state of the board
        actions: [(pieceId, symmetry, coordinate)] + ['pass']
            List of all possible actions

        Yields
        ------
        action
            the chosen `action` from the `actions` list
        """

        raise NotImplementedError


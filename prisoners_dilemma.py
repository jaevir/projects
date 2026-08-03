"""
Prisoner's Dilemma

Objective:
Test different strategies in a infinite horizon game where we want to see which set of strategies is optimal for both players
The user will input how many rounds, and also which strategy for each player

Features:
OOP
Discount Factor
User Interface
Data-Collection? (Pandas?) Need to research this
Unit-Testable
Generators to yield result at each  time

New Skills Needed:
- Need to research how to collect data for each round
- Need to research how to visualise the data
- Need to research how to implement discount factor
"""

"""
First Milestone: Implement Finite Version first
Second Milestone: Implement Discount Factor and Infinite Version  and Generator stuff

"""
return 

def main():
    Player_A = Player.get()
    Player_B = Player.get()
    while True:
        try:
            rounds = int(input("Rounds: "))
            if rounds<1:
                raise ValueError("Rounds must be at least 1")
            break
        except ValueError as error:
            print(f"Invalid input: {error}")#prints either rounds must be at least 1 or invalid literal for int()
    play_game(Player_A, Player_B, rounds)


class Player:
    # this Class will contain all the strategies, and data unique to the player
    # I chose to separate the playing and payoffs part from the 'class' cause I wanted to make the function of the class solely just for the 'player' and not for the 'game', conversely I added the input method to the class cause it directly relates to getting data
    strategies = [
        "grim trigger",
        "tit-for-tat",
        "reverse tit-for-tat",
        "always defect",
        "always cooperate",
    ]

    def __init__(self, name, strategy):
        self.strategy = strategy
        self.history = []
        self.payoff = 0
        self.name = name

    def __str__(self):
        return f"{self.name} has {self.payoff} points using {self.strategy}"

    @classmethod
    def get(cls):
        print(f"These are the available strategies: {cls.strategies}")
        # note we can't just drop strategies like that, we need to put cls at first to access it--it's not a local variable!
        while True:
            try:
                name = input("Player's Name: ")
                strategy = input("Player's Strategy: ").lower().strip()
                return cls(name, strategy)
            except ValueError as error:
                print(f"Error: {error}")#'as error' prints "NEeds a name" or "Invalid strategy..." The specific error that occurs so the user knows what's up
                print("Please try again.\n")

    @property  # this is the getter for when we have a non-assignment related operation that requires the value
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        if (
            strategy not in Player.strategies
        ):  # we do Player.strategies cause we dont have a cls to do it with
            raise ValueError(f"Invalid Strategy. Choose from {Player.strategies}")
        self._strategy = strategy

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, history):
        if history and not all(
            action in ["C", "D"] for action in history
        ):  # note all checks each element of the list if it's valid, new function! also list comprehension, we tried doing 'not history or ["C", "D"] only in history, but it didn't work
            raise ValueError(f"Invalid Action. Choose from ['C', 'D']")
        self._history = history

    @property
    def payoff(self):
        return self._payoff

    @payoff.setter
    def payoff(self, payoff):
        if not isinstance(payoff, int):
            raise ValueError("Payoff Must be an Integer")
        self._payoff = payoff

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Needs a Name")
        self._name = name


def always_cooperate(my_history: list, opponent_history: list) -> str:
    return "C"


def always_defect(my_history: list, opponent_history: list) -> str:
    return "D"


def tit_for_tat(my_history: list, opponent_history: list) -> str:
    if len(opponent_history) == 0:
        return "C"
    return opponent_history[-1]


def grim_trigger(my_history: list, opponent_history: list) -> str:
    if len(opponent_history) == 0:
        return "C"
    elif "D" in opponent_history:
        return "D"
    else:
        return "C"


def reverse_tit_for_tat(my_history: list, opponent_history: list) -> str:
    if len(opponent_history) == 0:
        return "D"
    return opponent_history[-1]

function_map = {
    "always cooperate": always_cooperate,
    "always defect": always_defect,
    "tit-for-tat": tit_for_tat,
    "reverse tit-for-tat": reverse_tit_for_tat,
    "grim trigger": grim_trigger,
}

def play_game(
    player_a: Player, player_b: Player, rounds=100
) -> tuple:  # note we need type hints otherwise pylance doesn't know what we're putting in, and it registers our attributes as unknown below
    # this is where we play the game iteratively and create a generator and also the panda dataframe stuff
    if player_a.strategy not in function_map or player_b.strategy not in function_map:
        raise ValueError(f"Unknown Strategy! Choose from {Player.strategies}")
    for _ in range(rounds):
        action_a = function_map[player_a.strategy](
            player_a.history, player_b.history
        )  # verbose way of trying to match the string to the function using dicts lol--I struggled a lot with this, design choice
        action_b = function_map[player_b.strategy](player_b.history, player_a.history)
        payoff_a, payoff_b = payoff_matrix(action_a, action_b)
        player_a.payoff += payoff_a  # note we don't assign the attributes directly otherwise that defeats the point of a cumulative payoff, it'll be fine if rounds=1!
        player_b.payoff += payoff_b
        player_a.history.append(action_a)
        player_b.history.append(action_b)
    print(player_a)
    print(player_b)
    return (player_a.payoff, player_b.payoff)


def payoff_matrix(action_A: str, action_B: str) -> tuple:
    if action_A == "C" and action_B == "C":
        return (2, 2)
    elif action_A == "C" and action_B == "D":
        return (-2, 10)
    elif action_A == "D" and action_B == "C":
        return (10, -2)
    elif action_A == "D" and action_B == "D":
        return (0, 0)
    # note that previously I ended off here, but my payoff matrix thing in play_game had an error as it said that None was a possible value which is true because I ended off with 'elif'-- if I input apple and oranges, it would return None which isn't iterable and able to be split-- so i need something to catch 'all' that isn't C or D
    raise ValueError(
        f"Invalid moves:{action_A}, {action_B}"
    )  # the principle of this is to catch all code


if __name__ == "__main__":
    main()

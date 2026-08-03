# Modelling a Finite Prisoner's Dilemma


# OBJECTIVE
This project aims to simulate a finite Prisoner's Dilemma game between two players using a predetermined set of strategies.

My goal is to model this environment, allowing the user the chance to experiment and observe how cumulative payoffs for each player varies as strategies and the number of finite rounds vary. 

# The Prisoner's Dilemma Explained

The Prisoner's Dilemma is a foundational concept in Game Theory. In the classic scenario, we have two players, A and B for instance. 

Suppose we have two players A and B. For some odd reason or crime, both are taken in as prisoners somewhere to be interrogated. 

The two players are separated in different rooms, and each player is completely unaware of the other's actions. 

Each player has two choices: Defect ('D') or Cooperate. 

Cooperate means that the player chooses to stay silent and not betray his partner. 
Defect means that the player chooses to 'snitch' and testify against their partner. 

In Game Theory, we use a payoff matrix to model the consequences of their simultaneous actions. 
| | **Player B: Cooperate (C)** | **Player B: Defect (D)** |
| :--- | :---: | :---: |
| **Player A: Cooperate (C)** | (2, 2) | (-2, 10) |
| **Player A: Defect (D)** | (10, -2) | (0, 0) |

Naturally, the scenario where the other player chooses to Cooperate while you Defect yields the highest reward for you (10) and the worst penalty for them (-2). If both Cooperate, the outcome is mutually beneficial (2, 2). However, if both give in to the temptation to Defect, both walk away with nothing (0, 0).

### Design Choice: Finite vs. Infinite Games
There are two primary types of repeated 'Prisoner's Dilemma' games: Finite and infinite. In repeated games, players know the other player's *past* actions, but they must make their current round decisions simultaneously. I.e. each player has no knowledge of what the other will choose in the current round. 

While I could have restricted myself to just a single roundd, I wanted to model the behaviour of players over repeated games to produce a more dynamic result. Originally, I attempted to model an infinite game with a discount factor. However, I realised that this required libraries like Pandas for data-tracking. Instead, I made the design choice to build a finite version relying **strictly on the basic Python library**. This allowed me to demonstrate to myself how powerful the basic Python library can be using the concepts I've learnt throughout CS50P. 



## Strategies
The Prisoner's Dilemma has been much analysed and there are some well-known 'strategies' anybody who finds themselves in such a scenarion can draw upon. These strategies rely on what we call the 'history of play', or the known past sequence of actions my opposing player has chosen in previous rounds. 

I have created individual strategy functions based on what each strategy is.

### Design Choice: Global Scope for Strategy Functions
I chose not to put the strategy functions as class methods under the Player class as I wanted my Player class to be more streamlined and to directly function like a 'Player', strictly representing player data. Instead, I gave my strategy functions global scope. This models real life decision-making where we submit to our 'contextual knowledge' or the 'higher powers' of the game to determine our actions.

I detail what each strategy means here:
1. **Always Cooperate**
This refers to a player's actions being independent of what the opponent's actions are or their history of play. No matter what they play, I will always play "Cooperate" in every round played.

2. **Always Defect**
This is the exact opposite of Always Cooperate. No matter what the opponent plays, I will always play "Defect' in every round played. 

3. **Tit-for-Tat**
Tit-for-tat is dependent on my opponent's history of play. It is recursive. 
I will always play my opponent's past action in the previous round. 
At the start, I will choose to play "C" by convention. Nobody wants to start off on a bad note!

4. **Reverse Tit-for-Tat**
The same as Tit-for-Tat, but we start off on "D". This is just to facilitate a symmetrical order of play and observe the resulting consequences.

5. **Grim Trigger**
This is dependent on my opponent's history of play. One can consider this as modelling 'trust' and 'betrayal'.
If my opponent always 'Cooperates', I will similarly cooperate too. 
The moment they play "Defect", this will 'trigger' the 'Grim Trigger', and I will always play 'Defect" regardless of whether they choose to play "Cooperate" in a future round. I will never "Cooperate", or more intuitively 'trust' them again. Trust, once broken, is never regained.


## What My Code Does

My code anchors itself on Object-Oriented Programming (OOP).

### Design Choice: Using OOP
I chose to use OOP as I realised that my project objectives necessitated a lot of value updating, modification, and data retrieval. OOP allowed me to bundle this in an efficient and streamlined way. It was also fun to create a data type that was just 'Player'. 

## What my Player Class does

My Player class essentially acts as a real 'Player' with all the attributes you might expect.
It stores attributes like strategies, payoff value, name, and their history of moves.
The class has one 'class' variable which is the set list of strategies.
It has one class method for 'getting' input values at the start for 'name' and 'strategy'.


---

## Sequence of Play


### A. Prompting the User and Instantiating our Players

1. When main() is run, we first call the 'get' class method under the Player class. 

2. This class method prompts the user for two inputs: the name and then the strategy they want. We also print the set list of strategies available. Note that we created a 'while loop' to catch any errors the user makes when typing in the strategies. 

3. 'get' returns the two values to the Player class, and we instantiate our two instances: Player_A and Player_B. We have setters and getters in case, for some reason, the values we pass into Player are not valid. These will raise ValueErrors. 

4. We enter a while loop to prompt the user for the number of rounds they would like to repeat the game for. We raise a ValueError if the number is less than 1 or if the input value is not an integer.

5. We call the 'play_game' function, and start our modelling. 



### B. Modelling our Game and Calculating Cumulative Payoffs. 

1. We perform a final check if the strategy values within our player instances are valid strategies, otherwise we raise ValueErrors. 

2. We enter a for loop based on the number of rounds.

   **Design Choice:* The most interesting design choice in this code is something I struggled with a lot. 
    Fundamentally, how might I map my strategy names to the corresponding strategy functions? 
    After much thought and many Exceptions, I realised that I could just use a dictionary and map the strategy_names as 'keys' to the corresponding 'value' which would be the literal function itself. 

3. After calling the strategy functions, inputting our player strategies, and receiving the consequent actions to take, we input these actions into our pay_off matrix function. 
    The payoff_matrix function just models the table we saw above, where each combination of "Defect' or "Cooperate' returns a specific tuple of payoffs. 

   **Design Choice*
    The background to an interesting design choice here was that after writing all 'elifs' into my matrix, I missed out on 'else'. This meant that any value not caught by my combination of actions would return 'None' back to my play_game function. This was an error curiously caught by Pylance, where the function actually had red squiggly lines to show that None was a possible return value. For instance, ("apple", "orange") as arguments. Returning None would complicate and cause errors in my function, so I realised that I had to add a 'raise ValueError' to catch anything that fell through the cracks'.

4. Returning a tuple of payoffs from the payoff_matrix function, we unpack it and then update the respective player attributes for 'payoff'.

5. After that, we update or 'append' the history of play in our player instances to track the history of actions of played in previous rounds. This is crucial cause our strategies rely on this, particularly the Grim Trigger. 

6. Our function then prints or calls upon __str__ in our player instances. This prints an f-string that tells us what strategy they used and what their cumulative payoffs are. 

    **Design Choice*
    I tried learning the 'Pandas' library to visualise our strategies and payoffs better by tracking every combination of strategies and payoffs. But I struggled to implement it successfuly, and I reduced the scope to just a simple 'experiment' where our results are output through a string. 

7. The function ends by returning a tuple of the cumulative payoffs. 
    **Design Choice*
    While the main program doesn't explicitly need this return value to print the results, returning the data made unit-testing the simulation significantly easier.


## Unit-Testing

### Design Choices
The unit test uses pytest as taught. It is standard for the most part. 
It tests the strategy functions, the play and payoff functions, and then the setters plus str for my Player class too.
I initially wanted to use sys.exit() for my setters, but I wanted to make unit-testing easier, so I changed them to normal exceptions. This also has the added benefit of making my requirements.txt empty. 

The most interesting design choice here is the testing of my 'get' class method.
Because it relies on the user's input, I struggled to envision how it might be tested.
While reading the pytest documentation, I discovered 'monkeypatch', which could replace the 'input' function and fake the input. 

I also learnt of the difference between iterator and iterable. As my code requires consecutive inputs, I needed to use the next function to jump from one fake input to the next in my list. I had to use the 'iter' function to transform my list into an iterator which allowed me to use my next function on it. Learning this technique was a major step in understanding how to test functions that required user input. 

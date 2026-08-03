import prisoners_dilemma as pd
import pytest

'''

struggled to see how to test the get class function cause it relied on input, but found monkeypatch feature in pytest that allows fake user input!
'''

def test_str():
    player=pd.Player("Bob", "grim trigger")
    assert str(player)=="Bob has 0 points using grim trigger"
    player.payoff=10
    assert str(player)=="Bob has 10 points using grim trigger"
    player.strategy="always cooperate"
    assert str(player)=="Bob has 10 points using always cooperate"


def test_always_cooperate():
    assert pd.always_cooperate(["C"], ["D"])=="C"
    assert pd.always_cooperate([], ["C", "C", "D", "C"])=="C"
    assert pd.always_cooperate([], [])=="C"

def test_always_defect():
    assert pd.always_defect(["C"], ["C"])=="D"
    assert pd.always_defect([], [])=="D"
    assert pd.always_defect(["D"], ["C", "C", "D"])=="D"

def test_grim_trigger():
    assert pd.grim_trigger([], [])=="C"
    assert pd.grim_trigger(["C", "C", "C"], ["C", "C", "C"])=="C"
    assert pd.grim_trigger(["C"], ["C", "D"])=="D"
    assert pd.grim_trigger(["C", "D"], ["C", "C"])=="C"
    assert pd.grim_trigger(["C", "D", "D", "D"], ["D", "D", "D", "C"])=="D"

def test_reverse_tit_for_tat():
    assert pd.reverse_tit_for_tat([], [])=="D"
    assert pd.reverse_tit_for_tat(["C"], ["D"])=="D"
    assert pd.reverse_tit_for_tat(["C", "D"], ["C", "D"])=="D"
    assert pd.reverse_tit_for_tat(["C", "C"], ["D", "D", "C"])=="C"
    #note we dont catch for errors here cause we assume they'll be caught under payoff_matrix

def test_tit_for_tat():
    assert pd.tit_for_tat([], [])=="C"
    assert pd.tit_for_tat(["C"], ["D"])=="D"
    assert pd.tit_for_tat(["C", "D"], ["C", "D"])=="D"
    assert pd.tit_for_tat(["C", "C"], ["D", "D", "C"])=="C"

def test_play_game():
    Player_A=pd.Player("Player A", "always cooperate")
    Player_B=pd.Player("Player B", "always cooperate")
    assert pd.play_game(Player_A, Player_B, rounds=100)==(200,200)
    Player_A=pd.Player("Player A", "always cooperate")
    Player_B=pd.Player("Player B", "always defect")
    assert pd.play_game(Player_A, Player_B, rounds=100)==(-200,1000)
    Player_A=pd.Player("Player A", "tit-for-tat")
    Player_B=pd.Player("Player A", "reverse tit-for-tat")
    assert pd.play_game(Player_A, Player_B, rounds=100)==(400,400)
    Player_A=pd.Player("Player A", "grim trigger")
    Player_B=pd.Player("Player A", "always defect")
    assert pd.play_game(Player_A, Player_B, rounds=100)==(-2,10)
    Player_A=pd.Player("Player A", "always defect")
    Player_B=pd.Player("Player A", "always defect")
    assert pd.play_game(Player_A, Player_B, rounds=100)==(0,0)

def test_payoff_matrix():
    assert pd.payoff_matrix("C", "D")==(-2,10)
    assert pd.payoff_matrix("D", "C")==(10,-2)
    assert pd.payoff_matrix("C", "C")==(2,2)
    assert pd.payoff_matrix("D", "D")==(0,0)
    with pytest.raises(ValueError):
        pd.payoff_matrix("A", "Apple")
        pd.payoff_matrix("", "")
        pd.payoff_matrix(None, "C")

def test_player_setters():
    player=pd.Player("Alice", "tit-for-tat")
    with pytest.raises(ValueError):
        player.strategy="random"
    with pytest.raises(ValueError):
        player.payoff=2.5
    with pytest.raises(ValueError):
        player.history=["C", "X"]
    with pytest.raises(ValueError):
        player.name=""

def test_player_get(monkeypatch):
    fake_input=iter(["Bob", "always defect"])
    monkeypatch.setattr('builtins.input', lambda _:next(fake_input)) 
    player=pd.Player.get()
    assert player.name=="Bob"
    assert player.strategy=="always defect"



'''
#note that there's a difference between iterator and iterable-- a list is an iterable, but not an iterator
we need our list to be an iterator cause we need our function to remember where we are or bookmark where we are each time, so we can use our 'next' function to move to the next one after
next requires an iterator
the iter function turns an iterable into an iterator

'''



'''
A(tit-for-tat): 400 points, B(reverse tit for tat):400
A(always defect): 1000 points, B(always cooperate):-200
A(grim trigger): -2, B(always defect):10 
A(always cooperate):200, B(always cooperate):200
A(always defect):0 B(always defect):0
'''


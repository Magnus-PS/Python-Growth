#The dumbest AI ever ...
#Playing rock, paper, scissors against the computer.

print("Welcome to Rock, Paper, Scissors!")

#Human v. human version:

'''
player_1 = str(input("Enter player 1's choice: \n")).lower()
player_2 = str(input("Enter player 2's choice: \n")).lower()

print("Rock, paper, scissors ... shoot!")

if player_1 == player_2:
    print("You chose the same. It's a draw.")
elif player_1 == "rock" and player_2 == "scissors":
    print("Rock beats scissors. Player 1 wins.")
elif player_2 == "rock" and player_1 == "scissors":
    print("Rock beats scissors. Player 2 wins.")
elif player_1 == "rock" and player_2 == "paper":
    print("Paper beats rock. Player 2 wins.")
elif player_1 == "paper" and player_2 == "rock":
    print("Paper beats rock. Player 1 wins.")
elif player_1 == "scissors" and player_2 == "paper":
    print("Scissors beat paper. Player 1 wins.")
elif player_1 == "paper" and player_2 == "scissors":
    print("Scissors beat paper. Player 2 wins")
else:
    print("Please enter 'rock', 'paper', or 'scissors'!!!")

'''

#Human v. computer version:

import random #since we use randint()

c = random.randint(0,2)

if c == 0:
    comp = "rock"
elif c == 1:
    comp = "scissors"
else:
    comp = "paper"

human = str(input("Human ... enter your hand: \n")).lower()

print("Rock, paper, scissors ... shoot!")

if human == comp:
    print("You chose the same. It's a draw.")
elif human == "rock": 
    if comp == "scissors":
        print("Rock beats scissors. Humanity wins.")
    elif comp == "paper":
        print("Paper beats rock. AI wins.")
elif human == "scissors":
    if comp == "paper":
        print("Scissors beats paper. Humanity wins.")
    elif comp == "rock":
        print("Rock beats scissors. AI wins")
elif human == "paper":
    if comp == "rock":
        print("Paper beats rock. Humanity wins.")
    elif comp == "scissors":
        print("Scissors beats paper. AI wins.")
else:
    print("Please enter 'rock', 'paper', or 'scissors'!!!")


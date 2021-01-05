#Guessing game
##Guess a number between 1 and 10 with hints from the computer.

import random

print("Welcome to the Guessing Game ...")

n = random.randint(1,10)
done = False

while done != True:

    guess = int(input("Guess a number between 1 and 10: \n"))

    if n == guess:
        print("Correct! Great guess.")

        replay = str(input("Do you want to play again? (y/n) \n"))

        if replay == "y":
            n = random.randint(1,11) #generate a new number
        elif replay == "n":
            done = True
        else:
            print("Incorrect entry ...")

    elif n > guess:
        print("Too low, try again.")
    elif n < guess:
        print("Too high, try again.")
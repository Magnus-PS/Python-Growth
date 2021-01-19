import requests
from random import choice
from bs4 import BeautifulSoup

'''SCRAPING FUNCTIONALITY:
-Scrape ALL quotes, authors, bio-links from www.quotes.toscrape.com
-Read in quotes and authors for all (10) pages
'''

all_quotes = []

for page in range(1,11):
    response = requests.get(f"https://quotes.toscrape.com/page/{page}/")
    soup = BeautifulSoup(response.text, "html.parser")
    
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        all_quotes.append({
            'text': quote.find(class_="text").get_text(),
            'author': quote.find(class_="author").get_text(),
            'bio-link': quote.find("a")["href"]
        })
    #Verify functionality of scraper
    #print(all_quotes)

'''GAMEPLAY LOGIC:
-Welcome user to game and display a random quote from our all_quotes list
-While the guess is not the author continue looping through and providing hints
--Hint #1: birthdate and place
--Hint #2: first initial of first name
--Hint #3: first initial of last name
-Track the number of guesses remaining
--Exit loop if guess is correct
--Flash a 'Game Over' message if they run out of guesses
'''

def start_game():

    quote = choice(all_quotes)
    rem_guesses = 4
    guess = ''

    print("Welcome to the Quote Guessing Game! Here's a quote:")
    print(quote["text"])

    while guess.lower() != quote["author"].lower() and rem_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining = {rem_guesses}\n")

        if guess.lower() == quote["author"].lower():
            print("Correct! You got it right :)")
            break
        
        rem_guesses -= 1

        if rem_guesses == 3:
            bio_req = requests.get(f"https://quotes.toscrape.com{quote['bio-link']}/")
            soup = BeautifulSoup(bio_req.text, "html.parser")
            birthdate = soup.find(class_="author-born-date").get_text()
            location = soup.find(class_="author-born-location").get_text()
            print(f"Hint #1: the author was born on {birthdate} {location}.")
        elif rem_guesses == 2:
            print(f"Hint #2: the 1st initial of the author's first name is {quote['author'][0]}.")
        elif rem_guesses == 1:
            last_initial = quote['author'].split(' ')[1][0]
            print(f"Hint #2: the last initial of the author's last name is {last_initial}.")
        else:
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}.")

    '''REPLAY FUNCTIONALITY:
    -track an again variable
    '''

    again = ""
    while again.lower() not in ('yes', 'y', 'no', 'n'):
        again = input("Would you like to play again (y/n)?")
    if again.lower() in ('yes','y'):
        return start_game()
    else:
        print("Very well, goodbye ...")

start_game()

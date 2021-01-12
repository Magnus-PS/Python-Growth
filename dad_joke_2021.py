import requests
import pyfiglet
from termcolor import colored
 
#ask user for message and output color
msg = "Dad Joke 2021"
col = "blue"
 
#format message and color prior to printing
ascii_out = pyfiglet.figlet_format(msg)
colored_ascii = colored(ascii_out, col)
print("Welcome to ...")
print(colored_ascii)

#store the joke topic
topic = input("Let me tell you a joke. Give me a topic: ")

url = "https://icanhazdadjoke.com/search"

#request the json contents from our url:
response_j = requests.get(
    url, 
    headers={"Accept": "application/json"},
    params={"term":topic})

#return the number of jokes AND one joke (to be displayed)
data = response_j.json()
num = len(data['results'])
if num == 0:
    print("Sorry ... there aren't any jokes on that topic.")
else:
    print(f"I've got {num} jokes about {topic}, here's one:")
    print(data['results'][0]['joke'])
import requests
from bs4 import BeautifulSoup
from csv import writer

#Download data
response = requests.get("https://www.rithmschool.com/blog")
#print(response.text) #verify that we've downloaded HTML
soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article")

with open("blog_data.csv", "w") as csv_file:
    csv_writer = writer(csv_file) 
    csv_writer.writerow(["title", "link", "date"])

#use developer tools to identify code block(s) of interest and then retrieve article titles
    for article in articles:
        a_tag = article.find("a")
        title = a_tag.get_text() 
        url = a_tag["href"]
        date = article.find("time")["datetime"]
        csv_writer.writerow([title, url, date])
    

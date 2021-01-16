import requests
from bs4 import BeautifulSoup
from csv import writer

#Download data
response = requests.get("https://www.rithmschool.com/blog")
soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article")

#Create csv file to be written to
with open("blog_data.csv", "w") as csv_file:
    csv_writer = writer(csv_file) 
    csv_writer.writerow(["title", "link", "date"])

#Use developer tools to identify code block(s) of interest and then retrieve article titles
    for article in articles:
        a_tag = article.find("a")
        title = a_tag.get_text() 
        url = a_tag["href"]
        date = article.find("time")["datetime"]
        #For each blog entry (on the page), write to file
        csv_writer.writerow([title, url, date])
    

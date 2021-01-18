import requests
from bs4 import BeautifulSoup
from csv import writer

#Download data
response = requests.get("http://www.magnusskonberg.com/blog")
soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article")

#print(articles)

#Create csv file to be written to
with open("personal_blog.csv", "w") as csv_file:
    csv_writer = writer(csv_file) 
    csv_writer.writerow(["title", "link", "date"])

#Use developer tools to identify code block(s) of interest and then retrieve article titles
    for article in articles:
        a_tag = article.find("a")
        h_tag = article.find("h2")

        all_text = h_tag.text #retain title text
        split = all_text.split() #split at each " "
        relevant = split[2:] #remove data, white space
        title = " ".join(relevant, ) #rejoin with relevant Title 

        ###NEXT: navigate all blog pages for data

        url = a_tag["href"]
        date = article.find("time")["datetime"]
        
    #For each blog entry (on the page), write to file
        csv_writer.writerow([title, url, date])
    

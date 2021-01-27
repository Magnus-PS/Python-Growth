'''
The purpose of this project is to explore the livability of various US cities.
'''

import requests
import re
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen


#.............................................PHASE I.............................................#
##Read in population data, create initial dataframe, and for high-growth, mid-size cities##


#Scrape population data from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")

#Create arrays to hold extracted data
cities = []
states = []
populations = []
growth_rates = []
densities = []

bad_chars = ['+','%'] #characters to be removed from growth_rates list

for table in tables:
    rows = table.find_all('tr')

    for row in rows:
        cells = row.find_all('td')

        if len(cells) == 11 and len(cities) < 316: #to ensure proper table and row entries:
            city = cells[1]
            cities.append(re.sub("[\[].*?[\]]", "", city.text.strip())) #remove characters between parentheses and parentheses "[]" themselves

            state = cells[2]
            states.append(state.text.strip())

            population = cells[3]
            populations.append(int(re.sub("[^0-9]", "", population.text.strip())))

            growth = cells[5]
            growth_rates.append(''.join(i for i in growth.text.strip() if not i in bad_chars))

            density = cells[8]
            densities.append(int(re.sub("[^0-9]", "", density.text.strip())))

#convert to float and assign negative growth as 0.00
growth_rates = [float(rate) if rate[0].isnumeric() else 0.00 for rate in growth_rates ]

#Verify that lists include data that we're looking for ---DONE---
##print(cities)
##print(states)
#print(populations)
#print(growth_rates)
##print(densities)

#Re-join lists into pandas dataframe
df = pd.DataFrame()
df['City'] = cities
df['State'] = states
df['Population'] = populations
df['Density (per sq mi)'] = densities
df['Growth (10 yr)'] = growth_rates

#Verify formation of dataframe ---DONE---
##print(df)

#Filter data for high-growth, mid-size cities (ie. career opportunities)
rslt_df = df[df['Growth (10 yr)'] > 20.00] #filter for EXTREMELY high growth
filtered_df = rslt_df[rslt_df['Population'] > 200000] #filter for cities with 200k+ inhabitants

#Verify the formation of our filtered dataframe ---DONE---
##print(filtered_df)
##print(len(filtered_df)) #14 cities


#.............................................PHASE II.............................................#
##Read in affordability csv, add 'Cost of Living' column to dataframe, and filter out high cost of living cities##


advisor_col = pd.read_csv("advisor_col.csv") #add actual affordability values (where provided)

a_dict = {}
affordabilities = []

#Compare city values between dfs and when they match store the corresponding city and Cost of Living Index (CoLI) in our a_dict dictionary
for city_a in filtered_df['City']:
    
    for index, city_b in enumerate(advisor_col['City']):
        #when our city of interest is in both dfs, set the city and CoLI as key-value pairs
        if city_a == city_b:
            a_dict.update({city_a : float(advisor_col.iloc[index]['Cost of Living Index'])})
    
    #if our filtered_df city has an associate CoLI, assign it. Otherwise, default 100.00 (assumed national avg)
    if city_a in list(a_dict.keys()):
        affordabilities.append(a_dict[city_a])
    else:
        affordabilities.append(100.00)

filtered_df['Cost of Living'] = affordabilities 

#Verify that we've filtered and accounted for Cost of Living with our df ---DONE---
##print(filtered_df)

a_df = filtered_df[filtered_df['Cost of Living'] < 120.0] #filter for lower cost of living cities (those beneath 120.0)
a_df = a_df[a_df['City'] != 'Irvine'] #manual override since Irvine's incredibly expensive
##print(a_df)


#.............................................PHASE III.............................................#
##Create / import active lifestyle metric, add 'Lifestyle' and 'Total Score' columns to dataframe, and filter out unhealthy, outlier cities.##

'''
Section Notes 
[1] Active Lifestyle Score equation: (2 * WalletHub score) - (1.3 * obesity rate)
Being that Denver had the high score on both metrics (high Wallethub score, lowest obesity rate), I took it to be the "model city" (nearest 100.00) 
and formulated the equation based on this assumption ...

[2] Total Score equation: (4 * 'Growth' * 0.3) + (1 / 'Cost of Living') * 9900 * 0.4) + ('Active Lifestyle' * 0.3)
My aim here was to ensure all metrics had a positive correlation with the Total Score (hence inverting the 'Cost of Living') and were on a similar scale (~100.00),
before utilizing multipliers on each metric (0.3 * 'Growth', 0.4 * 'Affordability', 0.3 * 'Active Lifestyle' ).
'''

a_l = pd.read_csv("active_lifestyle.csv") #read in csv
a_df['Active Lifestyle'] = list(a_l['Active Lifestyle Score']) #add lifestyle column

#Verify additional column ---DONE---
##print(a_df)

scores = []

for index, row in a_df.iterrows():
    scores.append(((row['Growth (10 yr)'] * 4) * 0.3) + (((1 / row['Cost of Living']) * 9900) * 0.4) + ((row['Active Lifestyle']) * 0.3)) 

a_df['Total Score'] = scores #add Total Score column
a_df = a_df[a_df['City'] != 'Frisco'] #manual override since Frisco's growth makes it an outlier


#.............................................PHASE IV.............................................#
##Prepare output file: rank based on 'Total Score' and output to csv.##


final_df = a_df.sort_values(by='Total Score', ascending=False) #rank based on total score
final_df.to_csv('Livability_Rankings.csv', index=False) #export to csv without index

import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

data = []
# Make it dynamic
Agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

url = "https://www.worldometers.info/coronavirus/#main_table"

page = requests.get(url, headers=Agent)
soup = BeautifulSoup(page.text, "html.parser")

#fix makes error on line 22
table1 = soup.find('div', {'id': 'main_table'})
table = soup.find('table', {'id': 'main_table_countries_today'})

# Fix statement
thead = table.find('thead')
headers = thead.find_all('th')
    
tbody = table.find('tbody')
rows = tbody.find_all('tr')
    
for row in rows:
    cols = row.find_all('td')
    item = {}
    item['Country']  = cols[1].text.strip()
    item['Total Cases'] = cols[2].text.strip()
    item['New Cases']  = cols[3].text.strip()
    item['Total Deaths'] = cols[4].text.strip()
    item['New Deaths'] = cols[5].text.strip()
    item['Total Recovered'] = cols[6].text.strip()
    item['New Recovered'] = cols[7].text.strip()
    item['Active Cases'] = cols[8].text.strip()
    item['Serious/Critical Cases'] = cols[9].text.strip()
    item['Total Tests'] = cols[12].text.strip()
    item['Population'] = cols[14].text.strip()

    data.append(item)

    print(f"Country: {item['Country']}")
    print(f"Total Cases: {item['Total Cases']}")
    print(f"New Cases: {item['New Cases']}")
    print(f"Total Deaths: {item['Total Deaths']}")
    print(f"New Deaths: {item['New Deaths']}")
    print(f"Total Recovered: {item['Total Recovered']}")
    print(f"New Recovered: {item['New Recovered']}")
    print(f"Active Cases: {item['Active Cases']}")
    print(f"Serious/Critical Cases: {item['Serious/Critical Cases']}")
    print(f"Total Tests: {item['Total Tests']}")
    print(f"Population: {item['Population']}")

delay = random.uniform(1, 4)  # Random delay between 1 and 4 seconds
print(f"Waiting for {delay:.2f} seconds before next request...")
time.sleep(delay)

df = pd.DataFrame(data)
df.to_excel("cases2.xlsx")
df.to_csv("cases2.csv")
df.to_json("case2.json")
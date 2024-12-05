import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
scraped_quotes = set()
current_page = 1
proceed = True

while(proceed):
    print(f"Currently scraping page: {current_page}")
    
    url = f"https://quotes.toscrape.com/page/{current_page}/"
    
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.text, "html.parser")
    
    all_quotes = soup.find_all('div', {'class': 'quote'})
    
    if not all_quotes:
        proceed = False
        print("No more quotes found. Stopping...")
    else:
        for quote in all_quotes:
            quote_text = quote.find('span', {'class': "text"}).text[1:-1]  # Remove extra quotation marks
            
            if quote_text in scraped_quotes:
                continue  # Skip this quote if it's already been scraped
            
            # Add the quote text to the set of scraped quotes
            scraped_quotes.add(quote_text)
            
            item = {}
            item['Quote']  = quote.find('span', {'class': "text"}).text[1:-1]
            item['Author'] = quote.find('small', {'class': "author"}).text
            item['About']  = "https://quotes.toscrape.com/" + quote.find('a').attrs["href"]
            tags           = quote.find_all('a', {'class': 'tag'})
            item['Tags']   = ', '.join(tag.text for tag in tags)
            data.append(item)
            
            print(f"Quote: {item['Quote']}")
            print(f"Author: {item['Author']}")
            print(f"About: {item['About']}")
            print(f"Tags: {item['Tags']}")
            print("-" * 80)

        next_page = soup.find('li', {'class': 'next'})
        if next_page:
            current_page += 1 
        else:
            proceed = False 

    delay = random.uniform(1, 4)  # Random delay between 1 and 3 seconds
    print(f"Waiting for {delay:.2f} seconds before next request...")
    time.sleep(delay)

df = pd.DataFrame(data)
df.to_excel("quotes.xlsx")
df.to_csv("quotes.csv")

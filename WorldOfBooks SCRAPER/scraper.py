import selector
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

class Extraction:

    def __init__(self):
        self.url, self.category = selector.SelectCategory().run()
        self.all_data = []
        self.max_pages = int(input("Enter Max Pages: "))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'
        }
        
    def extract(self, page_number):
        max_retries = 3
        for _ in range(max_retries):
            response = requests.get(f"{self.url}/{page_number}", headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
                return []
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all items on the current page
            items = soup.find_all(class_="item gridItem col-6 col-sm-4 col-lg-3 mb-4")
            
            if items:
                break  # If items are found, exit the retry loop
            else:
                print(f"Retrying page {page_number}...")
                time.sleep(random.uniform(1, 5))  # Random delay before retry

        # After all retries, check if items were found
        if not items:
            print(f"No more items found at page {page_number}.")
            return []  # Return an empty list if no items are found after retries

        data = []
        for item in items:
            title_tag = item.find(class_="title")
            title = title_tag.text.strip() if title_tag else 'No Title'
            
            author_tag = item.find(class_="author")
            author = author_tag.text.strip() if author_tag else "None"
        
            condition_tag = item.find(class_="itemType")
            condition = condition_tag.text.strip() if condition_tag else "None"
        
            price_tag = item.find(class_="itemPrice")
            price = price_tag.contents[0].strip() if price_tag else "None"

            data.append({
                'title': title,
                'author': author,
                'condition': condition,
                'price': price
            })
        
        print(f"Scraped page {page_number} with {len(items)} items.")
        return data
    
    def save_to_csv(self):
        cleaned_category = re.sub(r'[<>:"/\\|?*]', '_', self.category)
        df = pd.DataFrame(self.all_data)
        csv_file_name = f"data/{cleaned_category}.csv".replace(" ", "_").lower()
        df.to_csv(csv_file_name, index=False)
        print(f"Data has been written to {csv_file_name}")

    def run(self):
        with ThreadPoolExecutor(max_workers=30) as executor:  
            futures = [executor.submit(self.extract, page) for page in range(1, self.max_pages + 1)]
            for future in as_completed(futures):
                result = future.result()
                if result:  # Check if the result is not empty
                    self.all_data.extend(result)
        
        print(f"\nTotal Number of Items: {len(self.all_data)}")
        self.save_to_csv()

if __name__ == '__main__':
    while True:
        scrap = Extraction()
        scrap.run()

        another = input("\nDo you want to scrape another category? (yes/no): ").strip().lower()
        
        if another != 'yes':
            print("Exiting the scraper.")
            break 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

class WebCrawler:
    def __init__(self):
        self.home_page_url = "https://www.wob.com/en-gb"
        self.response = requests.get(self.home_page_url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.all_links = []  # To store all extracted links
    
    def extract_main_links(self):
        """Extract main category links from homepage."""
        main_links = []
        link_containers = self.soup.find_all('div', class_='categoryItem')

        for container in link_containers:
            link_tag = container.find('a', class_='categoryName')
            if link_tag:
                link_url = urljoin(self.home_page_url, link_tag['href'])
                main_links.append(link_url)
        
        for main_url in main_links:
            print(main_url)
            self.all_links.append(main_url)
    
        return main_links

    def scrape_category(self):
        """Scrape category links from each main link."""
        main_links = self.extract_main_links()
        category_links = []

        for url in main_links:
            print(f"\nScraping category page: {url}")
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                category_div = soup.find('div', class_='categoryFilter')
                
                if category_div:
                    categories = category_div.find_all('a')
                    for link in categories:
                        category_url = urljoin(url, link['href'])
                        print(f"Category URL: {category_url}")
                        category_links.append(category_url)
                        self.all_links.append(category_url)
                else:
                    print(f"No category filter found at {url}.")
            else:
                print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            
        return category_links

    def scrape_subcategory(self):
        """Scrape subcategory links from each category."""
        category_links = self.scrape_category()

        for url in category_links:
            print(f"\nScraping subcategory page: {url}")
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                subcategory_div = soup.find('div', class_='categoryFilter')
                
                if subcategory_div:
                    subcategory_links = subcategory_div.find_all('a')
                    for link in subcategory_links:
                        subcategory_url = urljoin(url, link['href'])
                        print(f"Subcategory URL: {subcategory_url}")
                        self.all_links.append(subcategory_url)
                else:
                    print(f"No subcategory filter found at {url}.")
            else:
                print(f"Failed to retrieve {url}. Status code: {response.status_code}")

    def save_to_csv(self, filename="extracted_links.csv"):
        """Save all extracted URLs to a CSV file using pandas."""
        df = pd.DataFrame(self.all_links)
        df.to_csv(filename, index=False, header=False)
        print(f"\nData saved to {filename}")

    def run(self):
        # Step 1: Extract categories and subcategories
        self.scrape_subcategory()
        
        print(f"\nTotal Links: {len(self.all_links)}")
        
        # Step 2: Save all URLs to a CSV file
        self.save_to_csv()

if __name__ == '__main__':
    crawler = WebCrawler()
    crawler.run()

import pandas as pd

class SelectCategory:

    def __init__(self):
        self.file_path = 'extracted_links.csv'
        self.data = pd.read_csv(self.file_path, header=None)
        self.home_page_url = "https://www.wob.com/en-gb/category/"

    def extract_slug(self):
        self.data['slug'] = self.data[0].apply(lambda url: url.rstrip('/').split('/')[-1])

        print("CATEGORY:")
        for slug in self.data['slug']:
            print(f"\t{slug}")
    
    def select_category(self):
        selector = input("\nEnter Category (e.g. crime-mystery): ")  
        self.category = selector
        search_category = self.home_page_url + selector
        print(f"\nSearch Category: {search_category}")
        return search_category
    
    def run(self):
        self.extract_slug()
        return self.select_category(), self.category

if __name__ == '__main__':
    select = SelectCategory()
    select.run()
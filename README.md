# WorldOfBooks Crawler Scraper

## Overview

This project is a web scraping tool designed to extract data from the **World of Books** website. It is composed of four Python scripts that work together to collect and visualize data about items in various categories. The project uses multithreading to optimize the scraping process and includes a data visualization component to present the results.

## Project Structure

- **extract_links.py**: Gathers category links from the main page.
- **selector.py**: Provides a user interface for selecting a category to scrape.
- **scraper.py**: Scrapes data from the selected category using multithreading for faster execution.
- **data_visualization.py**: Visualizes the scraped data in an interactive bar chart.

## Requirements

The following Python libraries are required to run the project:

- `requests`
- `beautifulsoup4`
- `pandas`
- `plotly`
- `concurrent.futures`

## How It Works

### 1. **extract_links.py**

This script is responsible for fetching all url links from the World of Books homepage. It parses the HTML, extracts and stores the URLs these in a CSV file. 

### 2. **selector.py**

Once the URLs are fetched, the selector.py script prompts the user to input a "category". The "category" also known as a 'slug,' refers to the specific term used at the end of the URL (e.g., crime-mystery), representing the category the user wishes to scrape. This "category" is then appended to the base URL to form the complete URL for that category.

After the "category" is selected, the script constructs the URL and initiates the scraping process by passing it to the scraper, which retrieves and processes data from the chosen category. This allows for targeted scraping based on the user's input.

### 3. **scraper.py** (Multithreading Implementation)

The `scraper.py` script is the core of the project, responsible for scraping book data such as title, author, condition, and price from the selected category. The key feature here is the **use of multithreading** through the `ThreadPoolExecutor`.

### How Multithreading Works:

Without multithreading, the scraper would process each page sequentially, which would significantly slow down the scraping process. To overcome this limitation, the script uses a **thread pool** for parallel processing. 

- The `max_pages` value allows the user to specify the total number of pages they want to scrape.
- The scraper launches up to 30 threads at a time, each processing a different page in parallel. As one thread finishes, a new one starts until all pages are scraped.
- This parallel processing drastically reduces the overall scraping time compared to sequential scraping.

For each page, the scraper extracts all items and their respective details, appending them to a list for further processing.

This approach is particularly useful when scraping a large number of pages since it prevents the bottleneck of sequential HTTP requests.

After the data is scraped, it's saved as a CSV file, named according to the selected category.

### 4. data_visualization.py

Once the data has been scraped and saved, the `data_visualization.py` script generates an interactive bar chart using Plotly. The chart shows the number of items scraped in each category, providing an easy-to-understand visual summary of the data.

- The CSV files are processed to count the number of items in each category.
- A bar chart is generated with categories on the X-axis and the number of items on the Y-axis.
- The total number of items is also displayed in the chart's title for added clarity.

#### **Important: Update the Folder Path**

Before running the `data_visualization.py` script, you need to update the file path to match the location where your CSV files are saved.

1. Open the `data_visualization.py` script.
2. Find the line:
   ```python
   self.folder_path = r"replace_with_file_path\data"
   ```
3. Replace `"replace_with_file_path"` with the correct path on your machine where the `data` folder is located. For example:
   ```python
   self.folder_path = r"C:\Users\YourUsername\Documents\WorldOfBooks Crawler Scraper\data"
   ```
4. Save the file and run the script.

This will ensure that the script can locate your CSV files and generate the visualizations correctly.

## Usage

1. **Clone the repository using the terminal**:
   
   Open a terminal on your local machine and run the following commands:
   git clone https://github.com/SHAIMOOM251283/WorldOfBooks-Crawler-Scraper.git
   cd WorldOfBooks-Crawler-&-Scraper
   
2. **Clone the repository using VS Code's Git integration**:
   
   If you prefer using VS Code, follow these steps:
   
   - Open **VS Code**.
   - Open the **Command Palette** by pressing `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS).
   - Type `Git: Clone` and select the option `Git: Clone`.
   - Enter the repository URL: `https://github.com/SHAIMOOM251283/WorldOfBooks-Crawler-Scraper.git`.
   - Choose a local folder to clone the repository into.
   - When prompted, select **Open** to load the repository in VS Code.

3. **Clone the repository using VS Code's Integrated Terminal**:
   
   You can also clone the repository directly from VS Code’s built-in terminal:
   
   - Open **VS Code**.
   - Open the integrated terminal by pressing `Ctrl + `` (backtick)` or navigating to **Terminal** > **New Terminal**.
   - Run the following commands in the terminal:
   
    git clone https://github.com/SHAIMOOM251283/WorldOfBooks-Crawler-Scraper.git
    cd WorldOfBooks-Scraper

4. **Run extract_links.py**:
    Before starting the scraping process, run 'extract_links.py' to extract and store the URLs in a CSV file.
    
5. **Run the scraper**:
    To start the scraping process, simply execute the `scraper.py` script:
    python scraper.py
    
6. **Select a category**:
    After running the script, you will be prompted to enter the name of the category you'd like to scrape. You can select the category from the URLs that will be displayed in the terminal. For example:
    - URL: https://www.wob.com/en-gb/category/crime-mystery
    - category: crime-mystery

7. **Enter the maximum number of pages**:
    The scraper will then ask for the `max_pages` you wish to scrape. This value determines how many pages will be processed in parallel, taking full advantage of multithreading.

8. **Visualize the data**:
    After scraping, run the `data_visualization.py` script to generate an interactive bar chart.
    
## Example

If you select the "crime-mystery" category and specify `max_pages` as 1500, the scraper will launch 30 threads, each scraping a different page simultaneously. This will drastically reduce the time taken to gather data compared to sequential scraping.

### Sample Output:

- **Scraped Data**:
    ```
    Scraped page 1 with 48 items.
    Scraped page 2 with 48 items.
    Scraped page 3 with 48 items.
    Scraped page 4 with 48 items.
    Scraped page 5 with 48 items.
    ```

- **Data Visualization**: The bar chart will display "crime-mystery" as the category and the total number of items scraped across all pages.

## Conclusion

This project demonstrates efficient web scraping techniques using Python, BeautifulSoup, and multithreading, along with data visualization using Plotly. By leveraging multithreading with the `max_pages` parameter, the scraper can process multiple pages in parallel, drastically improving performance and reducing overall execution time.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

urls = [
    "https://openaccess.thecvf.com/CVPR2023?day=2023-06-20",
    "https://openaccess.thecvf.com/CVPR2023?day=2023-06-21",
    "https://openaccess.thecvf.com/CVPR2023?day=2023-06-22"
    ]

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")  # This line should help

# Choose Chrome Browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

data = []

for url in urls:
    driver.get(url)

    # Find all paper links
    paper_links = driver.find_elements(By.CSS_SELECTOR, '.ptitle a')

    # Collect all the URLs of the papers
    paper_urls = [paper.get_attribute('href') for paper in paper_links]

    # paper_urls = paper_urls[:10]

    for idx, paper_url in enumerate(paper_urls):
        driver.get(paper_url)

        # Wait for the new page to load
        time.sleep(2)

        # Parse the new page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the title, abstract, and PDF link
        title = soup.find('div', id='papertitle').text.strip()
        print(f"Processing paper {idx+1} of {len(paper_urls)}: {title}")
        abstract = soup.find('div', id='abstract').text.strip()
        pdf_link = 'https://openaccess.thecvf.com/' + soup.find('a', text='pdf')['href']
        
        data.append({
            'title': title,
            'abstract': abstract,
            'pdf_link': pdf_link
        })


with open('cvpr_2023_papers.json', 'w') as f:
    json.dump(data, f)


driver.quit()
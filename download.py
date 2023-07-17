from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from bs4 import BeautifulSoup
import json
import time

BASE_URL="https://openaccess.thecvf.com/"

yeartopage = {
    2023 : ['CVPR2023?day=2023-06-20', 'CVPR2023?day=2023-06-21', 'CVPR2023?day=2023-06-22'],
    2022 : ['CVPR2022?day=2022-06-21', 'CVPR2022?day=2022-06-22', 'CVPR2022?day=2022-06-23', 'CVPR2022?day=2022-06-24'],
    2021 : ['CVPR2021?day=2021-06-21', 'CVPR2021?day=2021-06-22', 'CVPR2021?day=2021-06-23', 'CVPR2021?day=2021-06-24', 'CVPR2021?day=2021-06-25'],
    2020 : ['CVPR2020?day=2020-06-16', 'CVPR2020?day=2020-06-17', 'CVPR2020?day=2020-06-18'],
    2019 : ['CVPR2019?day=2019-06-18', 'CVPR2019?day=2019-06-19', 'CVPR2019?day=2019-06-20'],
    2018 : ['CVPR2018?day=2018-06-19', 'CVPR2018?day=2018-06-20', 'CVPR2018?day=2018-06-21'],
    2017 : ['CVPR2017'],
    2016 : ['CVPR2016'],
    2015 : ['CVPR2015'],
    2014 : ['CVPR2014'],
    2013 : ['CVPR2013']
}


yeartourl = {year: [BASE_URL+ day for day in yeartopage[year]] for year in yeartopage.keys()}

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")  # This line should help

# Choose Chrome Browser
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()), options=chrome_options)
missing=[]

for year in range(2022, 2023):
    data = []
    urls=yeartourl[year]
    print()
    print('==============================')
    print(f'Processing papers for CVPR {year}')
    print('==============================')
    print()
    
    for url in urls:

        driver.get(url)

        # Find all paper links
        paper_links = driver.find_elements(By.CSS_SELECTOR, '.ptitle a')

        # Collect all the URLs of the papers
        paper_urls = [paper.get_attribute('href') for paper in paper_links]

        # paper_urls = paper_urls[:10]

        for idx, paper_url in enumerate(paper_urls):
            try:
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

            except Exception as e:
                print(f'Error {str(e)}')
                missing.append(url)


    with open(f'data/cvpr_{year}_papers.json', 'w') as f:
        json.dump(data, f)


driver.quit()
print('Please manually download some papers from these urls:')
print(missing)

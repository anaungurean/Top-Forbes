from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup

class ForbesScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.profile_billionaire_urls = []

    def scrape_page_top_billionaires(self):
        try:
            html_source = self.driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            divs = soup.find_all('div', class_='TableRow_row__L-0Km')

            for div in divs:
                div_id = div['id']
                url = f'https://www.forbes.com/profile/{div_id}'
                if len(self.profile_billionaire_urls) >= 200:
                   break
                self.profile_billionaire_urls.append(url)

        except Exception as e:
            print(f"An error occurred: {e}")

    def run_scraper(self):
        try:
            self.driver.get('https://www.forbes.com/billionaires/')
            self.scrape_page_top_billionaires()

            button_locator = (By.CSS_SELECTOR, 'button.Pagination_gotoPageBtn__een24[aria-label="go to page 1"]')
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(button_locator)
            ).click()
            self.scrape_page_top_billionaires()
            print(self.profile_billionaire_urls)

        finally:
            self.driver.quit()




